from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from starlette.responses import FileResponse

router = APIRouter()
other_chatters: list[WebSocket] = []

def profanity_check(msg: str):
    msg = msg[:50]
    return msg.capitalize()

@router.get("/chat")
def chat():
    return FileResponse('public/chat.html')

@router.websocket("/ws/{client_id}")
async def chat_ws_endpoint(websocket: WebSocket, client_id: int):
    """The school chat websocket endpoint, it handles the chat data traffic

    Args:
        websocket (WebSocket): represents the current user/chatter websocket, we can use it to interact only the user.
    """
    await websocket.accept()
    other_chatters.append(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            data  = profanity_check(data)
            await websocket.send_text(f"You: {data}")
            for chatter in other_chatters:
                if chatter != websocket:
                    await chatter.send_text(f"{client_id}: {data}")
    except WebSocketDisconnect:
        other_chatters.remove(websocket)
        for chatter in other_chatters:
                if chatter != websocket:
                    await chatter.send_text(f"User {client_id} has left")