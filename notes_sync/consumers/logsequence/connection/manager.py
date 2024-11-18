from bidict import bidict
from fastapi import WebSocket, WebSocketDisconnect


class ConnectionManager:
    """
    A class that implements the necessary functionality for working with WebSocket connection
    """

    def __init__(self):
        self.active_connections: dict[str, WebSocket] = bidict()

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
        return cls.instance

    async def connect(self, token: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[token] = websocket

    def __remove(self, websocket: WebSocket):
        token = self.active_connections.inverse(websocket)
        del self.active_connections[token]

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.__remove(websocket)

    def get(self, token: str):
        return self.active_connections.get(token, None)

    async def receive_json(self, websocket: WebSocket):
        try:
            message = await websocket.receive_json(websocket)
            return message
        except WebSocketDisconnect:
            self.remove(websocket)
            raise

    async def send_json(self, websocket: WebSocket, message: object):
        try:
            await websocket.send_json(message)
        except WebSocketDisconnect:
            self.remove(websocket)
            raise

    async def broadcast(self, message: object):
        deletion_list: list[WebSocket] = []
        for connection in self.active_connections.values():
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                deletion_list.append(connection)
        for connection in deletion_list:
            self.remove(connection)
        if deletion_list:
            raise WebSocketDisconnect()
