class HTTPError(Exception):
    def __init__(self, status_code: int, detail: str = "") -> None:
        self.status_code = status_code
        self.detail = detail


async def app(scope, receive, send):
    if scope["type"] == "http":
        await _handle_http(scope, receive, send)
    elif scope["type"] == "lifespan":
        await _handle_lifespan(scope, receive, send)
    else:
        msg = "Wrong type"
        raise HTTPError(500, msg)


async def _handle_http(_scope, _receive, send):
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


async def _handle_lifespan(_scope, receive, send):
    while True:
        message = await receive()
        if message["type"] == "lifespan.startup":
            await send({"type": "lifespan.startup.complete"})
        elif message["type"] == "lifespan.shutdown":
            await send({"type": "lifespan.shutdown.complete"})
            return
