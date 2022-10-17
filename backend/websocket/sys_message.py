# -*- coding: utf-8 -*-

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core import check_jwt_token
from backend.apis.deps import get_db

router = APIRouter()

@router.websocket(path="/message.io/{token}")
async def websocket_endpoint(websocket: WebSocket, db: AsyncSession = Depends(get_db), token: str = Depends(check_jwt_token)):
    await websocket.accept()
    while True:
        # 接收
        data = await websocket.receive_text()
        # 发送
        await websocket.send_text(f"接收到文本: {data}")