from fastapi import APIRouter, WebSocket

router = APIRouter()

@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()

    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"You said: {data}")
