from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, content: str, origin: WebSocket):
        for connection in self.active_connections:
            if connection is not origin:
                await connection.send_text(content)


manager = ConnectionManager()


@app.websocket("/")
async def connect(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            content = await websocket.receive_text()
            print(f"GOT: {content}")
            await manager.broadcast(content, websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
