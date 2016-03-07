netstorage
==========

Netstorage is a simple client library for Akamai's Netstorage API.

To get started, you'll need the following from your account/luna portal.

- Key name
- Key
- Hostname

Example Use
-----------

First you'll need to create a Netstorage instance.

.. code-block:: python

    import netstorage

    token_name, token, hostname = 'TOKENABC SECRET_TOKEN whalerock-nsu.akamai-hd.net'.split()
    ns = netstorage(token_name, token, hostname)

Disk Usage
----------

The root directory is usually a `CP CODE`.

.. code-block:: python

    disk_usage = ns.du('/39650')

    print disk_usage.files
    print disk_usage.size

List directory contents
-----------------------

Retrieve directory contents

.. code-block:: python

   directory_contents = ns.dir('/396500')
   for item in directory_contents:
       print '{item.name} | {item.path} | {item.size}'.format(item=item)

Deleting a file
---------------

.. code-block:: python

   ns.delete('/396500/important.txt')

Downloading a file
------------------

.. code-block:: python

   ns.download('/396500/very_important.txt', '/tmp/very_important.txt')

   # You can also supply a directory
   ns.download('/396500/very_important.txt', '/tmp/')

Supported actions
-----------------

You'll notice that the methods match Akamai's API documentation.  The
methods that are currrently supported are:

- delete
- dir
- download
- du
- rename

Development Guide
-----------------

To run tests, install `tox` and run `tox`.

Integration tests
~~~~~~~~~~~~~~~~~

We use `betamax`_ to capture the http/https interactions. We filter out sensitive data such as hostname to the nestorage instance, as well as the `KEY NAME` used in the headers.

.. _betamax: https://github.com/sigmavirus24/betamax
