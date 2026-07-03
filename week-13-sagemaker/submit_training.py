import boto3
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
import time

session = sagemaker.Session()
role = "arn:aws:iam::396510133350:role/service-role/AmazonSageMaker-ExecutionRole-20260626T115618"

bucket = session.default_bucket()
print(f"Using S3 bucket: {bucket}")

s3 = boto3.client("s3", region_name="us-east-1")
s3.upload_file(
    "data/training_data.json",
    bucket,
    "aria-training/training_data.json"
)

train_input = f"s3://{bucket}/aria-training/"
print(f"Training data uploaded to: {train_input}")

estimator = SKLearn(
    entry_point="train.py",
    source_dir="training_script",
    role=role,
    instance_type="ml.m5.large",
    instance_count=1,
    framework_version="1.2-1",
    py_version="py3",
    base_job_name="aria-classifier"
)

print("Starting training job...")
estimator.fit({"train": train_input})

print(f"\nTraining complete!")
print(f"Model artifact location: {estimator.model_data}")