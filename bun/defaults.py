# -*- coding: utf-8 -*-
"""
Implementation of builtin defaults for bun
"""

from __future__ import print_function
import yaml

from invoke import task

DEFAULT_CONFIG = {
    'bun': {
        'backup_dir': '/backup',         # location we backup to
        'checksum': 'sha256sum',         # checksum program to use - leave empty for no checksum generation
        'compress': 'xz -9',             # compression command to use - leave empty for no compression; also see suffix
        'default': ['homes'],            # default 'spec set(s)' to backup; see: spec dict later on
        'nice': 'nice ionice -c3',       # nice'ness to use - leave empty for no nice'ness
        'suffix': 'xz',                  # add this suffix to the generated tarball; see compress program earlier
        'start_dir': '/',                # paths to backup are relative to this dir
        'tar_opts': [                    # options to pass to tar
            '--exclude-caches',
            '--exclude-vcs',
            '--exclude-vcs-ignores',
            '--one-file-system'
            ],
        'timespec': '%Y%m%d-%H%M%S',     # alt: '%Y%m%d'
        'spec': {                        # directory sets that can be backed up
            'homes': [                   # unique token to identify the set (the reserved token 'all' means all sets)
                'home',                  # list of directories/files to backup relative to the start_dir
                'root'
                ]
        }
    },
    'run': {                             # invoke default overrides
        'echo': True
    }
}


def settings():
    """Returns the unaltered default built-in configuration for bun"""
    return DEFAULT_CONFIG


@task(default=True)
def defaults(ctx):  # pylint: disable=unused-argument
    """
    dump the default settings to the console
    :param ctx:
    :return:
    """
    print(yaml.dump(settings(), default_flow_style=False))
