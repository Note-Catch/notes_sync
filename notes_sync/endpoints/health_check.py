from aiokafka import AIOKafkaProducer, errors
from fastapi import APIRouter, Depends, Response, status

from notes_sync.broker import Producer
from notes_sync.dependencies import admin_basic_auth
from notes_sync.schemas import PingResponse

api_router = APIRouter(tags=["Health check"])


@api_router.get(
    "/health_check/ping",
    summary="API server health check",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_basic_auth)],
)
async def health_check():
    return PingResponse()


@api_router.get(
    "/health_check/broker",
    summary="Message broker health check",
    response_model=PingResponse,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(admin_basic_auth)],
)
async def health_check_broker(producer: AIOKafkaProducer = Depends(Producer.get)):
    try:
        await producer.send_and_wait("health_check", b"Ping!")
        return PingResponse()
    except errors.KafkaTimeoutError:
        return Response(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
