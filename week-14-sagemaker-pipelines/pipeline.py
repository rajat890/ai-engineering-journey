"""
pipeline.py — defines and runs the 3-step SageMaker Pipeline

Steps:
  1. ProcessingStep  -> runs preprocessing.py    (80/20 stratified split)
  2. TrainingStep    -> runs train.py            (fit CountVectorizer + MultinomialNB)
  3. ProcessingStep  -> runs evaluate.py         (score model on held-out test set)

LOCAL MODE: instance_type="local" everywhere. This runs each step in Docker
on your own machine instead of provisioning real SageMaker instances -- no
quota needed, no AWS charges. Switching to the cloud later is a one-line
change per step (instance_type="local" -> "ml.m5.large").
"""
import sagemaker
from sagemaker.sklearn.processing import SKLearnProcessor
from sagemaker.sklearn.estimator import SKLearn
from sagemaker.processing import ProcessingInput, ProcessingOutput
from sagemaker.workflow.steps import ProcessingStep, TrainingStep
from sagemaker.workflow.pipeline import Pipeline
from sagemaker.workflow.pipeline_context import LocalPipelineSession
from sagemaker.workflow.properties import PropertyFile
from sagemaker.workflow.condition_step import ConditionStep
from sagemaker.workflow.conditions import ConditionGreaterThanOrEqualTo
from sagemaker.workflow.functions import JsonGet, Join
from sagemaker.workflow.fail_step import FailStep
from sagemaker.workflow.parameters import ParameterFloat
from sagemaker.inputs import TrainingInput

# --- Setup ---------------------------------------------------------------

# LocalPipelineSession is the local-mode equivalent of PipelineSession.
# Everything downstream (processors, estimators, steps) must be built with
# this session object, or SageMaker will try to hit real AWS APIs.
local_pipeline_session = LocalPipelineSession()

role = "arn:aws:iam::396510133350:role/service-role/AmazonSageMaker-ExecutionRole-20260626T115618"

import os

# NOTE: Even in "local mode," a Pipeline (unlike a plain Processor.run())
# still needs REAL S3 to hand data between steps -- only the compute
# (running preprocessing.py/train.py/evaluate.py) happens in local Docker.
# So this must be a plain filesystem path with NO "file://" scheme --
# the SDK uploads it to your account's default S3 bucket automatically.
RAW_DATA_PATH = os.path.abspath("./data/training_data.json")

# --- Step 1: Processing (split) ------------------------------------------

sklearn_processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_type="local",       # <-- runs in Docker on your Mac
    instance_count=1,
    base_job_name="aria-preprocess",
    sagemaker_session=local_pipeline_session,
)

step_process = ProcessingStep(
    name="PreprocessData",
    processor=sklearn_processor,
    inputs=[
        ProcessingInput(source=RAW_DATA_PATH, destination="/opt/ml/processing/input"),
    ],
    outputs=[
        ProcessingOutput(output_name="train", source="/opt/ml/processing/output/train"),
        ProcessingOutput(output_name="test", source="/opt/ml/processing/output/test"),
    ],
    code="preprocessing.py",
)

# --- Step 2: Training ------------------------------------------------------

sklearn_estimator = SKLearn(
    entry_point="train.py",
    role=role,
    instance_type="local",       # <-- runs in Docker on your Mac
    instance_count=1,
    framework_version="1.2-1",
    py_version="py3",
    base_job_name="aria-classifier",
    sagemaker_session=local_pipeline_session,
)

step_train = TrainingStep(
    name="TrainModel",
    estimator=sklearn_estimator,
    inputs={
        # THE HAND-OFF: step_process hasn't run yet at definition time, so we
        # can't pass a real S3/local path here. properties.ProcessingOutputConfig...
        # is a placeholder the SDK resolves automatically once step_process
        # actually finishes -- same idea as Terraform's resource attribute
        # references (${aws_s3_bucket.x.arn}) resolving only after apply.
        "train": TrainingInput(
            s3_data=step_process.properties.ProcessingOutputConfig.Outputs[
                "train"
            ].S3Output.S3Uri
        )
    },
)

# --- Step 3: Evaluation -----------------------------------------------------

evaluator = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_type="local",
    instance_count=1,
    base_job_name="aria-evaluate",
    sagemaker_session=local_pipeline_session,
)

