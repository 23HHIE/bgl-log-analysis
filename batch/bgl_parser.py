"""
BGL log parser — shared parsing logic for all batch and streaming jobs.

Log line format (space-separated):
  col0  alert_flag     e.g. "-" or "KERNRTSP", "KERNMC", "APPSEV"
  col1  timestamp      Unix epoch seconds
  col2  date           YYYY.MM.DD
  col3  node           e.g. R02-M1-N0-C:J12-U11
  col4  datetime       YYYY-MM-DD-HH.MM.SS.microseconds
  col5  node           (repeated)
  col6  msg_type       e.g. RAS
  col7  component      e.g. KERNEL, APP
  col8  level          e.g. INFO, FATAL, WARNING
  col9+ message        free-text, may contain spaces
"""

from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, StringType, TimestampType


def load_bgl(spark: SparkSession, path: str):
    """
    Load BGL.log into a structured Spark DataFrame.

    Each line is split on the first 9 spaces; everything after col8 is
    kept as a single 'message' string.

    Returns a DataFrame with columns:
        alert_flag, timestamp, date_str, node, datetime_str,
        node2, msg_type, component, level, message,
        dt (TimestampType), day_of_week (1=Sun..7=Sat), week_start (DateType)
    """
    raw = spark.read.text(path)

    # Split into exactly 10 parts (9 splits max), preserving spaces in message
    split_col = F.split(raw["value"], " ", 10)

    df = raw.select(
        split_col[0].alias("alert_flag"),
        split_col[1].alias("timestamp"),
        split_col[2].alias("date_str"),
        split_col[3].alias("node"),
        split_col[4].alias("datetime_str"),
        split_col[5].alias("node2"),
        split_col[6].alias("msg_type"),
        split_col[7].alias("component"),
        split_col[8].alias("level"),
        split_col[9].alias("message"),
    )

    # Parse datetime_str: "2005-06-03-15.42.50.363779"
    # Step 1: replace trailing "-HH.MM.SS.ffffff" with " HH:MM:SS"
    # Step 2: replace date separator "-" before time with " "
    dt_normalized = F.regexp_replace(
        F.regexp_replace(
            F.col("datetime_str"),
            r"-(\d{2})\.(\d{2})\.(\d{2})\.\d+$",
            " $1:$2:$3"
        ),
        r"^(\d{4}-\d{2}-\d{2})-",
        "$1 "
    )

    df = df.withColumn("dt", dt_normalized.cast(TimestampType()))

    # day_of_week: 1=Sunday, 2=Monday, ... 7=Saturday (Spark dayofweek convention)
    df = df.withColumn("day_of_week", F.dayofweek("dt"))

    # week_start: ISO week Monday — used for Q7 weekly aggregation
    df = df.withColumn("week_start", F.date_trunc("week", "dt").cast("date"))

    return df
