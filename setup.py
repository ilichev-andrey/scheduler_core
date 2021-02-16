import os
from typing import List

from setuptools import setup

import scheduler_core


def package_files(directory: str) -> List[str]:
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


def get_install_requires(file: str) -> List[str]:
    if not os.path.isfile(file):
        return []

    with open(file, 'r', encoding='utf-8') as fin:
        data = fin.read()

    return [item.strip() for item in data.split('\n')]


def get_long_description(file: str) -> str:
    with open(file, 'r', encoding='utf-8') as fin:
        return fin.read()


setup(
    name='scheduler-core',
    packages=['scheduler_core', 'wrappers'],
    package_data={
        'scheduler_core': package_files('scheduler_core'),
        'wrappers': package_files('wrappers')
    },
    version=scheduler_core.__version__,
    license='MIT',
    description='SchedulerCore this is one of the project modules for automating customer records.',
    long_description=get_long_description('README.md'),
    long_description_content_type="text/markdown",
    author='Ilichev Andrey',
    author_email='ilichev.andrey.y@gmail.com',
    url='https://github.com/ilichev-andrey/scheduler_core.git',
    keywords=[],
    install_requires=get_install_requires('requirements.txt'),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9'
    ]
)
