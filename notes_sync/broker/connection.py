from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from contextlib import asynccontextmanager

from notes_sync.config import get_settings


class ProducerManager:
    """
    A class that implements the necessary functionality for working with the message broker
    """

    def __init__(self) -> None:
        self.refresh()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ProducerManager, cls).__new__(cls)
        return cls.instance

    def get_producer(self) -> AIOKafkaProducer:
        return self.producer

    def refresh(self) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=get_settings().broker_uri)


class ConsumerManager:
    """
    A class that implements the necessary functionality for working with the message broker
    """

    def __init__(self) -> None:
        self.consumers = dict()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConsumerManager, cls).__new__(cls)
        return cls.instance

    def get_consumer(self, topic: str) -> AIOKafkaConsumer:
        if topic not in self.consumers:
            self.refresh(topic)
        return self.consumers[topic]

    def refresh(self, topic: str) -> None:
        self.consumers[topic] = AIOKafkaConsumer(
            topic,
            bootstrap_servers=get_settings().broker_uri,
            auto_offset_reset="earliest",
            enable_auto_commit=True,
        )


class Producer:
    async def get() -> AIOKafkaProducer:
        producer = ProducerManager().get_producer()
        try:
            await producer.start()
            yield producer
        finally:
            await producer.stop()

    __call__ = asynccontextmanager(get)


class Consumer:
    @asynccontextmanager
    async def get(topic: str) -> AIOKafkaConsumer:
        consumer = ConsumerManager().get_consumer(topic)
        try:
            await consumer.start()
            yield consumer
        finally:
            await consumer.stop()
