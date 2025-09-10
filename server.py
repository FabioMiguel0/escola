import os
import threading
import asyncio
import importlib
import httpx
import websockets
from fastapi import FastAPI, Request, Response, WebSocket
import uvicorn
import time

FLET_PORT = 10001
FLET_HOST = "127.0.0.1"
main_module = importlib.import_module("main")

def start_flet():
    import flet as ft
    print(f"[FLET] starting internal Flet on {FLET_HOST}:{FLET_PORT}")
    try:
        ft.app(target=main_module.main, view=ft.WEB_BROWSER, port=FLET_PORT)
    except Exception as e:
        print(f"[FLET] exception: {e}")

t = threading.Thread(target=start_flet, daemon=True)
t.start()

# wait a bit for Flet to start
time.sleep(1)

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.api_route("/{path:path}", methods=["GET","POST","PUT","DELETE","PATCH","OPTIONS","HEAD"])
async def proxy(request: Request, path: str):
    backend_url = f"http://{FLET_HOST}:{FLET_PORT}/{path}"
    params = dict(request.query_params)
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host","accept-encoding","connection")}
    body = await request.body()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(request.method, backend_url, params=params, headers=headers, content=body, timeout=15.0)
        except Exception as e:
            print(f"[PROXY] HTTP request error: {e}")
            return Response(content="Bad Gateway", status_code=502)
    excluded = {"content-encoding","transfer-encoding","connection","keep-alive"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers, media_type=resp.headers.get("content-type"))

@app.websocket("/{path:path}")
async def websocket_proxy(websocket: WebSocket, path: str):
    await websocket.accept()
    backend_ws = f"ws://{FLET_HOST}:{FLET_PORT}/{path}"
    try:
        async with websockets.connect(backend_ws) as ws_backend:
            async def client_to_backend():
                try:
                    while True:
                        msg = await websocket.receive_text()
                        await ws_backend.send(msg)
                except Exception:
                    pass
            async def backend_to_client():
                try:
                    async for message in ws_backend:
                        await websocket.send_text(message)
                except Exception:
                    pass
            await asyncio.wait([asyncio.create_task(client_to_backend()), asyncio.create_task(backend_to_client())], return_when=asyncio.FIRST_COMPLETED)
    except Exception as e:
        print(f"[WS PROXY] error connecting to backend ws: {e}")
        await websocket.close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"[PROXY] starting on 0.0.0.0:{port} -> internal Flet {FLET_HOST}:{FLET_PORT}")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")