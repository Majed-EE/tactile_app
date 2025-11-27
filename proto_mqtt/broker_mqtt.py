import asyncio
import logging
from hbmqtt.broker import Broker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MQTT Broker")

# Broker configuration
config = {
    'listeners': {
        'default': {
            'type': 'tcp',
            'bind': 'localhost:1883',  # Listen on localhost port 1883
        },
    },
    'auth': {
        'allow-anonymous': True,  # Allow connections without authentication
    },
    'topic-check': {
        'enabled': False,  # Allow all topics (for testing)
    }
}

async def start_broker():
    broker = Broker(config)
    await broker.start()
    logger.info("MQTT Broker started on localhost:1883")
    
    try:
        # Keep broker running
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        logger.info("Shutting down broker...")
        await broker.shutdown()

if __name__ == "__main__":
    asyncio.run(start_broker())