"""
evaluate.py — SageMaker EvaluateStep

Runs inside a scikit-learn container. SageMaker mounts:
  model:  /opt/ml/processing/model/model.pkl
          /opt/ml/processing/model/vectorizer.pkl
  test:   /opt/ml/processing/test/test.json
  output: /opt/ml/processing/evaluation/evaluation.json

The output JSON is registered as a "PropertyFile" in pipeline.py, which lets
a later ConditionStep read specific fields from it (e.g. accuracy) without
needing to open the file itself — SageMaker resolves that reference for you.
"""
import json
import pickle
import os
import tarfile
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

MODEL_DIR = "/opt/ml/processing/model"
TEST_PATH = "/opt/ml/processing/test/test.json"
OUTPUT_DIR = "/opt/ml/processing/evaluation"


def main():
    # SageMaker ALWAYS packages a TrainingStep's output as model.tar.gz --
    # it never hands over model.pkl/vectorizer.pkl as loose files. This step
    # extracts that tarball before we can load anything from it.
    tarball_path = os.path.join(MODEL_DIR, "model.tar.gz")
    print(f"Extracting {tarball_path}...")
    with tarfile.open(tarball_path, "r:gz") as tar:
        tar.extractall(path=MODEL_DIR)

    print("Loading model and vectorizer...")
    with open(os.path.join(MODEL_DIR, "model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(MODEL_DIR, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)

    print(f"Loading test data from: {TEST_PATH}")
    with open(TEST_PATH, "r") as f:
        test_data = json.load(f)

    texts = [item["text"] for item in test_data]
    true_labels = [item["label"] for item in test_data]

    # IMPORTANT: transform (not fit_transform) — reuse the vocabulary learned
    # during training. Fitting a new vectorizer here would be like validating
    # a deploy against a different config than what's running in prod.
    X_test = vectorizer.transform(texts)
    predictions = model.predict(X_test)

    # average="weighted" accounts for label imbalance, same reason we
    # stratified the split in preprocessing.py.
    metrics = {
        "accuracy": accuracy_score(true_labels, predictions),
        "precision": precision_score(true_labels, predictions, average="weighted", zero_division=0),
        "recall": recall_score(true_labels, predictions, average="weighted", zero_division=0),
        "f1": f1_score(true_labels, predictions, average="weighted", zero_division=0),
    }

    print(f"Evaluation metrics: {metrics}")

    # Structure matches what a SageMaker ClarifyCheckStep / ConditionStep
    # conventionally expects: metrics nested under a named key.
    report = {
        "classification_metrics": {
            "accuracy": {"value": metrics["accuracy"]},
            "precision": {"value": metrics["precision"]},
            "recall": {"value": metrics["recall"]},
            "f1": {"value": metrics["f1"]},
        }
    }

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "evaluation.json"), "w") as f:
        json.dump(report, f)

    print("Evaluation complete. Report written.")


if __name__ == "__main__":
    main()