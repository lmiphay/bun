# -*- coding: utf-8 -*-

import time
import unittest

import mock

from invoke import MockContext

from bun.backup import Bun, opt, now, latest_backup

class BunTest(unittest.TestCase):

    def test_opt(self):
        self.assertEqual(opt('a', 'b'), 'b')
        self.assertEqual(opt('', 'b'), '')

    def test_now(self):
        ctx = MockContext(config={'bun': MockContext(config={'timespec': '%Y'})})
        self.assertEqual(now(ctx), time.strftime('%Y'))

    def test_latest_backup(self):
        ctx = MockContext(config={'bun': MockContext(config={'backup_dir': '/bun'})})
        with mock.patch('glob.glob') as mock_glob:
            mock_glob.return_value = ['a', 'b', 'c']
            with mock.patch('os.path.getctime') as mock_getctime:
                mock_getctime.side_effect = ['1', '3', '2']
                self.assertEqual(latest_backup(ctx), 'b')

    def test_tarball(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'suffix': 'asuf'
        })})
        self.assertEqual(Bun(ctx, 'footime').tarball('aspec', '.xtra'),
                         '/bun/footime/aspec.tar.asuf.xtra')

    def test_redirect(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'suffix': 'asuf'
        })})
        self.assertEqual(Bun(ctx, 'footime').redirect('aspec', '.xtra'),
                         '>/bun/footime/aspec.tar.asuf.xtra')

    def test_tar(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'suffix': 'asuf',
            'start_dir': '/root',
            'tar_opts': ['--bar']
        })})
        self.assertEqual(Bun(ctx, 'footime').tar(['a', 'b'], 'foo_out'),
                         'tar -C /root --bar -cf foo_out a b')

    def test_compress(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'compress': 'zip -9',
            'suffix': 'asuf',
            'start_dir': '/root',
            'tar_opts': ['--bar']
        })})
        self.assertEqual(Bun(ctx, 'footime').compress('bar_out'),
                         '| zip -9 bar_out')

    def test_check_sum(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'checksum': 'cksum',
            'compress': 'zip -9',
            'suffix': 'asuf',
            'start_dir': '/root',
            'tar_opts': ['--bar'],
            'spec': {
                'aspec': ['/a/b', '/fg']
            }
        })})
        self.assertEqual(Bun(ctx, 'footime').check_sum('aspec'),
                         '| tee >(cksum>/bun/footime/aspec.tar.asuf.cksum)')

    def test_pipeline(self):
        ctx = MockContext(config={'bun': MockContext(config={
            'backup_dir': '/bun',
            'checksum': 'cksum',
            'compress': 'zip -9',
            'nice': 'anice',
            'suffix': 'asuf',
            'start_dir': '/root',
            'tar_opts': ['--bar'],
            'spec': {
                'aspec': ['/a/b', '/fg']
            }
        })})
        self.assertEqual(Bun(ctx, 'footime').pipeline('aspec', ['/a/b', '/fg']),
                         'anice tar -C /root --bar -cf - /a/b /fg | zip -9 - | tee >(cksum>/bun/footime/aspec.tar.asuf.cksum) >/bun/footime/aspec.tar.asuf')