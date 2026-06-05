import os
import time
from kafka import KafkaProducer

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "bgl-logs")
DATA_PATH = os.environ.get("DATA_PATH", "/data/BGL.log")

# producer = KafkaProducer(
#     bootstrap_servers=KAFKA_BROKER,  # Kafka broker address
#     value_serializer=lambda v: v.encode("utf-8")  # Serialize log lines as UTF-8 encoded bytes
# )

producer = None
for i in range(12):
    try:
         producer = KafkaProducer(
             bootstrap_servers=KAFKA_BROKER,  # Kafka broker address
             value_serializer=lambda v: v.encode("utf-8")  # Serialize log lines as

         )
         print("Connected to Kafka at {KAFKA_BROKER}.")
         break
    except NoBrokerAvailable:
        print(f"Kafka not ready, retrying in 5s... ({i+1}/12)")
        time.sleep(5)
if producer is None:
    raise RuntimeError("Could not connect to Kafka after 50 secconds")

with open(DATA_PATH, "r") as f:
    for line in f:
        producer.send(KAFKA_TOPIC, value=line.strip())
        time.sleep(0.001)  # Simulate real-time streaming

producer.flush()
producer.close()
print("Finished sending log lines to Kafka.")
