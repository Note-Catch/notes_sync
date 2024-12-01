import json

from aiokafka import AIOKafkaProducer
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from notes_sync.broker import Producer
from notes_sync import schemas
from notes_sync.database.models import User
from notes_sync.database.connection import get_db
from notes_sync.dependencies import oauth2


api_router = APIRouter(prefix="/messages", tags=["Messages"])


@api_router.post(
    "/post",
    responses={
        schemas.EmptyOkResponse.status_code(): {"model": schemas.EmptyOkResponse}
    },
    dependencies=[Depends(oauth2)],
)
async def post_message(
    request: schemas.MessagePostRequest,
    user: User = Depends(oauth2),
    producer: AIOKafkaProducer = Depends(Producer.get),
    db: Session = Depends(get_db),
) -> schemas.EmptyOkResponse:
    if user.logsequence_enable:
        await producer.send_and_wait(
            "logsequence",
            json.dumps({"user": user.id, "text": request.text}).encode("utf-8"),
        )
    return schemas.EmptyOkResponse()
