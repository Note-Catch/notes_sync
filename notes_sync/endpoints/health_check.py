from aiokafka import AIOKafkaProducer, errors
from fastapi import APIRouter, Depends

from notes_sync.broker import Producer
from notes_sync.dependencies import admin_basic_auth
from notes_sync.schemas import PingResponse, BrokerNotResponding

api_router = APIRouter(prefix="/health_check", tags=["Health check"])


@api_router.get(
    "/ping",
    summary="API server health check",
    responses={PingResponse.status_code(): {"model": PingResponse}},
    dependencies=[Depends(admin_basic_auth)],
)
async def health_check() -> PingResponse:
    return PingResponse()


@api_router.get(
    "/broker",
    summary="Message broker health check",
    responses={
        PingResponse.status_code(): {"model": PingResponse},
        BrokerNotResponding.status_code(): {"model": BrokerNotResponding},
    },
    dependencies=[Depends(admin_basic_auth)],
)
async def health_check_broker(
    producer: AIOKafkaProducer = Depends(Producer.get),
) -> PingResponse | BrokerNotResponding:
    try:
        await producer.send_and_wait("health_check", b"Ping!")
        return PingResponse()
    except errors.KafkaTimeoutError:
        return BrokerNotResponding()
