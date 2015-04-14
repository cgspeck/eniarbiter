===========
ENI Arbiter
===========

This utility lets you define a pool of Amazon Elastic Network Interfaces and instance tag filter criteria.

When run, it will:

#. find instances that match the criteria
#. detach named ENIs from any instance deemed unhealthy
#. attach any spare ENI to any healthy instance which does not have one

This requires environment variables or an IAM Role to be assigned to the machine it is being run on.

Setup
-----

Create virtualenv::

  mkvirtualenv -p `which python2.7` eni_arbiter

Or activate existing virtualenv::

  workon eni_arbiter

Then install::

  python setup.py install

Sample Config
-------------

See ``config.sample.json``.

Running
-------

After activating your virtualenv, run ``eniarbiter {CONFIG}``, e.g.::

	eniarbiter config.json

There is also a ``--dry-run`` mode and other switches avaliable via ``--help``.