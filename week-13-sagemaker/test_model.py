import pickle
import os

model_dir = "./output/model"

with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
    model = pickle.load(f)

with open(os.path.join(model_dir, 'vectorizer.pkl'), 'rb') as f:
    vectorizer = pickle.load(f)

test_questions = [
    "EC2 virtual machine",
    "S3 bucket storage",
    "VPC networking subnet",
    "Lambda serverless function",
    "EBS volume block"
]

print("Model predictions:")
print("-" * 40)
for q in test_questions:
    X = vectorizer.transform([q])
    prediction = model.predict(X)[0]
    print(f"{q:<30} → {prediction}")