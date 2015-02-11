.. tempest-lib documentation master file, created by
   sphinx-quickstart on Tue Jul  9 22:26:36 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to tempest-lib's documentation!
========================================================

Contents:

.. toctree::
   :maxdepth: 2

   readme
   installation
   usage
   contributing
   cli
   decorators

Release Notes
=============

0.2.1
-----
 * Fix subunit-trace to enable stdout passthrough

0.2.0
-----
 * Adds the skip_because decorator which was migrated from tempest
 * Fixes to rest_client
  * Separates the forbid
 * Cleans up the exception classes to make inheritance simpler
 * Doc typo fixes

0.1.0
-----
 * Adds the RestClient class which was migrated from tempest
 * Fix subunit-trace to handle when there isn't a worker tag in the subunit
   stream

0.0.4
-----
 * Fix subunit-trace when running with python < 2.7

0.0.3
-----
 * subunit-trace bug fixes:
  * Switch to using elapsed time for the summary view
  * Addition of --failonly option from nova's forked subunit-trace

0.0.2
-----
 * Fix the MRO ordering in the base test class

0.0.1
-----
 * Adds cli testing framework
 * Adds subunit-trace


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
