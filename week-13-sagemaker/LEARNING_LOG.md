# Learning Log — Week 13

## Week 13 — Session 1 & 2 — 03 July 2026

### What was built
- train.py — scikit-learn classifier training script
- training_data.json — 12 labeled AWS service examples
- submit_training.py — SageMaker training job submission script
- test_model.py — local model prediction test
- Trained model locally: model.pkl + vectorizer.pkl

### SageMaker training flow
Local machine
→ submit_training.py uploads data + script to S3
→ SageMaker spins up ml.m5.large instance
→ downloads data to SM_CHANNEL_TRAIN
→ runs train.py
→ saves model to SM_MODEL_DIR
→ uploads model.tar.gz to S3
→ instance terminates

### Key concepts learned
- SM_CHANNEL_TRAIN → where SageMaker puts your training data
- SM_MODEL_DIR → where your script saves model artifacts
- SageMaker uploads everything in SM_MODEL_DIR to S3 automatically
- Same script runs locally AND on SageMaker — no code changes needed
- Training instance is ephemeral — spins up, trains, terminates
- You pay only for training duration (~$0.01 for 5 minute job)

### SageMaker vs local training
Local:    python train.py --train ./data --model-dir ./output
SageMaker: same script, AWS sets env vars, manages compute + S3

### Quota issue
- New AWS account quota for training instances = 0
- Submitted increase request — rejected, needs 1 billing cycle history
- Workaround: ran training locally to verify script works
- Will resubmit quota request next billing cycle

### MLOps concepts covered
- Training script pattern (SM_CHANNEL_TRAIN, SM_MODEL_DIR)
- Model artifacts (pkl files → tar.gz → S3)
- SageMaker execution role permissions
- Why EFS is no longer created by default (cost saving)
- Multi-team SageMaker access patterns
- Data integrity: S3 versioning + Model Registry + Experiments
