# Question: Which node generated the largest number of KERNRTSP events?

from pyspark.sql import functions as F

def run(df):
    result = (
        df.filter(F.col("alert_flag") == "KERNRTSP")
        .groupBy("node")
        .count()
        .orderBy(F.col("count").desc())
        .limit(1)
    )

    result.show(truncate=False)
    return [row.asDict() for row in result.collect()]