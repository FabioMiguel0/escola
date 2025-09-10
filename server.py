import os
import threading
import asyncio
import importlib
import httpx
import websockets
from fastapi import FastAPI, Request, Response, WebSocket
import uvicorn

# porta onde o Flet vai rodar internamente
FLET_PORT = 10001

# importa a função main(page) do seu main.py (certifique-se que main.py define `def main(page: ft.Page): ...`)
main_module = importlib.import_module("main")

def start_flet():
    import flet as ft
    print(f"Starting internal Flet on port {FLET_PORT}")
    # inicia Flet como servidor web na porta interna
    ft.app(target=main_module.main, view=ft.WEB_BROWSER, port=FLET_PORT)

# start Flet em thread separada para não bloquear o FastAPI loop
t = threading.Thread(target=start_flet, daemon=True)
t.start()

app = FastAPI()

# proxy HTTP (GET/POST/PUT/...); encaminha requisições para o Flet interno
@app.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"])
async def proxy(request: Request, path: str):
    backend_url = f"http://127.0.0.1:{FLET_PORT}/{path}"
    # preserva query params
    params = dict(request.query_params)
    # filtra headers que não devem ser repassados
    headers = {k: v for k, v in request.headers.items() if k.lower() not in ("host", "content-length", "accept-encoding", "connection")}
    body = await request.body()
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(request.method, backend_url, params=params, headers=headers, content=body, timeout=30.0)
        except httpx.RequestError as e:
            return Response(content=f"Error proxying request: {e}", status_code=502)
    # remove hop-by-hop headers antes de retornar
    excluded = {"content-encoding", "transfer-encoding", "connection", "keep-alive"}
    response_headers = {k: v for k, v in resp.headers.items() if k.lower() not in excluded}
    return Response(content=resp.content, status_code=resp.status_code, headers=response_headers, media_type=resp.headers.get("content-type"))

# proxy WebSocket — encaminha mensagens entre cliente e Flet interno
@app.websocket("/{path:path}")
async def websocket_proxy(websocket: WebSocket, path: str):
    await websocket.accept()
    qs = websocket.query_params
    query = ""
    if qs:
        query = "?" + "&".join([f"{k}={v}" for k, v in qs.multi_items()])
    backend_ws_url = f"ws://127.0.0.1:{FLET_PORT}/{path}{query}"

    async def forward_client_to_backend(ws_client, ws_backend):
        try:
            while True:
                msg = await ws_client.receive_text()
                await ws_backend.send(msg)
        except Exception:
            try:
                await ws_backend.close()
            except Exception:
                pass

    async def forward_backend_to_client(ws_client, ws_backend):
        try:
            async for message in ws_backend:
                await ws_client.send_text(message)
        except Exception:
            try:
                await ws_client.close()
            except Exception:
                pass

    try:
        async with websockets.connect(backend_ws_url) as ws_backend:
            task1 = asyncio.create_task(forward_client_to_backend(websocket, ws_backend))
            task2 = asyncio.create_task(forward_backend_to_client(websocket, ws_backend))
            await asyncio.wait([task1, task2], return_when=asyncio.FIRST_COMPLETED)
    except Exception as e:
        # backend WS não disponível
        await websocket.close()
        return

if __name__ == "__main__":
    # porta que o Render decide; fallback 10000
    port = int(os.environ.get("PORT", 10000))
    print(f"Starting proxy server on 0.0.0.0:{port} (forwarding to internal Flet:{FLET_PORT})")
    uvicorn.run(app, host="0.0.0.0", port=port)