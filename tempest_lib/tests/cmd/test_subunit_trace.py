# Copyright 2015 SUSE Linux GmbH
# All Rights Reserved.
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

from datetime import datetime as dt

from ddt import data
from ddt import ddt
from ddt import unpack
from mock import patch

from tempest_lib.cmd import subunit_trace
from tempest_lib.tests import base


@ddt
class TestSubunitTrace(base.TestCase):

    @data(([dt(2015, 4, 17, 22, 23, 14, 111111),
            dt(2015, 4, 17, 22, 23, 14, 111111)],
           "0.000000s"),
          ([dt(2015, 4, 17, 22, 23, 14, 111111),
            dt(2015, 4, 17, 22, 23, 15, 111111)],
           "1.000000s"),
          ([dt(2015, 4, 17, 22, 23, 14, 111111),
            None],
           ""))
    @unpack
    def test_get_durating(self, timestamps, expected_result):
        self.assertEqual(subunit_trace.get_duration(timestamps),
                         expected_result)

    @data(([dt(2015, 4, 17, 22, 23, 14, 111111),
            dt(2015, 4, 17, 22, 23, 14, 111111)],
           0.0),
          ([dt(2015, 4, 17, 22, 23, 14, 111111),
            dt(2015, 4, 17, 22, 23, 15, 111111)],
           1.0),
          ([dt(2015, 4, 17, 22, 23, 14, 111111),
            None],
           0.0))
    @unpack
    def test_run_time(self, timestamps, expected_result):
        patched_res = {
            0: [
                {'timestamps': timestamps}
            ]
        }
        with patch.dict(subunit_trace.RESULTS, patched_res, clear=True):
            self.assertEqual(subunit_trace.run_time(), expected_result)
