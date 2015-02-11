===========
tempest-lib
===========

OpenStack Functional Testing Library

* Free software: Apache license
* Documentation: http://docs.openstack.org/developer/tempest-lib
* Source: http://git.openstack.org/cgit/openstack/tempest-lib
* Bugs: http://bugs.launchpad.net/tempest

tempest-lib is a library of common functionality that was originally in tempest
(or similar in scope to tempest)

Features
--------

Some of the current functionality exposed from the library includes:

* OpenStack python-* client CLI testing framework
* subunit-trace: A output filter for subunit streams. Useful in conjunction
                 with calling a test runner that emits subunit
* A unified REST Client
* Utility functions:
  * skip_because: Skip a test because of a bug
  * find_test_caller: Perform stack introspection to find the test caller.
                      common methods
