import json
import logging
import os
import sys

import asyncio

from scheduler_core import configs
from scheduler_core.application import Application
from wrappers import logger

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def main():
    try:
        config = configs.load(CONFIG_FILE)
    except KeyError as e:
        sys.stderr.write(f'Parameter {str(e)} is missing, see "README.md"')
        return False
    except ValueError as e:
        sys.stderr.write(f'{str(e)}. Invalid parameter, see "README.md"')
        return False

    logger.create(config.log_file, logging.INFO)

    application = Application(config)
    asyncio.run(application.run())
    return True


if __name__ == '__main__':
    exit(not main())
