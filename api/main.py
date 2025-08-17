from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load('sentiment_model.pkl')

class PredictionInput(BaseModel):
    text: str
    true_sentiment: str

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/predict")
def predict_sentiment(input: PredictionInput):
    prediction = model.predict([input.text])[0]

    os.makedirs("/logs", exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "request_text": input.text,
        "predicted_sentiment": prediction,
        "true_sentiment": input.true_sentiment
    }

    with open("/logs/prediction_logs.json", "a") as f:
        f.write(json.dumps(log_entry) + "\n")

    return {"predicted_sentiment": prediction}
