from pyspark.sql import functions as F

def run(df):
    result = (
        df.groupBy("day_of_week")
        .count()
        .orderBy(F.col("count").desc())
        .limit(3)
    )

    result.show()
    return [row.asDict() for row in result.collect()]