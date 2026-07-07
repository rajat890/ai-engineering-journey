import argparse
import os
import json
import pickle
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

def train():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    args = parser.parse_args()

    print(f"Loading training data from: {args.train}")
    
    with open(os.path.join(args.train, 'training_data.json'), 'r') as f:
        data = json.load(f)

    texts = [item['text'] for item in data]
    labels = [item['label'] for item in data]

    print(f"Training on {len(texts)} examples")

    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(texts)

    model = MultinomialNB()
    model.fit(X, labels)

    os.makedirs(args.model_dir, exist_ok=True)
    
    with open(os.path.join(args.model_dir, 'model.pkl'), 'wb') as f:
        pickle.dump(model, f)
    
    with open(os.path.join(args.model_dir, 'vectorizer.pkl'), 'wb') as f:
        pickle.dump(vectorizer, f)

    print("Training complete. Model saved.")

if __name__ == '__main__':
    train()
