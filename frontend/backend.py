# backend.py
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import random
from typing import List

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, room_code: str):
        await websocket.accept()
        self.active_connections.append((room_code, websocket))

    def disconnect(self, websocket: WebSocket):
        self.active_connections = [(room_code, ws) for room_code, ws in self.active_connections if ws != websocket]

    async def broadcast(self, room_code: str, message: str):
        for code, connection in self.active_connections:
            if code == room_code:
                await connection.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_code}")
async def websocket_endpoint(websocket: WebSocket, room_code: str):
    await manager.connect(websocket, room_code)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(room_code, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
