import asyncio
import json
from typing import Dict

import exceptions
import net
from command_executors import executors_factory
from command_responses.error_response import ErrorResponse
from commands import commands_factory
from commands.command import Command
from configs import Config
from database.db import DB
from enums import CommandType
from net import Client
from wrappers import LoggerWrap


class Application(object):
    _config = Config
    _db = DB

    def __init__(self, config: Config, database_password: str):
        self._config = config
        self._db = DB(config.database, password=database_password)

    async def run(self):
        await asyncio.gather(
            asyncio.ensure_future(self._run_server())
        )

    async def _run_server(self):
        server_config = self._config.server
        server = await net.start_server(handler=self._handle_data, host=server_config.host, port=server_config.port)
        await server.run()

    async def _handle_data(self, client: Client):
        data = await self._read_data(client)
        await self._execute_command(data, client)

    @staticmethod
    async def _read_data(client: Client) -> Dict:
        """
        :raises
            JSONDecodeError если полученная команда не в формате JSON
        """
        data = await client.readline()
        try:
            return json.loads(data)
        except json.JSONDecodeError as e:
            LoggerWrap().get_logger().exception(str(e))
            raise

    async def _execute_command(self, command_data: Dict, client: Client):
        try:
            command = self._handle_command(command_data)
            executor = executors_factory.create(command.get_type(), self._db)
        except exceptions.CommandException as e:
            LoggerWrap().get_logger().exception(str(e))
            return

        try:
            response = await executor.execute(command)
        except Exception as e:
            LoggerWrap().get_logger().exception(str(e))
            response = ErrorResponse(command_id=command.id, command_type=command.get_type())

        await client.writeline(json.dumps(response.to_dict()))

    @staticmethod
    def _handle_command(data: Dict) -> Command:
        """
        :raises
            UnknownCommand если получена неизвестная команда
            InvalidFormatCommand если не удалось загрузить команду
        """

        if 'type' not in data:
            raise exceptions.InvalidFormatCommand(f'Не найден параметр "type" в данных: {data}')

        command = commands_factory.create(CommandType(data['type']))
        if not command.load_from_dict(data):
            raise exceptions.InvalidFormatCommand(f'Не удалось загрузить команду, данные: {data}')

        LoggerWrap().get_logger().info(f'Команда обработана: {command}')
        return command
