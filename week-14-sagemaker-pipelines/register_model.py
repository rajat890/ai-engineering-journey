"""
register_model.py — placeholder "pass" branch action

Only runs if ConditionStep's condition evaluates True (accuracy >= threshold).
In a real project this is where a RegisterModel step would add this model
version to the SageMaker Model Registry. For today, it just proves the
"pass" branch actually fired -- real registration is a good next milestone
once you're comfortable with the ConditionStep mechanics.
"""
import os

MODEL_DIR = "/opt/ml/processing/model"


def main():
    print("Accuracy threshold met.")
    print(f"Model artifact present at: {MODEL_DIR}")
    print("PASS BRANCH: would call RegisterModel here to add this version to the Model Registry.")


if __name__ == "__main__":
    main()