import asyncio
import json
from typing import Callable, Coroutine, Any, Dict

from scheduler_core.command_responses import responses_factory

from scheduler_core import exceptions
from scheduler_core.command_responses.command_response import CommandResponse
from scheduler_core.commands.command import Command
from scheduler_core.enums import CommandType
from wrappers import LoggerWrap


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
    """Запустить сокет сервер и общаться с подключенными клиентами

    Первый параметр, `handler`, принимает параметр: client. client - это объект Client из данного модуля.
    Этот параметр должен быть сопрограммой.
    """
    async def client_connected_cb(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        await handler(Client(reader=reader, writer=writer))

    return Server(await asyncio.start_server(client_connected_cb, host=host, port=port))


def __load_response(data: Dict) -> CommandResponse:
    """
    :raises
        UnknownCommand если получен результат неизвестной команды
        InvalidFormatCommand если не удалось загрузить ответ команды
    """

    if 'type' not in data:
        raise exceptions.InvalidFormatCommandResponse(f'Не найден параметр "type" в данных: {data}')

    response = responses_factory.create(CommandType(data['type']))
    if not response.load_from_dict(data):
        raise exceptions.InvalidFormatCommandResponse(f'Не удалось загрузить ответ команды, данные: {data}')

    LoggerWrap().get_logger().info(f'Ответ команды обработан: {response}')
    return response


async def send_command(command: Command, host: str, port: int) -> CommandResponse:
    """
    :raises
        UnknownCommand если получен результат неизвестной команды
        InvalidFormatCommand если не удалось загрузить ответ команды
    """

    client = await open_connection(host=host, port=port)
    data = json.dumps(command.to_dict())
    await client.writeline(data)
    LoggerWrap().get_logger().info(f'Отправлена команда: {data}')

    data = await client.readline()
    LoggerWrap().get_logger().info(f'Получен ответ: {data}')
    client.close()

    return __load_response(json.loads(data))
