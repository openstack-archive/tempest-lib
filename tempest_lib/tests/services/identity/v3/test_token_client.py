# Copyright 2015 Hewlett-Packard Development Company, L.P.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import json

import httplib2
from oslotest import mockpatch

from tempest_lib.common import rest_client
from tempest_lib.services.identity.v3 import token_client
from tempest_lib.tests import base
from tempest_lib.tests import fake_http


class TestTokenClientV2(base.TestCase):

    def setUp(self):
        super(TestTokenClientV2, self).setUp()
        self.fake_201_http = fake_http.fake_httplib2(return_type=201)

    def test_auth(self):
        token_client_v3 = token_client.V3TokenClient('fake_url')
        post_mock = self.useFixture(mockpatch.PatchObject(
            token_client_v3, 'post', return_value=self.fake_201_http.request(
                'fake_url', body={'access': {'token': 'fake_token'}})))
        resp = token_client_v3.auth(username='fake_user', password='fake_pass')
        self.assertIsInstance(resp, rest_client.ResponseBody)
        req_dict = json.dumps({
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': 'fake_user',
                            'password': 'fake_pass',
                        }
                    }
                },
            }
        })
        post_mock.mock.assert_called_once_with('fake_url/auth/tokens',
                                               body=req_dict)

    def test_auth_with_tenant(self):
        token_client_v2 = token_client.V3TokenClient('fake_url')
        post_mock = self.useFixture(mockpatch.PatchObject(
            token_client_v2, 'post', return_value=self.fake_201_http.request(
                'fake_url', body={'access': {'token': 'fake_token'}})))
        resp = token_client_v2.auth(username='fake_user', password='fake_pass',
                                    project_name='fake_tenant')
        self.assertIsInstance(resp, rest_client.ResponseBody)
        req_dict = json.dumps({
            'auth': {
                'identity': {
                    'methods': ['password'],
                    'password': {
                        'user': {
                            'name': 'fake_user',
                            'password': 'fake_pass',
                        }
                    }},
                'scope': {
                    'project': {
                        'name': 'fake_tenant'
                    }
                },
            }
        })

        post_mock.mock.assert_called_once_with('fake_url/auth/tokens',
                                               body=req_dict)

    def test_request_with_str_body(self):
        token_client_v3 = token_client.V3TokenClient('fake_url')
        self.useFixture(mockpatch.PatchObject(
            token_client_v3, 'raw_request', return_value=(
                httplib2.Response({"status": "200"}),
                str('{"access": {"token": "fake_token"}}'))))
        resp, body = token_client_v3.request('GET', 'fake_uri')
        self.assertIsInstance(resp, httplib2.Response)
        self.assertIsInstance(body, dict)

    def test_request_with_bytes_body(self):
        token_client_v3 = token_client.V3TokenClient('fake_url')
        self.useFixture(mockpatch.PatchObject(
            token_client_v3, 'raw_request', return_value=(
                httplib2.Response({"status": "200"}),
                bytes(b'{"access": {"token": "fake_token"}}'))))
        resp, body = token_client_v3.request('GET', 'fake_uri')
        self.assertIsInstance(resp, httplib2.Response)
        self.assertIsInstance(body, dict)
