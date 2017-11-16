# -*- coding: utf-8 -*-
"""
Implement script entry point for bun.
"""

import invoke
import bun.config
import bun.defaults


class BunConfig(invoke.Config):
    """
    Specialisation of Config for bun.
    """
    prefix = 'bun'

    @staticmethod
    def global_defaults():
        return invoke.config.merge_dicts(invoke.Config.global_defaults(),
                                         bun.defaults.settings())


class BunProgram(invoke.Program):
    """
    Specialisation of Program for bun.
    """

    def core_args(self):
        core_args = super(BunProgram, self).core_args()
        extra_args = [
            invoke.Argument(names=('pretend', 'dry-run'),
                            help="Show the commands which would be executed, but don't actually execute them"),
        ]
        return core_args + extra_args


# pylint: disable=invalid-name
program = BunProgram(config_class=BunConfig,
                     namespace=bun.config.collection(),
                     version='0.1.0')
