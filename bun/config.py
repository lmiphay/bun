# -*- coding: utf-8 -*-
"""
Implements configuration discovery for bun
"""

from __future__ import print_function
import glob
import os
import yaml
import invoke
from invoke import task

import bun.backup
import bun.defaults


def add_packages(bun_config, directory):
    """
    if directory exists then merge all configuration into the bun_config dict

    :param bun_config: existing dict config to merge new config into
    :param directory: directory which holds config to merge
    :return: merged dict of the original config plus config from directory
    """
    if os.path.isdir(directory):
        for config_file in glob.glob('{}/*.yaml'.format(directory)):
            with open(config_file, encoding='utf-8') as package_yaml:
                invoke.config.merge_dicts(bun_config, yaml.safe_load(package_yaml))
    return bun_config


def settings():
    """
    generate a consolidated set of configuration for bun - if BUN_CONFIG_DIR is set
    then only read configuration from there; otherwise read config from the
    directory /etc/bun and the file /etc/oam/conf.d/bun.yaml (if it exists)

    :return: a dict holding bun configuration
    """
    bun_config = invoke.config.copy_dict(bun.defaults.settings())

    if 'BUN_CONFIG_DIR' in os.environ:
        add_packages(bun_config, os.environ('BUN_CONFIG_DIR'))
    else:
        if os.path.isdir('/etc/bun'):
            add_packages(bun_config, '/etc/bun')
            if os.path.isfile('/etc/oam/conf.d/bun.yaml'):
                with open('/etc/oam/conf.d/bun.yaml', encoding='utf-8') as bun_yaml:
                    invoke.config.merge_dicts(bun_config, yaml.safe_load(bun_yaml))

    return bun_config


def collection():
    """Return an invoke collection for bun"""
    # pylint: disable=invalid-name
    ns = invoke.Collection(
        bun.backup.backup,
        bun.backup.check,
        bun.backup.ignore,
        bun.backup.pretend,
        bun.backup.restore,
        bun.backup.verify,
        bun.backup.watch,
        bun.config,
        bun.defaults)

    ns.configure(settings())

    return ns


@task(default=True)
def config(ctx):
    """
    dump configuration in effect to the console

    :param ctx: invoke context
    """
    print(yaml.dump(ctx.bun, default_flow_style=False))
    # print(ctx.bun.backup_dir)
