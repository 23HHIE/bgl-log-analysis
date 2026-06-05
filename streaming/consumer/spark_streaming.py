import os
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "bgl-logs")

spark = SparkSession.builder.appName("BGL Log Streaming Analysis").getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# Read streaming data from Kafka
raw_stream = spark.readStream.format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_BROKER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

# Parse the raw log lines into structured format
lines = raw_stream.selectExpr("CAST(value AS STRING) as line")

# Assuming the log format is consistent, we can split the line into components
split_col = F.split(F.col("line"), " ", 10)
parsed = lines.select(
    split_col[0].alias("alert_flag"),
    split_col[3].alias("node"),
    split_col[4].alias("datetime_str"),
    split_col[7].alias("component"),
    split_col[8].alias("level"),
    split_col[9].alias("message"),
)

# Example query: Count the number of FATAL logs in the stream
fatal_stream = parsed.filter(F.col("level") == "FATAL")\
    .groupBy(F.col("level"))\
    .count()

# Output the results to the console every 10 seconds
query = fatal_stream.writeStream \
    .outputMode("complete")\
    .format("console")\
    .trigger(processingTime="10 seconds")\
    .start()

query.awaitTermination()