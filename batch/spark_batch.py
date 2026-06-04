import os
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

    print("=== Question 10: Top 3 Days with Most Logs ===")
    q10_top_days.run(df)

    print("=== Question 14: Node with Most KERNRTSP Events ===")
    q14_kernrtsp_node.run(df)

    print("=== Question 7: Average Weekly DDR Errors ===")
    q7_ddr_errors_weekly.run(df)

    # print("=== Question 18: Earliest Fatal Lustre Mount Failed ===")
    # q18_lustre_fatal.run(df)

    spark.stop()

if __name__ == "__main__":
    main()