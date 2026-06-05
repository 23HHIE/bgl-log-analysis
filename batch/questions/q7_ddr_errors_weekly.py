# Question7: For each week, what is the average number of times ”ddr errors” were detected and corrected? Assume a week runs from Monday to Sunday.

from pyspark.sql import functions as F

def run(df):
    weekly = (
        df.filter(F.lower(F.col("message")).contains("ddr errors"))
        .groupBy("week_start")
        .count()
    )

    avg_result = weekly.agg(F.avg("count").alias("avg_per_week"))

    weekly.orderBy("week_start").show(truncate=False)

    avg_result.show()
    return {
        "weekly_counts": [row.asDict() for row in weekly.collect()],
        "average_per_week": avg_result.collect()[0]["avg_per_week"]
    }