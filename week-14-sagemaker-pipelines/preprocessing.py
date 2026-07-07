import json
import os
from sklearn.model_selection import train_test_split

INPUT_PATH = "/opt/ml/processing/input/training_data.json"
TRAIN_OUTPUT_DIR = "/opt/ml/processing/output/train"
TEST_OUTPUT_DIR = "/opt/ml/processing/output/test"


def main():
    print(f"Reading raw data from: {INPUT_PATH}")
    with open(INPUT_PATH, "r") as f:
        data = json.load(f)

    labels = [item["label"] for item in data]
    print(f"Total examples: {len(data)}")
    print("Splitting 80/20, stratified by label...")

    train_data, test_data = train_test_split(
        data, test_size=0.2, stratify=labels, random_state=42
    )

    print(f"Train examples: {len(train_data)}")
    print(f"Test examples:  {len(test_data)}")

    os.makedirs(TRAIN_OUTPUT_DIR, exist_ok=True)
    os.makedirs(TEST_OUTPUT_DIR, exist_ok=True)

    with open(os.path.join(TRAIN_OUTPUT_DIR, "train.json"), "w") as f:
        json.dump(train_data, f)
    with open(os.path.join(TEST_OUTPUT_DIR, "test.json"), "w") as f:
        json.dump(test_data, f)

    print("Preprocessing complete.")


if __name__ == "__main__":
    main()