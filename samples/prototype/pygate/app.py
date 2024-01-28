class UnhandledScopeTypeError(Exception):
    pass


class Application:
    @staticmethod
    async def _null_lifespan():
        pass

    @staticmethod
    async def _null_http_router(scope, receive, send):
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

    def __init__(self) -> None:
        self.startup_lifespan = self._null_lifespan
        self.shutdown_lifespan = self._null_lifespan
        self.router = self._null_http_router

    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            await self.router(scope, receive, send)
        elif scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        else:
            raise UnhandledScopeTypeError

    async def _handle_lifespan(self, scope, receive, send):
        while True:
            message = await receive()

            type_ = message["type"]
            if type_ == "lifespan.startup":
                await self.startup_lifespan()
                await send({"type": f"{type_}.complete"})
            elif type_ == "lifespan.shutdown":
                await self.shutdown_lifespan()
                await send({"type": f"{type_}.complete"})
