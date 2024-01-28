from collections.abc import Callable, Coroutine
from typing import Any, Literal, Optional, TypedDict


class UnhandledScopeTypeError(Exception):
    pass


class Scope(TypedDict):
    type: Literal["http", "lifespan"]


Receiver = Callable[[], Coroutine[Any, Any, dict[str, Any]]]
Sender = Callable[[dict[str, Any]], Coroutine[Any, Any, None]]


class Application:
    @staticmethod
    async def _null_lifespan() -> None:
        pass

    @staticmethod
    async def _null_http_router(
        _scope: Scope,
        _receive: Receiver,
        send: Sender,
    ) -> None:
        await send({
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/plain"),
            ],
        })

        await send({
            "type": "http.response.body",
            "body": b"Hello World!",
        })

    def __init__(
        self,
        startup_lifespan: Optional[
            Callable[[], Coroutine[Any, Any, None]]
        ] = None,
        shutdown_lifespan: Optional[
            Callable[[], Coroutine[Any, Any, None]]
        ] = None,
        router: Optional[
            Callable[[Scope, Receiver, Sender], Coroutine[Any, Any, None]]
        ] = None,
    ) -> None:
        self.startup_lifespan = startup_lifespan or self._null_lifespan
        self.shutdown_lifespan = shutdown_lifespan or self._null_lifespan
        self.router = router or self._null_http_router

    async def __call__(self, scope: Scope, receive, send) -> None:
        if scope["type"] == "http":
            await self.router(scope, receive, send)
        elif scope["type"] == "lifespan":
            await self._handle_lifespan(scope, receive, send)
        else:
            raise UnhandledScopeTypeError

    async def _handle_lifespan(self, _scope: Scope, receive, send) -> None:
        while True:
            message = await receive()

            type_ = message["type"]
            if type_ == "lifespan.startup":
                await self.startup_lifespan()
                await send({"type": f"{type_}.complete"})
            elif type_ == "lifespan.shutdown":
                await self.shutdown_lifespan()
                await send({"type": f"{type_}.complete"})
