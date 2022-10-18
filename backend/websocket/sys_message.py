# -*- coding: utf-8 -*-

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core import check_jwt_token
from backend.apis.deps import get_db
from utils.socket_msg import ConnectionManager
from backend.crud.message import getMessage

router = APIRouter()

manager = ConnectionManager()

@router.websocket(path="/message.io")
async def sys_message_io(
        websocket: WebSocket,
        token: str = Depends(check_jwt_token),
        db: AsyncSession = Depends(get_db),
):
    result = await getMessage.get_first(db)
    data = {"event": "get_unread_message", "message": "你有一条新的消息", "data": result}
    await manager.connect(websocket)
    await manager.broadcast(data)
    try:
        while True:
            get_msg = await websocket.receive_text()
            await manager.send_personal_message(data, websocket)
            await manager.broadcast(data)
    except WebSocketDisconnect as e:
        manager.disconnect(websocket)
        await manager.broadcast('账户登出')