# PropertyFile = a named pointer to a JSON file a step will produce.
# We don't know the real S3 path yet (it depends on the execution ID,
# generated fresh each run) -- this just tells the pipeline: "the
# EvaluateModel step's 'evaluation' output will contain a file called
# evaluation.json, and later steps can query values out of it by name."
evaluation_report = PropertyFile(
    name="EvaluationReport",       # <-- the name we'll reference later
    output_name="evaluation",      # <-- must match ProcessingOutput's output_name below
    path="evaluation.json",        # <-- the actual filename inside that output
)

step_evaluate = ProcessingStep(
    name="EvaluateModel",
    processor=evaluator,
    inputs=[
        # Two hand-offs here: model artifact from step_train, test set from step_process.
        ProcessingInput(
            source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model",
        ),
        ProcessingInput(
            source=step_process.properties.ProcessingOutputConfig.Outputs[
                "test"
            ].S3Output.S3Uri,
            destination="/opt/ml/processing/test",
        ),
    ],
    outputs=[
        ProcessingOutput(output_name="evaluation", source="/opt/ml/processing/evaluation"),
    ],
    code="evaluate.py",
    property_files=[evaluation_report],  # <-- attach it to this step
)

# --- Step 4: Condition (pass/fail gate) --------------------------------------

# ParameterFloat = a pipeline input variable, like a Terraform `variable`.
# Override it per-run with pipeline.start(parameters={"AccuracyThreshold": 0.8})
# without touching this code -- default_value is what's used if you don't.
accuracy_threshold = ParameterFloat(name="AccuracyThreshold", default_value=0.7)

# JsonGet is the "read a value out of a PropertyFile" mechanism we set up
# last task. json_path walks into the JSON structure evaluate.py wrote:
#   {"classification_metrics": {"accuracy": {"value": 0.667}}}
cond_gte_threshold = ConditionGreaterThanOrEqualTo(
    left=JsonGet(
        step_name=step_evaluate.name,
        property_file=evaluation_report,
        json_path="classification_metrics.accuracy.value",
    ),
    right=accuracy_threshold,
)

# if_steps run when the condition is True, else_steps when False.
#
# NOTE ON WHY THESE STEPS ARE DEFINED HERE (not earlier, and not added to
# pipeline.steps below): SageMaker explicitly forbids listing a step in
# BOTH the pipeline's top-level `steps=[...]` AND inside a ConditionStep's
# if_steps/else_steps -- it belongs to the condition, not the pipeline
# directly. The ConditionStep itself (added to pipeline.steps) is what
# makes these reachable at execution time.

register_processor = SKLearnProcessor(
    framework_version="1.2-1",
    role=role,
    instance_type="local",
    instance_count=1,
    base_job_name="aria-register",
    sagemaker_session=local_pipeline_session,
)

step_register = ProcessingStep(
    name="RegisterModelPlaceholder",
    processor=register_processor,
    inputs=[
        ProcessingInput(
            source=step_train.properties.ModelArtifacts.S3ModelArtifacts,
            destination="/opt/ml/processing/model",
        ),
    ],
    code="register_model.py",
)

# FailStep stops the pipeline execution in a FAILED state with a clear
# message -- this is the "else" branch. Join builds the message string
# out of a mix of literal text and resolved runtime values (the actual
# accuracy number), similar to an f-string but resolved at execution time
# since neither value exists yet when this code runs.
step_fail = FailStep(
    name="AccuracyBelowThreshold",
    error_message=Join(
        on=" ",
        values=[
            "Model accuracy",
            JsonGet(
                step_name=step_evaluate.name,
                property_file=evaluation_report,
                json_path="classification_metrics.accuracy.value",
            ),
            "is below required threshold",
            accuracy_threshold,
        ],
    ),
)

step_condition = ConditionStep(
    name="CheckAccuracyThreshold",
    conditions=[cond_gte_threshold],
    if_steps=[step_register],
    else_steps=[step_fail],
)

# --- Assemble and run --------------------------------------------------------

pipeline = Pipeline(
    name="aria-classifier-pipeline",
    parameters=[accuracy_threshold],
    steps=[step_process, step_train, step_evaluate, step_condition],
    sagemaker_session=local_pipeline_session,
)

if __name__ == "__main__":
    print("Upserting pipeline definition...")
    pipeline.upsert(role_arn=role)

    print("Starting pipeline execution (local mode -- watch Docker)...")
    execution = pipeline.start()
    # NOTE: local-mode execution runs synchronously inside .start() itself --
    # there is no .wait() method like there is for real cloud pipelines.
    print(f"Pipeline execution status: {execution.list_steps()}")

    print("Pipeline run complete. Check evaluate step logs for metrics.")