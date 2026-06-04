# Question2: How many fatal log entries on Tuesday or Thursday resulted from "machine check interrupt"?

from pyspark.sql import functions as F

def run(df):
    # result = (
    #     df.filter(
    #         (F.col("level") == "FATAL") &
    #         (F.col("day_of_week").isin(3, 5)) &
    #         (F.lower(F.col("message")).contains("MACHINE_CHECK_INTERRUPT"))
    #     )
    #     .count()
    # )

    # print(f"Count: {result}")

    df.filter(F.col("level") == "FATAL").select("alert_flag", "level", "message").show(5, truncate=False)