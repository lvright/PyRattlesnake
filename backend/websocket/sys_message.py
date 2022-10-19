# -*- coding: utf-8 -*-

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from utils.socket_msg import ConnectionManager

manager = ConnectionManager()

router = APIRouter()

@router.websocket(path="/message.io/{token}")
async def sys_message_server(websocket: WebSocket, token: str):
    await manager.connect(websocket)
    await manager.broadcast(f"用户进入消息室")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"发送消息: {data}", websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"用户离线")