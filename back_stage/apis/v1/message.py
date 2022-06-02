# -*- coding: utf-8 -*-

from back_stage import *

@router.websocket(path='/message.io')
async def message_io(websocket: WebSocket, token: str):

    await manager.connect(websocket)
    await manager.broadcast(f'OK')

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"你说了: {data}", websocket)

    except WebSocketDisconnect as e:
        log.log_error(e)
        manager.disconnect(websocket)
        await manager.broadcast(f'用户离开')