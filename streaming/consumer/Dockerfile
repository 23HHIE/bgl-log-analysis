FROM apache/spark:3.5.0

USER root

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENTRYPOINT []
CMD ["/opt/spark/bin/spark-submit","--packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0","--master", "local[*]","spark_streaming.py"]