# monitoring/app.py

import streamlit as st
import pandas as pd
import json
import os

# Load the IMDB dataset
@st.cache_data
def load_imdb_data():
    df = pd.read_csv("IMDB Dataset.csv") 
    df["text_length"] = df["review"].astype(str).apply(len)
    return df

# Load and parse the logs
@st.cache_data
def load_logs():
    logs_path = "/logs/prediction_logs.json"
    if not os.path.exists(logs_path):
        return pd.DataFrame()
    
    with open(logs_path, "r") as f:
        lines = f.readlines()

    data = [json.loads(line) for line in lines]
    df = pd.DataFrame(data)
    df["text_length"] = df["request_text"].astype(str).apply(len)
    return df

# Load data
st.title("Sentiment Model Monitoring Dashboard")
imdb_df = load_imdb_data()
log_df = load_logs()

if log_df.empty:
    st.warning("No predictions logged yet.")
    st.stop()

# --- 1. Data Drift: Sentence length comparison ---
st.subheader("📏 Sentence Length Distribution")
st.write("Comparing input text length: IMDB training data vs. incoming requests")

hist_data = [
    imdb_df["text_length"],
    log_df["text_length"]
]
group_labels = ["IMDB Dataset", "Logged Requests"]

st.plotly_chart(
    pd.DataFrame({
        "IMDB": imdb_df["text_length"],
        "Logged": log_df["text_length"]
    }).plot.hist(bins=30, alpha=0.6, title="Sentence Length Histogram").figure,
    use_container_width=True
)

# --- 2. Target Drift ---
st.subheader("Sentiment Distribution Comparison")
col1, col2 = st.columns(2)

with col1:
    st.write("True Sentiment (from user feedback)")
    st.bar_chart(log_df["true_sentiment"].value_counts())

with col2:
    st.write("Predicted Sentiment")
    st.bar_chart(log_df["predicted_sentiment"].value_counts())

# --- 3. Accuracy and Precision ---
st.subheader("Model Performance Metrics")

correct = (log_df["true_sentiment"] == log_df["predicted_sentiment"]).sum()
total = len(log_df)
accuracy = correct / total

pred_pos = log_df[log_df["predicted_sentiment"] == "positive"]
true_pos = pred_pos[pred_pos["true_sentiment"] == "positive"]
precision = len(true_pos) / len(pred_pos) if len(pred_pos) > 0 else 0.0

st.metric("Accuracy", f"{accuracy:.2%}")
st.metric("Precision (Positive Class)", f"{precision:.2%}")

# --- 4. Alert if Accuracy < 80% ---
if accuracy < 0.80:
    st.error("Model accuracy has dropped below 80%!")

# --- Optional: Show log data ---
st.subheader("Raw Logs")
st.dataframe(log_df)
