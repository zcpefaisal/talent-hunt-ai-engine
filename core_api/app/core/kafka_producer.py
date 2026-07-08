import json
import logging
import asyncio
from aiokafka import AIOKafkaProducer
from app.core.config import settings

logger = logging.getLogger(__name__)

class KafkaManager:
    def __init__(self):
        self.producer: AIOKafkaProducer = None

    async def start(self):
        logger.info(f"Starting Kafka producer with bootstrap servers: {settings.KAFKA_BOOTSTRAP_SERVERS}")

        self.producer = AIOKafkaProducer(
            bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

        # Implementing a retry mechanism for starting the Kafka producer
        max_retries = 5
        retry_delay = 5  # seconds
        for attempt in range(1, max_retries + 1):
            try:
                await self.producer.start()
                logger.info("Kafka producer started successfully.")
                return # Exit the method if the producer starts successfully
            
            except Exception as e:
                logger.error(f"Failed to start Kafka producer (attempt {attempt}): {e}")
                if attempt < max_retries:
                    await asyncio.sleep(retry_delay) # Wait before retrying
                else:
                    raise RuntimeError("Failed to start Kafka producer after maximum retries.")

    
    async def stop(self):
        if self.producer:
            logger.info("Stopping Kafka producer...")
            await self.producer.stop()
            logger.info("Kafka producer stopped successfully.")


    async def send_message(self, topic: str, message: dict):
        if not self.producer:
            raise RuntimeError("Kafka producer is not initialized.")
        
        try:
            logger.info(f"Sending message to topic '{topic}': {message}")
            await self.producer.send_and_wait(topic, message)
            logger.info(f"Message sent to topic '{topic}' successfully.")
        except Exception as e:
            logger.error(f"Failed to send message to topic '{topic}': {e}")
            raise e
        
kafka_manager = KafkaManager()