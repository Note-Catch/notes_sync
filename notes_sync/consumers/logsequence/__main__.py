import asyncio
import json

import uvicorn
from fastapi import FastAPI, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy import delete
from sqlalchemy.orm import Session

from notes_sync.config import get_settings
from notes_sync.broker import Consumer
from notes_sync.database.connection import get_db
from notes_sync.database.models import LogsequenceMessage, User
from notes_sync.utils import get_hostname, row2dict, decode_access_token

from .connection import ConnectionManager


def get_app() -> FastAPI:
    """
    Creates application and all dependable objects.
    """

    async def lifespan(app: FastAPI):
        # Pre-FastAPI actions
        asyncio.create_task(transmit_messages())
        # Pass control to FastAPI
        yield None
        # Shutdown

    application = FastAPI(lifespan=lifespan)
    return application


app = get_app()
manager = ConnectionManager()


@app.websocket("/ws/{token}")
async def accept_connection(
    token: str, websocket: WebSocket, db: Session = Depends(get_db)
):
    username: str = decode_access_token(token).get("sub")
    if username is None:
        return

    await manager.connect(token, websocket)

    # Check if there messages for user with the given token, if there're some
    # Then trasmit it to the user
    messages = db.query(User).where(User.username == username).scalars()
    messages = [row2dict(message) for message in messages]
    ids = [messages["id"] for message in messages]
    try:
        await manager.send_json(websocket, {"messages": messages})
    except WebSocketDisconnect:
        # It's okay, then we'll send messages the next time
        return

    # It's essential to delete by ids not by token, cause there may be changes
    # between retrieval and deletion
    query = delete(LogsequenceMessage).where(LogsequenceMessage.id.in_(ids))
    db.execute(query)
    db.commit()


async def transmit_messages():
    def store_message(db: Session, message):
        new_message = LogsequenceMessage(**message)
        db.add(new_message)
        db.commit()

    with get_db() as db:
        async with Consumer.get("logsequence") as consumer:
            for message in consumer:
                # If user with token is online, then transmit message
                # Else store it in the database

                message = json.loads(message)
                connection = manager.get(message["token"])

                try:
                    if connection is not None:
                        await manager.send_json(connection, message)
                        # Skip store_messages call
                        continue
                except WebSocketDisconnect:
                    # Fall to store_messages call
                    pass

                store_message(db, message)


if __name__ == "__main__":
    settings = get_settings()
    uvicorn.run(
        "notes_sync.consumers.logsequence.__main__:app",
        host=get_hostname(settings.LOGSEQUENCE_CONSUMER_HOST),
        port=settings.LOGSEQUENCE_CONSUMER_PORT,
        reload=True,
    )
