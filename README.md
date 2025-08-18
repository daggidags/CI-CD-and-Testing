# CI-CD-and-Testing
Sentiment Analysis System with Monitoring

This project is a continuation of the previous repository: A5_Model_Monitoring and demonstrates a production-ready MLOps pipeline for sentiment analysis. It integrates CI/CD best practices, containerized deployment, and live model monitoring.

- `FastAPI` backend for serving predictions and logging them
- `Streamlit` dashboard for monitoring model performance over time
- All prediction logs are written to a shared volume (`/logs/prediction_logs.json`), allowing real-time monitoring.
- Unit tests

## Project Structure

```
├── api/                  # FastAPI backend
│   ├── main.py
│   ├── Dockerfile
│   ├── requirements.txt
│   └── sentiment_model.pkl
|   |__ test_api.py      # testing unit
|   |__ IMDB Dataset.csv
│
├── monitoring/           # Streamlit dashboard
│   ├── app.py
│   ├── Dockerfile
│   ├── requirements.txt
|   |__ test_dashboard.py # test for Streamlit dashboard
│
├── sentiment_logs/          
|
├── .github/workflows/ci.yml           
└── README.md
```

## API Endpoints (FastAPI)

| Endpoint    | Method | Description |
|-------------|--------|-------------|
| `/health`   | GET    | Health check – returns `{"status": "ok"}` |
| `/predict`  | POST   | Accepts JSON input `{"text": "...", "true_sentiment": "..."}` and returns predicted sentiment |

Example:
```json
{
  "text": "I loved the movie!",
  "true_sentiment": "positive"
}
```

Returns:
```json
{
  "predicted_sentiment": "positive"
}
```

### Running the System with Docker

1. Build the Containers

   ```bash
   docker build -t sentiment-api ./api
   docker build -t sentiment-monitoring ./monitoring
   ```
2. Create Shared Log Volume

   ```bash
   docker volume create sentiment_logs
   ```
3. Start Services
   ```bash
  docker run -d -p 8000:8000 --name sentiment-api \
  --mount source=sentiment_logs,target=/logs sentiment-api
  
  docker run -d -p 8501:8501 --name sentiment-monitor \
  --mount source=sentiment_logs,target=/logs sentiment-monitor
   ```

Once running, access the UI at: http://<your_public_ip>:8501

### Hosting on AWS EC2 

This project can also be deployed and tested on an **AWS EC2 instance**.

#### Steps to Deploy:

1. **Launch an EC2 instance** (e.g., Ubuntu).
2. **Add Security Groups** for ports `8000` and `8501` in your EC2 Security Group.
3. **SSH into your instance**:
   ```bash
   ssh -i /path/to/your-key.pem ubuntu@<your-ec2-public-ip>
   ```

4. **Install Docker**:
   ```bash
   sudo apt update
   sudo apt install docker.io -y
   sudo systemctl start docker
   sudo systemctl enable docker
   ```

5. **Clone the repo and navigate into the directory**:
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

6. **Create a shared Docker volume**:
   ```bash
   docker volume create sentiment_logs
   ```

7. **Build and run the FastAPI container**:
   ```bash
   docker build -t sentiment-api ./api
   docker run -d -p 8000:8000 --name sentiment-api \
     --mount source=sentiment_logs,target=/logs sentiment-api
   ```

8. **Build and run the Streamlit dashboard container**:
   ```bash
   docker build -t sentiment-monitor ./monitoring
   docker run -d -p 8501:8501 --name sentiment-monitor \
     --mount source=sentiment_logs,target=/logs sentiment-monitor
