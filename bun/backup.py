# -*- coding: utf-8 -*-
"""
Implement backup, verify, restore for bun.
"""
from __future__ import print_function
import glob
import os
import sys
import time

from invoke import task

SHELL = '/bin/bash'
PIPELINE = '{nice} {tar} {compress} {check_sum} {write}'
TARBALL = '{backup_dir}/{timestamp}/{spec_name}.tar.{suffix}{extra_suffix}'
DESTINATION = '>{tarball}'


def opt(cond, true_return):
    """helper to optionally add commands to a commaned pipeline if cond is not the empty string"""
    return true_return if cond != '' else ''


def now(ctx):
    """Return a string representing the current time formatted as per timespec"""
    return time.strftime(ctx.bun.timespec)


def latest_backup(ctx):
    """Return the latest directory in backup_dir (by creation time) - assumed to be a directory"""
    return max(glob.glob('{}/*'.format(ctx.bun.backup_dir)), key=os.path.getctime)


class Bun(object):
    """
    Backup path(s) based on configuration.
    """

    def __init__(self, ctx, timestamp):
        """
        :param ctx: invoke context
        :param timestmp: the timestamp of the (relevant) backup
        """
        self.ctx = ctx
        self.timestamp = timestamp  # same for all tarballs in a session
        self.backup_dir = '{backup_dir}/{timestamp}'.format(backup_dir=ctx.bun.backup_dir, timestamp=timestamp)

    def tarball(self, spec_name, extra_suffix=''):
        """
        Return the full path name of a tarball (or checksum of that tarball) based on spec_name
        :param spec_name: unique name prefix for a tarball/checksum file
        :param extra_suffix: optional suffix to add to the generated path name
        :return: a (string) tarball file name (fully qualified)
        """
        return TARBALL.format(spec_name=spec_name,
                              timestamp=self.timestamp,
                              extra_suffix=extra_suffix,
                              **self.ctx.bun)

    def redirect(self, spec_name, extra_suffix=''):
        """
        Generates the shell output redirect to create a tarball (or checksum of that tarball)
        :param spec_name: unique name prefix for a tarball/checksum file
        :param extra_suffix: optional suffix to add to the generated redirect/path
        :return: a redirect to path string suitable to store the generated tarball
        """
        return DESTINATION.format(tarball=self.tarball(spec_name, extra_suffix))

    def tar(self, paths, output='-'):
        """
        Generate a tar command
        :param paths: list of paths to backup in one go
        :param output: optionally specify the output directly - defaults to stdout ('-')
        :return: the tar command
        """
        return 'tar -C {start_dir} {opts} -cf {output} {ents}'.format(opts=' '.join(self.ctx.bun.tar_opts),
                                                                      output=output,
                                                                      ents=' '.join(paths),
                                                                      **self.ctx.bun)

    def compress(self, output='-'):
        """
        Generate the (optional) compress command as part of the backup pipeline
        :param output: optionally specify the output directly - defaults to stdout ('-')
        :return: the compress command
        """
        return opt(self.ctx.bun.compress, '| {compress} {output}'.format(output=output, **self.ctx.bun))

    def check_sum(self, spec_name):
        """
        return a shell command to create the specified checksum of the created tarball.
        :param spec_name: use this as the start of the tarball name
        :return: the checksum pipeline command to create the checksum file
        """
        return opt(self.ctx.bun.checksum,
                   '| tee >({checksum}{path})'.format(path=self.redirect(spec_name,
                                                                         extra_suffix='.' + self.ctx.bun.checksum),
                                                      **self.ctx.bun))

    def pipeline(self, spec_name, paths):
        """
        return a shell command to backup the directory tree at path
        :param spec_name: use this as the start of the tarball name
        :param paths: list of paths to backup in one go
        :return: the tar pipeline command to tar'up the directory tree under path
        """
        return PIPELINE.format(nice=self.ctx.bun.nice,
                               tar=self.tar(paths),
                               compress=self.compress(),
                               check_sum=self.check_sum(spec_name),
                               write=self.redirect(spec_name))

    def paths(self, target):
        """
        generator which yields the list of paths to process
        :param target: specifies the list of spec sets to return
        :return: (yield) a tuple: the (spec_name, path(s) list) to be backed up
        """
        if len(target) == 0:
            target = self.ctx.bun.default
        if target == ['all']:
            target = [key for key in self.ctx.bun.spec]
        for spec_name in target:
            if spec_name in self.ctx.bun.spec:
                yield (spec_name, self.ctx.bun.spec[spec_name])
            else:
                print('spec {} is not found'.format(spec_name))

    def only_existing(self, paths):
        """
        Return a list of elements from paths which exist on the filesystem (respects start_dir).
        """
        result = []
        for ent in paths:
            if os.path.exists('{start_dir}/{path}'.format(path=ent, **self.ctx.bun)):
                result.append(ent)
            else:
                print('{} does not exist'.format(ent))
        return result

    def backup(self, target):
        """
        Foreach target spec, backup the specified paths (if they exist).
        :param target: a list of one or more target spec names
        """
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        for spec_name, paths in self.paths(target):
            if not self.ctx.run(self.pipeline(spec_name, self.only_existing(paths))):
                print(' FAILED')
                return 1
        return 0

    def pretend(self, target):
        """
        As per backup, but don't check if paths exist, and only echo the tar command (not run it)
        :param target: is a list of one or more target spec names
        """
        for spec_name, paths in self.paths(target):
            print(self.pipeline(spec_name, paths))

    def verify(self, target):
        """
        Foreach tarball in the target spec(s) verify the check sums

        :param target: spec name to verify
        """
        result = 0

        for spec_name, paths in self.paths(target):  # pylint: disable=unused-variable
            tarball = self.tarball(spec_name)
            if os.path.exists('{}.{}'.format(tarball, self.ctx.bun.checksum)):
                print('{} '.format(tarball), end='')  # , flush=True
                sys.stdout.flush()
                if not self.ctx.run('{checksum} -c {tarball}.{checksum} < {tarball}'.format(tarball=tarball,
                                                                                            **self.ctx.bun),
                                    echo=False):
                    print(' FAILED')
                    result = 1

        return result

    def restore(self, location, target):
        """
        extract the tarballs belonging to target in bun.backup_dir to location
        :param location: is the point where the tarballs will be extracted to
        :param target: is the spec name of the target(s) to extract
        """
        result = 0

        with self.ctx.cd(location):
            for spec_name, paths in self.paths(target):  # pylint: disable=unused-variable
                tarball = self.tarball(spec_name)
                print('{}: '.format(tarball), end='')
                sys.stdout.flush()
                if os.path.exists(tarball):
                    if not self.ctx.run('echo tar -xf {}'.format(tarball)):
                        print(' FAILED')
                        result = 1

        return result


