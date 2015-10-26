# -*- coding: utf-8 -*-

import logging
import sys
import pathlib

import jinja2

project = pathlib.Path(__file__).parent

logger = logging.getLogger('zerg')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

loader = jinja2.FileSystemLoader(project.joinpath('templates').__str__())
jinja_env = jinja2.Environment(loader=loader)

__all__ = ['project', 'logger', 'jinja_env']