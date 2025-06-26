# ✈️ Airline Tweet Sentiment Analysis – End-to-End Pipeline
## 📊 Architecture Overview:
pgsql
Copy
Edit
[Twitter API]
   ↓
(Ingested via ADF Copy REST → Azure Blob Storage)
   ↓
[Azure Blob Storage]  ← Bronze (Raw JSON from Twitter API)
   ↓
[Azure Databricks]
   - Extract tweet text from raw JSON
   - Clean & preprocess text
   ↓
 Silver Layer (Delta Table: Cleaned tweets)
   - Contains only `text` column
   ↓
 Gold Layer (Delta Table: Sentiment Predictions)
   - `text` + `predicted_sentiment` using custom model
   ↓
 Power BI
   - Visualize tweet sentiment distribution and insights
## 📌 Project Description
This project demonstrates an end-to-end data pipeline for Airline Tweet Sentiment Analysis, leveraging Azure Data Factory, Azure Blob Storage, Azure Databricks, and Power BI.

✅ Data Ingestion:
Tweets are ingested from the Twitter API using ADF's Copy REST activity, and stored in Azure Blob Storage in raw JSON format — this forms the Bronze layer.

✅ Bronze → Silver Transformation:
Using Azure Databricks, the raw JSON files are parsed to extract the text field (i.e., the tweet content). The text is cleaned — removing emojis, symbols, nulls — and stored as a Delta Table (Silver layer) containing only the text column.

✅ Silver → Gold Enrichment:
A sentiment prediction function (predict_sentiment) is applied to each tweet using a Python UDF. This adds a new column predicted_sentiment (positive, negative, neutral) based on the tweet content. The resulting DataFrame is stored as the Gold layer in Delta format.

✅ Power BI Integration:
The final Delta table (Gold) is visualized in Power BI, enabling interactive dashboards such as:

Sentiment distribution pie chart

Most frequent complaint terms

Timeline of sentiment changes

Word cloud of tweet keywords

🧠 Key Features
📥 Ingests data via ADF from Twitter REST API

💾 Uses Blob Storage to manage Bronze, Silver, and Gold data layers

🧹 Cleans tweet text with regex, filters nulls and special characters

🤖 Applies custom sentiment analysis logic via UDF

🧱 Stores all processed layers as Delta Lake tables

📊 Power BI visualizations for stakeholder insights

## 🔄 Extendability
🔄 This architecture can be easily extended to a real-time streaming pipeline using:

Azure Event Hub or Kafka to stream tweets

Databricks Structured Streaming to process them live

ML model inference (e.g., LSTM or BERT) in real time
