# -*- coding: utf-8 -*-

from setuptools import setup

setup(name='bun',
      version='0.1.0',
      description='bun implementation',
      license='GPL-2',
      author='Paul Healy',
      url='https://github.com/lmiphay/bun',
      packages=[
          'bun'
      ],
      install_requires=['invoke', 'pyyaml'],
      entry_points={
        'console_scripts': ['bun = bun.main:program.run']
      },
      data_files=[
            ('/etc/bun', [
                  'etc/bun.yaml',
                  'etc/gitea.yaml',
                  'etc/homeassistant.yaml',
                  'etc/letsencrypt.yaml',
                  'etc/nginx.yaml',
                  'etc/oam.yaml',
                  'etc/portage.yaml',
                  'etc/squeezebox.yaml',
                  'etc/sys.yaml'
            ]),
            ('share/oam/site', [
                  'share/oam/site/bun.py'
            ])
      ]
)
