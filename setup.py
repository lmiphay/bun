# -*- coding: utf-8 -*-

from distutils.core import setup
from distutils.command.install_data import install_data

setup(name='bun',
      version='0.0.1',
      description='bun implementation',
      author='Paul Healy',
      url='https://github.com/lmiphay/bun',
      packages=[
          'bun'
      ],
      install_requires=['invoke'],
      entry_points={
        'console_scripts': ['bun = bun.main:program.run']
      }
)
