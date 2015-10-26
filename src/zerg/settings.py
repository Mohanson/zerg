# -*- coding: utf-8 -*-

import logging
import sys
import os

import jinja2


DEGUB = True
RECUR_DEEP = 3


class DIR:
    def __init__(self, path):
        self.path = path

    def join(self, *args):
        return DIR(os.path.join(self.path, *args))


project = DIR(os.path.dirname(__file__))

logger = logging.getLogger('zerg')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

loader = jinja2.FileSystemLoader(project.join('templates').path)
jinja_env = jinja2.Environment(loader=loader)

__all__ = ['DEBUG', 'RECUR_DEEP', 'project', 'logger', 'jinja_env']