#!/usr/bin/env python
# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

import sys
import unittest
from mock import patch, call, sentinel

from pyutil.scripts.lines import main


class lines_CLITests (unittest.TestCase):
    def setUp(self):
        topatch = [
            'sys.stdin',
            'sys.stdout',
            'pyutil.lineutil.lineify_file',
            'pyutil.lineutil.lineify_fileobjs',
            ]

        self._patchers = []

        for tp in topatch:
            p = patch(tp)
            self._patchers.append(p)

            name = tp.rsplit('.', 1)[-1]
            setattr(self, 'm_' + name, p.__enter__())

        self._original_argv = sys.argv
        sys.argv = [sentinel.FAKE_SCRIPT]

    def tearDown(self):
        for p in self._patchers:
            p.__exit__()

        sys.argv = self._original_argv

    def check_calls(self, mockname, calls):
        self.assertEqual(
            getattr(self, 'm_' + mockname).mock_calls,
            calls)

    # Tests:
    def test_basic_pipe(self):
        main()

        self.check_calls('lineify_fileobjs', [call(sys.stdin, sys.stdout)])
        self.check_calls('lineify_file', [])
