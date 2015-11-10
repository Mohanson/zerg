# -*- coding: utf-8 -*-

import logging
import sys
import pathlib

import jinja2


MODULE_DIR = pathlib.Path(__file__).parent

LOGGER = logging.getLogger('zerg')
LOGGER.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

LOGGER.addHandler(stream_handler)

loader = jinja2.FileSystemLoader(MODULE_DIR.joinpath('templates').__str__())
JINJA_ENV = jinja2.Environment(loader=loader)