from pyspark.sql.functions import col, expr, regexp_replace
import json

# ----------------------------------------
#  Define Input Path (Raw JSON)
# ----------------------------------------
bronze_path = "abfss://your-container@your-storageaccount.dfs.core.windows.net/twitter/bronze/"

# ----------------------------------------
# Read JSON Files from Blob
# Each file is like: { "data": [ {tweet1}, {tweet2} ] }
# ----------------------------------------
df_raw = spark.read.option("multiline", "true").json(bronze_path)

# JSON structure: root.data[*].text
df_flat = df_raw.selectExpr("explode(data) as tweet").select("tweet.text")

# ----------------------------------------
# Clean Data 
# ----------------------------------------

# Remove nulls or short text
df_clean = df_flat.filter(col("text").isNotNull() & (expr("length(text) > 5")))

# Remove emojis and special characters
df_clean = df_clean.withColumn("text", regexp_replace(col("text"), "[^\\x00-\\x7F]", ""))
df_clean = df_clean.withColumn("text", regexp_replace(col("text"), "[^a-zA-Z0-9\\s.,!?]", ""))

# ----------------------------------------
# Show Cleaned Tweets
# ----------------------------------------
df_clean.show(10, truncate=False)

# ----------------------------------------
# Save to CSV
# ----------------------------------------
silver_path_csv = "abfss://your-container@your-storageaccount.dfs.core.windows.net/twitter/silver/tweets_text_only_csv"

df_clean.write.format("delta").mode("overwrite").save(silver_path)