# -*- coding: utf-8 -*-

from __future__ import print_function
import yaml
from invoke import Collection, task

DEFAULT_CONFIG = {
    'bun': {
        'start_dir': '/',        # paths to backup are relative to this dir (we chdir before tar'ing)
        'backup_dir': '/backup', # location we backup to
        'default': 'home',       # default 'set' to backup
        'spec': {                # directory sets that can be backed up
            'home': [
	        'home', # list of directories/files to backup relative to the start_dir
                'root'
            ],
            'portage': [
                'etc/portage',
                'var/db/pkg',
                'usr/src/kernel-config.git',
                'var/lib/layman/installed.xml',
                'var/lib/portage'
            ],
            'sys': [
                'boot',
	        'etc',
                'lib/modules',
                'usr/src/linux/.config',
                'var/spool/cron/crontabs'
            ]
        },
        'nice': 'nice ionice -c3',
        'compress': 'xz -9',
        'suffix': 'tar.xz',
        'taropts': [
	    '--exclude-caches',
	    '--exclude-vcs',
	    '--exclude-vcs-ignores',
	    '--one-file-system'
        ],
        'timespec': '%Y%m%d' # alt: '%Y%m%d-%H-%M'
    }
}

def settings():
    return DEFAULT_CONFIG

@task
def dump(ctx):
    print(yaml.dump(settings()))
