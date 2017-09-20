# -*- coding: utf-8 -*-

import os
import yaml
import invoke

import bun.backup
import bun.defaults

ns = Collection(bun.backup, bun.defaults)

BUNCONFIG = invoke.config.copy_dict(bun.defaults.settings())

if os.path.isfile('tests/bun.yaml'):
    invoke.config.merge_dicts(BUNCONFIG, yaml.load(open('tests/bun.yaml')))
elif os.path.isfile('/etc/oam/conf.d/bun.yaml'):
    invoke.config.merge_dicts(BUNCONFIG, yaml.load(open('/etc/oam/conf.d/bun.yaml')))

ns.configure(BUNCONFIG)
