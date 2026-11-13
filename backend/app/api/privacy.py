"""Bound request bodies before JSON validation; never echo request validation values."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

from app.domain.models import MAX_REQUEST_BYTES


class PrivateIntakeMiddleware:
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        headers = dict(scope.get("headers", []))
        length = headers.get(b"content-length")
        if length:
            try:
                if int(length) > MAX_REQUEST_BYTES:
                    await self.reject(scope, receive, send)
                    return
            except ValueError:
                await JSONResponse({"detail": "Invalid request headers."}, status_code=400,
                                   headers={"Cache-Control": "no-store"})(scope, receive, send)
                return
        # Bound and buffer BEFORE FastAPI's JSON error handler can catch receive exceptions.
        body = bytearray()
        while True:
            message = await receive()
            if message["type"] == "http.disconnect":
                return
            chunk = message.get("body", b"")
            if len(body) + len(chunk) > MAX_REQUEST_BYTES:
                await self.reject(scope, receive, send)
                return
            body.extend(chunk)
            if not message.get("more_body", False):
                break
        delivered = False

        async def bounded_receive() -> Message:
            nonlocal delivered
            if not delivered:
                delivered = True
                return {"type": "http.request", "body": bytes(body), "more_body": False}
            return await receive()

        async def private_send(message: Message) -> None:
            if message["type"] == "http.response.start":
                response_headers = message.setdefault("headers", [])
                if not any(key.lower() == b"cache-control" for key, _ in response_headers):
                    response_headers.append((b"cache-control", b"no-store"))
                response_headers.append((b"x-content-type-options", b"nosniff"))
            await send(message)

        await self.app(scope, bounded_receive, private_send)

    @staticmethod
    async def reject(scope: Scope, receive: Receive, send: Send) -> None:
        await JSONResponse({"detail": "Request exceeds the 1 MiB engineering limit."}, status_code=413,
                           headers={"Cache-Control": "no-store"})(scope, receive, send)


async def private_validation_error(_request: Request, _exception: RequestValidationError) -> JSONResponse:
    # FastAPI/Pydantic defaults can echo raw input, unknown keys, or invalid JSON in error details.
    return JSONResponse(status_code=422, content={"detail": "Invalid parse request. Check text length, metadata fields, and synthetic-data confirmation."},
                        headers={"Cache-Control": "no-store"})
