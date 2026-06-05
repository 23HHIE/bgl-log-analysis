import os
import json
import datetime
import decimal
from pyspark.sql import SparkSession
from bgl_parser import load_bgl
from questions import q10_top_days
from questions import q14_kernrtsp_node
from questions import q7_ddr_errors_weekly
# from questions import q18_lustre_fatal

def main():
    spark = SparkSession.builder.appName("BGL Log Analysis").getOrCreate()

    data_path = os.environ.get("DATA_PATH", "/data/BGL.log")
    df = load_bgl(spark, data_path)
    output_path = os.environ.get("OUTPUT_PATH", "/output")

    results = {}
    results["q10_top_days"] = q10_top_days.run(df)
    results["q14_kernrtsp_node"] = q14_kernrtsp_node.run(df)
    results["q7_ddr_errors_weekly"] = q7_ddr_errors_weekly.run(df)

    def json_serializer(obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return obj.isoformat()
        if isinstance(obj, decimal.Decimal):
            return float(obj)
        raise TypeError(f"Type{type(obj)} not serializable")

    with open(f"{output_path}/results.json", "w") as f:
        json.dump(results, f, indent=2, default=json_serializer)

    spark.stop()

if __name__ == "__main__":
    main()
