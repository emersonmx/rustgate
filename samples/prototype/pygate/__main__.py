import asyncio
from pprint import pprint

import uvicorn
from httpx import AsyncClient

from .app import Application

http_client = AsyncClient()


async def shutdown_lifespan():
    await http_client.aclose()


async def router(scope, receive, send):
    data = await receive()
    pprint(scope)
    pprint(data)
    await send({
        "type": "http.response.start",
        "status": 200,
        "headers": [
            [b"content-type", b"text/plain"],
        ],
    })

    await send({
        "type": "http.response.body",
        "body": b"Hello World!",
    })


def create_app():
    app = Application()
    app.shutdown_lifespan = shutdown_lifespan
    app.router = router

    return app


async def main() -> int:
    config = uvicorn.Config(create_app(), log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