@task(default=True, iterable=['target'])
def bun(ctx, target):
    """
    back-up now
    :param ctx: invoke context
    :param target: 0 or more names of spec sets to backup
    """
    return Bun(ctx, now(ctx)).backup(target)


@task(iterable=['target'])
def pretend(ctx, target):
    """
    print out the commands which would be executed, but don't execute the backup
    :param ctx: invoke context
    :param target: 0 or more names of spec sets to backup
    """
    Bun(ctx, now(ctx)).pretend(target)


@task(iterable=['target'])
def verify(ctx, timestamp, target):
    """
    verify the check sums on tarballs which have been already created
    :param ctx: invoke context
    :param timestamp: the timestamp of the targets to verify
    :param target: 0 or more names of spec sets to backup
    """
    return Bun(ctx, timestamp).verify(target)


@task
def watch(ctx, interval=5):
    """
    run a watch(1) to observe the backup in progress
    :param ctx: invoke context
    :param interval: the interval between watch refreshes
    """
    with ctx.cd(latest_backup(ctx)):
        ctx.run('watch -n {interval} -d ls -lh'.format(interval=interval))


@task(iterable=['target'])
def restore(ctx, timestamp, location, target):
    """
    extract the specified target tarballs from the configured backup directory
    to location

    :param ctx: invoke context
    :param timestamp: the timestamp of the targets to restore
    :param location: where to extract the tarball(s) to
    :param target: spec name(s) whose tarballs will be extracted
    """
    return Bun(ctx, timestamp).restore(location, target)
