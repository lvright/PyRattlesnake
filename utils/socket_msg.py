# -*- coding: utf-8 -*-

from fastapi import WebSocket, WebSocketDisconnect
from typing import List

class ConnectionManager:

    def __init__(self):
        # 存放激活的ws连接对象
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        # 等待连接
        await ws.accept()
        # 存储ws连接对象
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        # 关闭时 移除ws对象
        self.active_connections.remove(ws)

    @staticmethod
    async def send_personal_message(message, ws: WebSocket):
        # 发送个人消息
        if isinstance(message, str): await ws.send_text(message)

        if isinstance(message, dict): await ws.send_json(message)

        if isinstance(message, bytes): await ws.send_bytes(message)

    async def broadcast(self, message):
        # 广播消息
        for connection in self.active_connections:

            if isinstance(message, str): await connection.send_text(message)

            if isinstance(message, dict): await connection.send_json(message)

            if isinstance(message, bytes): await connection.send_bytes(message)