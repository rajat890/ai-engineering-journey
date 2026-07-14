"""
inference.py — required by SKLearnModel for registration

This is NOT run today (nothing gets deployed in this session) -- but
SageMaker requires an inference script to exist before a model can be
registered, since a registered model must be immediately deployable.
This becomes real/tested once you build an endpoint in a later week.

Implements the four functions SageMaker's SKLearn serving container expects:
  model_fn    -> how to load the model from disk
  input_fn    -> how to parse an incoming request
  predict_fn  -> how to run inference
  output_fn   -> how to format the response
"""
import json
import os
import pickle


def model_fn(model_dir):
    with open(os.path.join(model_dir, "model.pkl"), "rb") as f:
        model = pickle.load(f)
    with open(os.path.join(model_dir, "vectorizer.pkl"), "rb") as f:
        vectorizer = pickle.load(f)
    return {"model": model, "vectorizer": vectorizer}


def input_fn(request_body, content_type="application/json"):
    data = json.loads(request_body)
    return data["texts"]  # expects {"texts": ["some text", "another text"]}


def predict_fn(input_data, model_artifacts):
    vectorizer = model_artifacts["vectorizer"]
    model = model_artifacts["model"]
    X = vectorizer.transform(input_data)
    return model.predict(X)


def output_fn(prediction, accept="application/json"):
    return json.dumps({"predictions": prediction.tolist()})