from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from ollama import AsyncClient

from connection import ConnectionManager

app = FastAPI()
api = FastAPI()

client = AsyncClient(
    host="http://gpu.lan:11434",
)

manager = ConnectionManager(client)


@api.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    client_id = await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = data[:256].strip()
            if data:
                await manager.process_message(client_id, data)

    except WebSocketDisconnect:
        manager.disconnect(client_id)


app.mount("/api", api)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
