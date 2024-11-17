from aiokafka import AIOKafkaProducer

from notes_sync.config import get_settings


class BrokerManager:
    """
    A class that implements the necessary functionality for working with the message broker
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(BrokerManager, cls).__new__(cls)
        return cls.instance

    def get_producer(self) -> AIOKafkaProducer:
        return self.producer

    def refresh(self) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=get_settings().broker_uri)


async def get_producer() -> AIOKafkaProducer:
    producer = BrokerManager().get_producer()
    await producer.start()
    try:
        yield producer
    finally:
        await producer.stop()
