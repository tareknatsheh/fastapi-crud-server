from fastapi import APIRouter, WebSocket

router = APIRouter()

other_chatters: list[WebSocket] = []

@router.websocket("/chat")
async def chat(websocket: WebSocket):
    await websocket.accept()
    other_chatters.append(websocket)

    while True:
        data = await websocket.receive_text()

        for chatter in other_chatters:
            if chatter != websocket:
                await chatter.send_text(f"someone said {data}")
