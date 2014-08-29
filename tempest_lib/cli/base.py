# Copyright 2013 OpenStack Foundation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging
import os
import shlex
import subprocess

from tempest_lib import base
import tempest_lib.cli.output_parser
from tempest_lib import exceptions


LOG = logging.getLogger(__name__)


def execute(cmd, action, flags='', params='', fail_ok=False,
            merge_stderr=False, cli_dir='/usr/bin'):
    """Executes specified command for the given action."""
    cmd = ' '.join([os.path.join(cli_dir, cmd),
                    flags, action, params])
    LOG.info("running: '%s'" % cmd)
    cmd = shlex.split(cmd.encode('utf-8'))
    result = ''
    result_err = ''
    stdout = subprocess.PIPE
    stderr = subprocess.STDOUT if merge_stderr else subprocess.PIPE
    proc = subprocess.Popen(cmd, stdout=stdout, stderr=stderr)
    result, result_err = proc.communicate()
    if not fail_ok and proc.returncode != 0:
        raise exceptions.CommandFailed(proc.returncode,
                                       cmd,
                                       result,
                                       result_err)
    return result


class CLIClientBase(object):
    def __init__(self, username='', password='', tenant_name='', uri='',
                 cli_dir='', *args, **kwargs):
        super(CLIClientBase, self).__init__()
        self.cli_dir = cli_dir if cli_dir else '/usr/bin'
        self.username = username
        self.tenant_name = tenant_name
        self.password = password
        self.uri = uri

    def nova(self, action, flags='', params='', admin=True, fail_ok=False,
             endpoint_type='publicURL'):
        """Executes nova command for the given action."""
        flags += ' --endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'nova', action, flags, params, admin, fail_ok)

    def nova_manage(self, action, flags='', params='', fail_ok=False,
                    merge_stderr=False):
        """Executes nova-manage command for the given action."""
        return execute(
            'nova-manage', action, flags, params, fail_ok, merge_stderr)

    def keystone(self, action, flags='', params='', admin=True, fail_ok=False):
        """Executes keystone command for the given action."""
        return self.cmd_with_auth(
            'keystone', action, flags, params, admin, fail_ok)

    def glance(self, action, flags='', params='', admin=True, fail_ok=False,
               endpoint_type='publicURL'):
        """Executes glance command for the given action."""
        flags += ' --os-endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'glance', action, flags, params, admin, fail_ok)

    def ceilometer(self, action, flags='', params='', admin=True,
                   fail_ok=False, endpoint_type='publicURL'):
        """Executes ceilometer command for the given action."""
        flags += ' --os-endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'ceilometer', action, flags, params, admin, fail_ok)

    def heat(self, action, flags='', params='', admin=True,
             fail_ok=False, endpoint_type='publicURL'):
        """Executes heat command for the given action."""
        flags += ' --os-endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'heat', action, flags, params, admin, fail_ok)

    def cinder(self, action, flags='', params='', admin=True, fail_ok=False,
               endpoint_type='publicURL'):
        """Executes cinder command for the given action."""
        flags += ' --endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'cinder', action, flags, params, admin, fail_ok)

    def swift(self, action, flags='', params='', admin=True, fail_ok=False,
              endpoint_type='publicURL'):
        """Executes swift command for the given action."""
        flags += ' --os-endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'swift', action, flags, params, admin, fail_ok)

    def neutron(self, action, flags='', params='', admin=True, fail_ok=False,
                endpoint_type='publicURL'):
        """Executes neutron command for the given action."""
        flags += ' --endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'neutron', action, flags, params, admin, fail_ok)

    def sahara(self, action, flags='', params='', admin=True,
               fail_ok=False, merge_stderr=True, endpoint_type='publicURL'):
        """Executes sahara command for the given action."""
        flags += ' --endpoint-type %s' % endpoint_type
        return self.cmd_with_auth(
            'sahara', action, flags, params, admin, fail_ok, merge_stderr)

    def cmd_with_auth(self, cmd, action, flags='', params='',
                      fail_ok=False, merge_stderr=False):
        """Executes given command with auth attributes appended."""
        # TODO(jogo) make admin=False work
        creds = ('--os-username %s --os-tenant-name %s --os-password %s '
                 '--os-auth-url %s' %
                 (self.username,
                  self.tenant_name,
                  self.password,
                  self.uri))
        flags = creds + ' ' + flags
        return execute(cmd, action, flags, params, fail_ok, merge_stderr,
                       self.cli_dir)


class ClientTestBase(base.BaseTestCase):

    def setUp(self):
        super(ClientTestBase, self).setUp()
        self.clients = self._get_clients()
        self.parser = tempest_lib.cli.output_parser

    def _get_clients(self):
        raise NotImplementedError

    def assertTableStruct(self, items, field_names):
        """Verify that all items has keys listed in field_names."""
        for item in items:
            for field in field_names:
                self.assertIn(field, item)

    def assertFirstLineStartsWith(self, lines, beginning):
        self.assertTrue(lines[0].startswith(beginning),
                        msg=('Beginning of first line has invalid content: %s'
                             % lines[:3]))
