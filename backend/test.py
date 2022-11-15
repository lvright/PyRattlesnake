import websocket

ws = websocket.WebSocket()

ws.connect("ws://127.0.0.1", http_proxy_host="test", http_proxy_port=8086)