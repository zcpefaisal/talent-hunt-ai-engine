# Application entry point\
import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.api import api_router
# Importing the rate limit exceeded handler and error class
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
# Importing the rate limiter
from app.core.limiter import limiter
# Importing the Kafka manager
from app.core.kafka_producer import kafka_manager
from app.core.kafka_consumer import consume_cv_uploads

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup events ---
    logger.info("Starting up the application...")
    await kafka_manager.start()

    # Start the Kafka consumer task for CV uploads
    logger.info("Starting Kafka consumer for CV uploads...")
    consumer_task = asyncio.create_task(consume_cv_uploads())
    yield # Here the app will be running mode
    
    # --- Shutdown events ---
    logger.info("Shutting down the application...")
    await kafka_manager.stop()
    logger.info("Kafka producer stopped successfully.")
    # Cancel the consumer task if it's still running
    consumer_task.cancel()
    logger.info("Waiting for Kafka consumer task to finish...")


    try:
        await consumer_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="Enterprice Scalable Async Backend", version="1.0.0", lifespan=lifespan)

# Setting up the rate limiter with the FastAPI app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


app.include_router(api_router, prefix="/api/v1")

# Root endpoint URL: /
@app.get("/")
def root():
    return {"message": "Welcome to the Enterprice Scalable Async Backend!"}