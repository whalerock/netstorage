Human Friend API to Akamai Netstorage
=====================================

Simple API to manage Akamai Netstorage instances

..code-block:: python

    import netstorage

    token_name, token, hostname = 'TOKENABC SECRET_TOKEN whalerock-nsu.akamai-hd.net'.split()
    ns = netstorage(token_name, token, hostname)
    disk_usage = ns.du('/39650')

    remote_file = '/39650/123.txt'
    destination = '/tmp/'

    # Download a file on netstorage to local filesystem
    ns.download(remote, destination)

    # Delete a file on netstorage
    ns.delete(remote)

Listing contents
----------------

This returns a list of files.

.. code-block:: python

   contents = ns.dir('/396500')

