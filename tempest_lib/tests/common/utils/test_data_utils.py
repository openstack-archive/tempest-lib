# Copyright 2014 NEC Corporation.
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


from tempest_lib.common.utils import data_utils
from tempest_lib.tests import base


class TestDataUtils(base.TestCase):

    def test_rand_uuid(self):
        actual = data_utils.rand_uuid()
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]"
                                         "{4}-[0-9a-f]{4}-[0-9a-f]{12}$")
        actual2 = data_utils.rand_uuid()
        self.assertNotEqual(actual, actual2)

    def test_rand_uuid_hex(self):
        actual = data_utils.rand_uuid_hex()
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^[0-9a-f]{32}$")

        actual2 = data_utils.rand_uuid_hex()
        self.assertNotEqual(actual, actual2)

    def test_rand_name(self):
        actual = data_utils.rand_name()
        self.assertIsInstance(actual, str)
        actual2 = data_utils.rand_name()
        self.assertNotEqual(actual, actual2)

        actual = data_utils.rand_name('foo')
        self.assertTrue(actual.startswith('foo'))
        actual2 = data_utils.rand_name('foo')
        self.assertTrue(actual.startswith('foo'))
        self.assertNotEqual(actual, actual2)

    def test_rand_name_with_prefix(self):
        actual = data_utils.rand_name(prefix='prefix-str')
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^prefix-str-")
        actual2 = data_utils.rand_name(prefix='prefix-str')
        self.assertNotEqual(actual, actual2)

    def test_rand_url(self):
        actual = data_utils.rand_url()
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^https://url-[0-9]*\.com$")
        actual2 = data_utils.rand_url()
        self.assertNotEqual(actual, actual2)

    def test_rand_int(self):
        actual = data_utils.rand_int_id()
        self.assertIsInstance(actual, int)

        actual2 = data_utils.rand_int_id()
        self.assertNotEqual(actual, actual2)

    def test_rand_mac_address(self):
        actual = data_utils.rand_mac_address()
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^([0-9a-f][0-9a-f]:){5}"
                                         "[0-9a-f][0-9a-f]$")

        actual2 = data_utils.rand_mac_address()
        self.assertNotEqual(actual, actual2)

    def test_parse_image_id(self):
        actual = data_utils.parse_image_id("/foo/bar/deadbeaf")
        self.assertEqual("deadbeaf", actual)

    def test_arbitrary_string(self):
        actual = data_utils.arbitrary_string()
        self.assertEqual(actual, "test")
        actual = data_utils.arbitrary_string(size=30, base_text="abc")
        self.assertEqual(actual, "abc" * int(30 / len("abc")))
        actual = data_utils.arbitrary_string(size=5, base_text="deadbeaf")
        self.assertEqual(actual, "deadb")

    def test_random_bytes(self):
        actual = data_utils.random_bytes()  # default size=1024
        self.assertIsInstance(actual, str)
        self.assertRegexpMatches(actual, "^[\x00-\xFF]{1024}")
        actual2 = data_utils.random_bytes()
        self.assertNotEqual(actual, actual2)

        actual = data_utils.random_bytes(size=2048)
        self.assertRegexpMatches(actual, "^[\x00-\xFF]{2048}")
