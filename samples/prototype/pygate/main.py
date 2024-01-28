from pprint import pprint

from httpx import AsyncClient

from .app import Application

http_client = AsyncClient()


async def shutdown_lifespan():
    await http_client.aclose()


async def router(scope, receive, send):
    data = await receive()
    pprint(scope)
    pprint(data)
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/plain"],
            ],
        }
    )

    await send(
        {
            "type": "http.response.body",
            "body": b"Hello World!",
        }
    )


app = Application()
app.shutdown_lifespan = shutdown_lifespan
app.router = router
