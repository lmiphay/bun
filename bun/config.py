# -*- coding: utf-8 -*-

import os
import yaml
import invoke

import bun.backup
import bun.defaults


def settings():
    bunconfig = invoke.config.copy_dict(bun.defaults.settings())

    if os.path.isfile('tests/bun.yaml'):
        invoke.config.merge_dicts(bunconfig, yaml.load(open('tests/bun.yaml')))
    elif os.path.isfile('/etc/bun/bun.yaml'):
        invoke.config.merge_dicts(bunconfig, yaml.load(open('/etc/bun/bun.yaml')))
    elif os.path.isfile('/etc/oam/conf.d/bun.yaml'):
        invoke.config.merge_dicts(bunconfig, yaml.load(open('/etc/oam/conf.d/bun.yaml')))

    return bunconfig

def collection():
    ns = invoke.Collection(bun.backup, bun.defaults)

    ns.configure(settings())

    return ns
