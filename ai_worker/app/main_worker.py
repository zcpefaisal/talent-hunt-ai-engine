import time
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("ai_worker")

if __name__ == "__main__":
    logger.info("🚀 AI Worker successfully started in background mode!")
    while True:
        time.sleep(1)