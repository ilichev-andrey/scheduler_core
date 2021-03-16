import json
import logging
import os
import sys

import asyncio

from scheduler_core import configs
from scheduler_core.application import Application
from wrappers import logger

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def error(message: str):
    sys.stderr.write(f'{message}\n')


def main():
    try:
        config = configs.load(CONFIG_FILE)
    except KeyError as e:
        error(f'Parameter {str(e)} is missing, see "README.md"')
        return False
    except ValueError as e:
        error(f'{str(e)}. Invalid parameter, see "README.md"')
        return False

    logger.create(config.log_file, logging.INFO)

    application = Application(config)
    asyncio.run(application.run())
    return True


if __name__ == '__main__':
    exit(not main())
