# -*- coding: utf-8 -*-

import logging
import sys

import jinja2

import saika.path


# DEFINE
DEGUB = True
RECUR_DEEP = 3

# PROJECT
project = saika.path.File(__file__).parents[1]

# LOGGER
logger = logging.getLogger('zerg')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

# JINJA2 ENV
loader = jinja2.FileSystemLoader(project.join('templates').path)
jinja_env = jinja2.Environment(loader=loader)

__all__ = ['DEBUG', 'RECUR_DEEP', 'project', 'logger', 'jinja_env']