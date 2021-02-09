import asyncio
from typing import Callable, Coroutine, Any


class Client(object):
    _reader: asyncio.StreamReader
    _writer: asyncio.StreamWriter

    def __init__(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        self._reader = reader
        self._writer = writer

    async def readline(self) -> str:
        data = await self._reader.readline()
        return data.decode()

    async def writeline(self, message: str):
        self._writer.write(message.encode() + b'\n')
        await self._writer.drain()

    def close(self):
        self._writer.close()


class Server(object):
    _server = asyncio.AbstractServer

    def __init__(self, server: asyncio.AbstractServer):
        self._server = server

    async def run(self):
        async with self._server:
            await self._server.serve_forever()


async def open_connection(host: str, port: int) -> Client:
    reader, writer = await asyncio.open_connection(host=host, port=port)
    return Client(reader, writer)


async def start_server(handler: Callable[[Client], Coroutine[Any, Any, None]], host: str, port: int) -> Server:
    """Запустить сокет сервер и общаться с подключенными клиентамию

    Первый параметр, `handler`, принимает параметр: client. client - это объект Client из данного модуля.
    Этот параметр должен быть сопрограммой.
    """
    async def client_connected_cb(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        await handler(Client(reader=reader, writer=writer))

    return Server(await asyncio.start_server(client_connected_cb, host=host, port=port))
