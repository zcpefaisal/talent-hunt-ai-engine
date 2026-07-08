import json
import logging
import asyncio
from aiokafka import AIOKafkaConsumer
from app.core.config import settings

logger = logging.getLogger(__name__)

async def consume_cv_uploads():
    consumer = AIOKafkaConsumer(
        "cv_upload",
        bootstrap_servers = settings.KAFKA_BOOTSTRAP_SERVERS,
        group_id = "cv_upload_consumer_group",
        auto_offset_reset = "earliest",
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    await consumer.start()
    logger.info("Kafka consumer started and listening to 'cv_upload'")

    try:
        async for msg in consumer:
            try:
                # Decode the kafka message value from bytes to string and then parse it as JSON
                payload = msg.value

                # Here we will call our main processing logic (AI / Text Extraction) later
                await asyncio.sleep(2)  # I'm leaving a dummy slip for testing for now.
            
                logger.info(f"Consumed message from topic 'cv_upload': {payload}")

            except json.JSONDecodeError:
                logger.error("Failed to decode JSON from Kafka message")
            except Exception as e:
                logger.error(f"Unexpected error occurred: {e}")

    except Exception as e:
        logger.error(f"Error while consuming messages: {e}")
    finally:
        await consumer.stop()
        logger.info("Kafka consumer stopped.")