from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_predict_positive():
    response = client.post("/predict", json={
        "text": "This movie was great!",
        "true_sentiment": "positive"
    })
    assert response.status_code == 200
    assert "predicted_sentiment" in response.json()

def test_predict_negative():
    response = client.post("/predict", json={
        "text": "I did not like this movie.",
        "true_sentiment": "negative"
    })
    assert response.status_code == 200
    assert "predicted_sentiment" in response.json()

def test_missing_field():
    response = client.post("/predict", json={"text": "Missing sentiment!"})
    assert response.status_code == 422 
