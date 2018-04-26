|image0| |image1|

|CI Status| |Version|

This project provides an authentication handler for Apple’s CloudKit
server-to-server API for the requests Python library. In English, this
means that this library lets you interact with CloudKit with Python in a
server environment. It just has two
dependencies–\ `requests <https://github.com/kennethreitz/requests>`__
and python-ecdsa–and lets you skip all of the dull and boring
cryptographic signing steps when authenticating with CloudKit on your
own. While the underlying code is pretty straightforward, there was no
correct code sample available online that described how to do this–but
now there is!

Installation
------------

requests-cloudkit is available for download through the Python Package
Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

    pip install requests-cloudkit

Usage
-----

requests-cloudkit provides an authentication handler that can be passed
directly to the requests library to authenticate requests to the
CloudKit API. Before working with the CloudKit server-to-server API,
you’ll first need to follow Apple’s instructions to generate a
certificate and a server-to-server key (see `Accessing CloudKit Using a
Server-to-Server
Key <https://developer.apple.com/library/ios/documentation/DataManagement/Conceptual/CloutKitWebServicesReference/SettingUpWebServices/SettingUpWebServices.html#//apple_ref/doc/uid/TP40015240-CH24-SW6>`__).

Once you have these values, just plug them into a CloudKitAuth object,
which you can use with requests to interface with CloudKit. E.g.:

.. code:: pycon

    >>> import requests
    >>> from requests_cloudkit import CloudKitAuth
    >>> auth = CloudKitAuth(key_id=YOUR_KEY_ID, key_file_name=YOUR_PRIVATE_KEY_PATH)
    >>> requests.get("https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/public/zones/list", auth=auth)

Using Requests-CloudKit with RestMapper
---------------------------------------

requests-cloudkit can also be used with
`python-restmapper <https://github.com/lionheart/python-restmapper>`__
to integrate directly with the CloudKit API.

.. code:: pycon

    >>> CloudKit = restmapper.RestMapper("https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/")

Instantiate a cloudkit instance using your CloudKit server-to-server key
ID and provide the path to the private key file.

.. code:: pycon

    >>> cloudkit = CloudKit(auth=CloudKitAuth(key_id=YOUR_KEY_ID, key_file_name=YOUR_KEY_FILE))

Now, you can start making requests to the CloudKit API using a nice
attribute syntax.

.. code:: pycon

    >>> response = cloudkit.public.zones.list()

The above will hit
https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/public/zones/list.

If you want to pass in body data for a POST, provide a single argument
to the call to the API, and specify “POST” as the first attribute (note:
this argument expects a *str* value, so if you want to pass JSON, use
``json.dumps`` to encode it into a string). I.e.

.. code:: pycon

    >>> cloudkit.POST.my.request(data)

Or:

.. code:: pycon

    >>> cloudkit.POST.my.request(json.dumps(json_payload))

For the full list of CloudKit Server-to-Server API capabilities,
reference `Apple’s developer
documentation <https://developer.apple.com/library/ios/documentation/DataManagement/Conceptual/CloutKitWebServicesReference/Introduction/Introduction.html#//apple_ref/doc/uid/TP40015240-CH1-SW1>`__.

Support
-------

If you like this library, or need help implementing it, just send us an
email: hi@lionheartsw.com.

.. _license-licenselicense-imagelicense-url:

License |License|
-----------------

Apache License, Version 2.0. See `LICENSE <license-url>`__ for details.

.. raw:: html

   <!--
   .. |downloads| image:: https://img.shields.io/pypi/dm/requests-cloudkit.svg?style=flat
   .. _downloads: https://pypi.python.org/pypi/requests-cloudkit
   -->

.. |image0| image:: meta/repo-banner.png
.. |image1| image:: meta/repo-banner-bottom.png
   :target: https://lionheartsw.com/
.. |CI Status| image:: https://img.shields.io/travis/lionheart/requests-cloudkit.svg?style=flat
   :target: https://travis-ci.org/lionheart/requests-cloudkit.py
.. |Version| image:: https://img.shields.io/pypi/v/requests-cloudkit.svg?style=flat
   :target: https://pypi.python.org/pypi/requests-cloudkit
.. |License| image:: http://img.shields.io/pypi/l/requests-cloudkit.svg?style=flat
   :target: LICENSE
