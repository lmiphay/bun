# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='bun',
      version='0.0.1',
      description='bun implementation',
      license='GPL-2',
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
