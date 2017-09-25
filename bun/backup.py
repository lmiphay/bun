# -*- coding: utf-8 -*-

import os
import time

from invoke import task

def today(ctx):
    return time.strftime(ctx.bun.timespec)

def exists(ctx, path):
    return os.path.exist('{start_dir}/{path}'.format(path=path, **ctx.bun))

def tar(ctx, path, output='-'):
    return '{nice} tar -C {start_dir} {taropts} -cf {output} ${path}'.format(
        path=path,
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
def tar(ctx, path):
    ctx.run('{tar} | {compress}'.format(tar=tar(ctx, path),
                                        compress=compress(ctx, path.replace('/', '-'))),
            shell=True)

@task
def backupspec(ctx, specname):
    for path in ctx.bun['spec'][specname]:
        if exists(ctx, path):
            tar(ctx, path)

@task(default=True, aliases=['bun'])
def backup(ctx, target=None):
    if target is None:
        target = ctx.bun.default
    if target == 'all':
        for specname in ctx.bun['spec']:
            backupspec(ctx, specname)
    else:
        backupspec(ctx, target)
