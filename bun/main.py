# -*- coding: utf-8 -*-

import invoke
import bun.config
import bun.defaults

class BunConfig(invoke.Config):
    prefix = 'bun'

    @staticmethod
    def global_defaults():
        return merge_dicts(invoke.Config.global_defaults(),
                           bun.defaults.settings())

program = invoke.Program(config_class=BunConfig,
                         namespace=bun.config.collection(),
                         version='0.0.1')
