import json
import logging
import os
import sys

import asyncio

import configs
from application import Application
from wrappers import logger

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config.json')


def main():
    if not os.path.isfile(CONFIG_FILE):
        sys.stderr.write(f'File "{CONFIG_FILE}" - missing')
        exit(1)

    with open(CONFIG_FILE) as fin:
        config = json.load(fin)

    try:
        config = configs.load_config(config)
    except KeyError as e:
        sys.stderr.write(f'Parameter {str(e)} is missing in the file, see "default_config.json"')
        exit(1)

    logger.create(config.log_file, logging.INFO)

    application = Application(config, os.getenv('DATABASE_PASSWORD'))
    asyncio.run(application.run())


if __name__ == '__main__':
    main()
