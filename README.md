# ✈️ Airline Tweet Sentiment Analysis – End-to-End Pipeline
## 📊 Architecture Overview:

<pre> ┌─────────────────────────────┐ │ Twitter API (Search v2) │ └────────────┬────────────────┘ │ ▼ ┌─────────────────────────────────────────┐ │ Azure Data Factory (REST Copy Activity)│ │ - Polls Twitter API via Linked Service │ │ - Writes JSON to Blob Storage │ └────────────────┬────────────────────────┘ │ ▼ ┌──────────────────────────────────────────┐ │ Azure Blob Storage (Bronze Layer) │ │ - Raw JSON response from Twitter │ │ - Stored as tweets_bronze.json │ └────────────────┬─────────────────────────┘ │ ▼ ┌──────────────────────────────────────────┐ │ Azure Databricks (Bronze ➝ Silver) │ │ - Extracts & cleans tweet text │ │ - Removes special chars/emojis │ │ - Stores as Delta table │ │ tweets_silver │ └────────────────┬─────────────────────────┘ │ ▼ ┌──────────────────────────────────────────┐ │ Azure Databricks (Silver ➝ Gold) │ │ - Applies predict_sentiment(text) │ │ - Appends new column │ │ - Stores Gold as Delta table │ │ tweets_gold (text + sentiment) │ └────────────────┬─────────────────────────┘ │ ▼ ┌──────────────────────────────────────────┐ │ Power BI │ │ - Connects to Gold Delta layer │ │ - Visualizes: │ │ • Sentiment distribution │ │ • Word clouds, timelines │ │ • Common complaints │ └──────────────────────────────────────────┘ </pre>

▼ Twitter API
   - Twitter Search API v2 or recent tweets endpoint
   - Provides tweets in JSON format

▼ Azure Data Factory (ADF)
   - REST Linked Service to Twitter API
   - Copy Activity fetches tweets on schedule
   - Stores raw tweet JSON in Azure Blob Storage

▼ Azure Blob Storage (Bronze Layer)
   - Stores raw JSON files from ADF
   - Example: tweets_bronze.json

▼ Azure Databricks (Bronze ➝ Silver)
   - Reads raw JSON from Blob (Bronze)
   - Extracts only 'text' field from each tweet
   - Cleans data: removes nulls, emojis, unwanted characters
   - Writes cleaned data as Delta table (Silver)

▼ Delta Table: Silver Layer
   - Contains only one column: 'text'
   - Data stored in Delta format in Blob Storage

▼ Azure Databricks (Silver ➝ Gold)
   - Loads Silver Delta table
   - Applies `predict_sentiment(text)` UDF
   - Adds new column: 'predicted_sentiment'
   - Writes enriched data as Gold Delta table

▼ Delta Table: Gold Layer
   - Columns: 'text', 'predicted_sentiment'
   - Stored in Delta format in Blob Storage

▼ Power BI
   - Connects to Gold Delta (via CSV or Synapse / SQL Warehouse)
   - Visualizes:
     • Sentiment distribution (positive/negative/neutral)
     • Most frequent complaint words
     • Timeline of sentiment trends
     • Filter by keywords or tweet content

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
