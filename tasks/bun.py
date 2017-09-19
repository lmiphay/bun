# -*- coding: utf-8 -*-

from __future__ import print_function
import os
import pprint
import time
import yaml

from invoke import Collection, task
import invoke

DEFAULT_CONFIG = {
    'bun': {
        'start_dir': '/',        # paths to backup are relative to this dir (we chdir before tar'ing)
        'backup_dir': '/backup', # location we backup to
        'default': 'home',       # default set to backup
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

def today(ctx):
    return time.strftime(ctx.bun.timespec)

def tar(ctx, directory, output='-'):
    return '{nice} tar -C {start_dir} {taropts} -cf {output} ${directory}'.format(
        directory=directory,
        taropts=' '.join(ctx.bun.taropts),
        output=output,
        **ctx.bun)

def compress(ctx, prefix, target='-'):
    return '{compress} {target} > {backup_dir}/{prefix}-{today}.{suffix}'.format(
        target=target,
        prefix=prefix,
        today=today,
        **ctx.bun)

@task
def tar(ctx, directory):
    ctx.run('{tar} | {compress}'.format(tar=tar(ctx, directory),
                                        compress=compress(ctx, directory.replace('/', '-'))),
            shell=True)

@task
def backupspec(ctx, specname):
    for location in ctx.bun['spec'][specname]:
        tar(ctx, location)

@task(default=True, aliases=['bun'])
def backup(ctx, target=None):
    if target is None:
        target = ctx.bun.default
    if target == 'all':
        for specname in ctx.bun['spec']:
            backupspec(ctx, specname)
    else:
        backupspec(ctx, target)

@task
def showconfig(ctx):
    pprint.pprint(ctx.bun)

@task
def yamlconfig(ctx):
    print(yaml.dump(ctx.bun))

@task
def defaultconfig(ctx):
    print(yaml.dump(DEFAULT_CONFIG))

ns = Collection(tar, backupspec, backup, showconfig, yamlconfig, defaultconfig)

BUNCONFIG = invoke.config.copy_dict(DEFAULT_CONFIG)

if os.path.isfile('tests/bun.yaml'):
    invoke.config.merge_dicts(BUNCONFIG, yaml.load(open('tests/bun.yaml')))
elif os.path.isfile('/etc/oam/conf.d/bun.yaml'):
    invoke.config.merge_dicts(BUNCONFIG, yaml.load(open('/etc/oam/conf.d/bun.yaml')))

ns.configure(BUNCONFIG)
