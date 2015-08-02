===========
ENI Arbiter
===========

This utility lets you define a pool of Amazon Elastic Network Interfaces and Elastic IP Addresses and instance tag filter criteria.

When run it will:

#. find instances that match the criteria
#. attach any spare `Elastic Network Interface <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-eni.html>`_ to any matched running instance which does not have one from the set you defined
#. attach any spare `Elastic IP Addresses <http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html>`_ to any matched running instance which does not have one from the set you defined

When an instance is terminated AWS detaches the Elastic Network Interface or Elastic IP Address for you automatically.

This requires environment variables or an IAM Role to be assigned to the machine it is being run on.

Depends on boto (2.38.0) and so requires Python 2.7 and is installable from PyPI with  ``pip install eniarbiter``.

Sample Config::

    {
    "region": "ap-southeast-2",
    "eni_list": ["eni-913c08e6", "eni-9d3c08ea", "eni-d33c08a4", "eni-cd3e0aba"],
    "ip_list": ["222.15.158.2", "74.89.251.77", "10.126.147.95", "115.69.216.207", "52.124.77.212"],
    "instance_tag_spec": {
        "tag:aws:autoscaling:groupName": "cs-TEST",
        "tag:Availability": "{\"availability\": \"24x7\"}"
        }
    }

The variables ``eni_list`` and ``ip_list`` may be omitted if you do not require that functionality.

Running
-------

After activating your virtualenv, run ``eniarbiter {CONFIG}``, e.g.::

    (eniarbiter)[chris@tripparch eniarbiter]$ eniarbiter config.json
    2015-04-14 23:06:52,121 - INFO - Connecting to AWS...
    2015-04-14 23:06:52,123 - INFO - Retrieving ENIs...
    2015-04-14 23:06:52,821 - INFO - 3 available ENIS
    2015-04-14 23:06:52,954 - INFO - 3 running matching instances
    2015-04-14 23:06:52,954 - INFO - Attaching interface eni-cd3e0aba to instance i-07c46dc9 as eth1
    2015-04-14 23:06:53,180 - INFO - Attaching interface eni-9d3c08ea to instance i-b4c46d7a as eth1
    2015-04-14 23:06:53,389 - INFO - Instance i-1fc56cd1 already has a specified ENI attached

And if you immediately re-run you will see that the ENIs are attached and available count has reduced::

    (eniarbiter)[chris@tripparch eniarbiter]$ eniarbiter config.json
    2015-04-14 23:07:05,039 - INFO - Connecting to AWS...
    2015-04-14 23:07:05,041 - INFO - Retrieving ENIs...
    2015-04-14 23:07:05,436 - INFO - 1 available ENIS
    2015-04-14 23:07:05,748 - INFO - 3 running matching instances
    2015-04-14 23:07:05,749 - INFO - Instance i-07c46dc9 already has a specified ENI attached
    2015-04-14 23:07:05,749 - INFO - Instance i-b4c46d7a already has a specified ENI attached
    2015-04-14 23:07:05,749 - INFO - Instance i-1fc56cd1 already has a specified ENI attached
    (eniarbiter)[chris@tripparch eniarbiter]$

There is also a Dry Run mode (``--dry-run`` or ``-c``)::

    (eniarbiter)[chris@tripparch eniarbiter]$ eniarbiter config.json -c
    2015-04-14 23:06:39,959 - INFO - Connecting to AWS...
    2015-04-14 23:06:39,961 - INFO - Retrieving ENIs...
    2015-04-14 23:06:40,174 - INFO - 3 available ENIS
    2015-04-14 23:06:40,316 - INFO - 3 running matching instances
    2015-04-14 23:06:40,317 - INFO - Propose attching interface eni-cd3e0aba to instance i-07c46dc9 as eth1
    2015-04-14 23:06:40,317 - INFO - Propose attching interface eni-9d3c08ea to instance i-b4c46d7a as eth1
    2015-04-14 23:06:40,317 - INFO - Instance i-1fc56cd1 already has a specified ENI attached

Setup from source
-----------------

Create virtualenv::

  mkvirtualenv -p `which python2.7` eni_arbiter

Or activate existing virtualenv::

  workon eni_arbiter

Then install::

  python setup.py install

For development I suggest you do a ``pip install -r requirements-dev.txt``.


Initially created April 2015 by Chris Speck | `Web <https://www.chrisspeck.com>`_ | `Github <https://www.github.com/cgspeck>`_

Licensed under the GPLv3