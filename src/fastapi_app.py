import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.sklearn
import pandas as pd
from typing import List


EXPERIMENT_NAME = "breast_cancer"  # Defined in src/train.py
MODEL_ARTIFACT_PATH = "sklearn_breast_cancer_classifier"


app = FastAPI()


def load_best_model():
    """
    Load the best model from the MLflow experiment.
    """
    runs_df = mlflow.search_runs(experiment_names=[EXPERIMENT_NAME])
    best_run_index = runs_df[
        "metrics.accuracy"
    ].idxmax()  # Get the index of the row with max accuracy
    best_run = runs_df.loc[best_run_index]  # Select that row
    best_run_id = best_run["run_id"]
    model_uri = f"runs:/{best_run_id}/{MODEL_ARTIFACT_PATH}"
    print(f"Loading model from: {model_uri}")
    return mlflow.sklearn.load_model(model_uri)


model = load_best_model()


class InputData(BaseModel):
    data: List[float]


@app.get("/")
def read_root():
    return {"message": "Welcome to the breast cancer prediction API"}


@app.post("/predict")
def predict(data: InputData):
    """
    Predict the target class for the input data.
    """
    if len(data.data) != 30:
        return {"error": "Input data must have 30 features"}

    features = [data.data]
    prediction = model.predict(pd.DataFrame(features))
    print(f"Prediction: {prediction[0]}")
    return {"prediction": int(prediction[0])}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
