# -*- coding: utf-8 -*-

import os
import codecs

from setuptools import find_packages, setup


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames)).read()


setup(
    name='zerg',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,

    url='https://github.com/Mohanson/zerg',
    license='',
    author='Mohanson',
    author_email='mohanson@outlook.com',
    description='zerg',
    long_description=read('README.md'),
    install_requires=['Markdown==2.6.2', 'Jinja2==2.8', 'beautifulsoup4==4.4.0', 'Pygments==2.0.2'],
)