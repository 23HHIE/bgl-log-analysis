import os
from fastapi import APIRouter, WebSocket
from aiokafka import AIOKafkaConsumer

router = APIRouter()

KAFKA_BROKER = os.environ.get("KAFKA_BROKER", "kafka:9092")
KAFKA_TOPIC = os.environ.get("KAFKA_TOPIC", "bgl-logs")

@router.websocket("/ws/stream")
async def stream(websocket: WebSocket):
    await websocket.accept()

    consumer = AIOKafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BROKER,
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            line = message.value.decode("utf-8")
            if "FATAL" in line:
                await websocket.send_text(line)
    finally:
        await consumer.stop()
