# -*- coding: utf-8 -*-

# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import warnings

import pbr.version

__version__ = pbr.version.VersionInfo(
    'tempest_lib').version_string()

# Emit a warning for tempest-lib deprecation. We want the warning to
# be displayed only once.
warnings.simplefilter('once', category=DeprecationWarning)
warnings.warn(
    'tempest-lib is deprecated for future bug-fixes and code changes in favor '
    'of tempest. Please change your imports from tempest_lib to tempest.lib',
    DeprecationWarning)
# And back to normal!
warnings.resetwarnings()
