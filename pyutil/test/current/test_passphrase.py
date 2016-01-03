﻿# -*- coding: utf-8-with-signature-unix; fill-column: 77 -*-
# -*- indent-tabs-mode: nil -*-

#  This file is part of pyutil; see README.rst for licensing terms.

import unittest
from cStringIO import StringIO

from mock import patch, call, ANY

from pyutil.scripts import passphrase


class Passphrase(unittest.TestCase):

    @patch('argparse.ArgumentParser')
    @patch('pyutil.scripts.passphrase.gen_passphrase')
    @patch('sys.stdout')
    def test_main(self, m_stdout, m_gen_passphrase, m_ArgumentParser):
        m_args = m_ArgumentParser.return_value.parse_args.return_value
        m_args.dictionary = StringIO('alpha\nbeta\n')
        m_args.bits = 42

        m_gen_passphrase.return_value = ('wombat', 43)

        passphrase.main()

        self.assertEqual(
            m_ArgumentParser.mock_calls,
            [call(
                prog='passphrase',
                description=('Create a random passphrase by ' +
                             'picking a few random words.')),
             call().add_argument(
                 '-d',
                 '--dictionary',
                 help=('what file to read a list of words from ' +
                       "(or omit this option to use passphrase's " +
                       'bundled dictionary)'),
                 type=ANY,
                 metavar="DICT"),
             call().add_argument(
                 'bits',
                 help="how many bits of entropy minimum",
                 type=float,
                 metavar="BITS"),
             call().parse_args()])

        self.assertEqual(
            m_gen_passphrase.mock_calls,
            [call(42, {u'alpha', u'beta'})])

        self.assertEqual(
            m_stdout.mock_calls,
            [call.write(u"Your new password is: 'wombat'. " +
                        "It is worth about 43 bits."),
             call.write('\n')])
