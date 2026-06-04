# Question18: On which date and time was the earliest fatal kernel error where the message contains"Lustre mount FAILED"?

from pyspark.sql import functions as F

def run(df):
    result = (
        df.filter(
            (F.col("level") == "FATAL") &
            (F.col("component") == "KERNEL") &
            (F.lower(F.col("message")).contains("lustre mount failed"))
        )
        .orderBy(F.col("dt").asc())
        .limit(1)
        .select("datetime_str","node", "message")
    )

    result.show(truncate=False)