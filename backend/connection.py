from asyncio import Queue, Task
from dataclasses import dataclass

from fastapi import WebSocket
from ollama import AsyncClient

from prompts import InterpretationLevel, base_prompt, level_prompts


@dataclass
class InterpretationRequest:
    client_id: int
    level: InterpretationLevel
    message: str


@dataclass
class InterpretationState:
    level: InterpretationLevel
    last_message: str
    is_in_progress: bool = False


@dataclass
class ConnectedUser:
    websocket: WebSocket
    client_id: int
    interpretations: dict[InterpretationLevel, InterpretationState]
    current_message: str = ""


class ConnectionManager:
    def __init__(self, ollama_client: AsyncClient) -> None:
        self.active_connections: dict[int, ConnectedUser] = {}
        self.ollama_client = ollama_client
        self._client_counter = 0
        self._message_queue: Queue[InterpretationRequest] = Queue()
        self._chat_worker_task = Task(self._chat_worker())

    async def _chat_worker(self):
        while True:
            request = await self._message_queue.get()
            try:
                print(f"Processing message: {request.message} ({request.level})")
                response = await self.ollama_client.chat(
                    model="mistral-small:24b-instruct-2501-q4_K_M",
                    messages=[
                        {
                            "role": "system",
                            "content": base_prompt.format(
                                level_prompt=level_prompts[request.level]
                            ),
                        },
                        {"role": "user", "content": request.message},
                    ],
                )
                interpretation = response.message.content

            except Exception as exc:
                print(f"_chat_worker: {exc}")
                interpretation = None

            await self._interpretation_done_callback(request, interpretation)

    async def _interpretation_done_callback(
        self, request: InterpretationRequest, interpretation: str | None
    ):
        try:
            user = self.active_connections[request.client_id]
            state = user.interpretations[request.level]
            state.is_in_progress = False
            await self._check_user_message_progress(user)
            if interpretation:
                await user.websocket.send_json(
                    {
                        "level": request.level,
                        "message": request.message,
                        "interpretation": interpretation,
                    }
                )

        except Exception as exc:
            print(f"_interpretation_done_callback: {exc}")

    async def connect(self, websocket: WebSocket) -> int:
        await websocket.accept()
        self._client_counter += 1
        initial_interpretations = {
            level: InterpretationState(level, "") for level in InterpretationLevel
        }
        user = ConnectedUser(websocket, self._client_counter, initial_interpretations)
        self.active_connections[user.client_id] = user
        return user.client_id

    def disconnect(self, client_id: int):
        self.active_connections.pop(client_id)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.websocket.send_text(message)

    async def process_message(self, client_id: int, message: str):
        user = self.active_connections[client_id]
        user.current_message = message
        await self._check_user_message_progress(user)

    async def _check_user_message_progress(self, user: ConnectedUser):
        for level in InterpretationLevel:
            state = user.interpretations[level]
            if state.last_message != user.current_message and not state.is_in_progress:
                state.is_in_progress = True
                state.last_message = user.current_message
                await self._message_queue.put(
                    InterpretationRequest(user.client_id, level, user.current_message)
                )
