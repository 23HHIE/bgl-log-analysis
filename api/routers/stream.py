import os
from fastapi import APIRouter, WebSocket
from kafka import KafkaConsumer

router = APIRouter()

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "bgl_logs")

@router.websocket("/ws/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        # ensure we read from the beginning of the topic when the consumer starts
        auto_offset_reset="earliest",
        # decode bytes to string
        value_deserializer=lambda v: v.decode("utf-8")
    )

    for message in consumer:
        line = message.value
        # only send lines containing "FATAL" to the client
        if "FATAL" in line:
            await websocket.send_text(line)