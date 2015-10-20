# -*- coding: utf-8 -*-
import os
import codecs

from setuptools import find_packages, setup


def read(*rnames):
    return codecs.open(os.path.join(os.path.dirname(__file__), *rnames), encoding='utf-8').read()


setup(
    name='zerg',
    version='0.0.1',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    include_package_data=True,
    # entry_points={
    # 'console_scripts': [
    # 'saika=saika.scripts.manage:main',
    # ]
    # },
    zip_safe=False,
    url='https://github.com/Mohanson/zerg',
    license='',
    author='Mohanson',
    author_email='mohanson@outlook.com',
    description='zerg',
    long_description=read('README.md'),
    install_requires=['jinja2==2.8', 'saika==0.3.8', 'Markdown==2.6.2', 'ndict.py==1.0.2'],
)