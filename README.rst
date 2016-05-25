Requests-CloudKit |ci| |downloads| |version|
============================================

This project provides Apple CloudKit server-to-server support for the requests Python library.

Installation
------------

requests-cloudkit is available for download through the Python Package Index (PyPi). You can install it right away using pip or easy_install.

.. code:: bash

   pip install requests-cloudkit

Usage
-----

requests-cloudkit provides an authentication object that can be passed directly to requests to authenticate HTTP calls. To work with the CloudKit server-to-server API, you'll need to follow Apple's instructions to generate a certificate and a server-to-server key (see `Accessing CloudKit Using a Server-to-Server Key <https://developer.apple.com/library/ios/documentation/DataManagement/Conceptual/CloutKitWebServicesReference/SettingUpWebServices/SettingUpWebServices.html#//apple_ref/doc/uid/TP40015240-CH24-SW6>`_).

Once you have these values, just plug them into a CloudKitAuth object, which you can use with requests to make API calls to CloudKit. E.g.:

.. code:: pycon

   >>> import requests
   >>> from requests_cloudkit import CloudKitAuth
   >>> auth = CloudKitAuth(key_id=YOUR_KEY_ID, key_file_name=YOUR_PRIVATE_KEY_PATH)
   >>> requests.get("https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/public/zones/list", auth=auth)

requests-cloudkit can also be used with `RestMapper <https://github.com/lionheart/python-restmapper>`_ to integrate directly with the CloudKit API.

.. code:: pycon

   >>> CloudKit = restmapper.RestMapper("https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/")

Instantiate a cloudkit instance using your CloudKit server-to-server key ID and provide the path to the private key file.

.. code:: pycon

   >>> cloudkit = CloudKit(auth=CloudKitAuth(key_id=YOUR_KEY_ID, key_file_name=YOUR_KEY_FILE))

Now, you can start making requests to the CloudKit API using a nice attribute syntax.

.. code:: pycon

   >>> response = cloudkit.public.zones.list()

...will hit https://api.apple-cloudkit.com/database/[version]/[container]/[environment]/public/zones/list.

If you want to pass in body data for a POST, provide a single argument to the call to the API, and specify "POST" as the first attribute. I.e.

.. code:: pycon

   >>> cloudkit.POST.my.request(data)

Support
-------

If you like this library, or need help implementing it, send me an email: dan@lionheartsw.com.

License
-------

.. image:: http://img.shields.io/pypi/l/requests-cloudkit.svg?style=flat
   :target: LICENSE

Apache License, Version 2.0. See `LICENSE <LICENSE>`_ for details.

.. |ci| image:: https://img.shields.io/travis/lionheart/requests-cloudkit.svg?style=flat
.. _ci: https://travis-ci.org/lionheart/requests-cloudkit.py

.. |downloads| image:: https://img.shields.io/pypi/dm/requests-cloudkit.svg?style=flat
.. _downloads: https://pypi.python.org/pypi/requests-cloudkit

.. |version| image:: https://img.shields.io/pypi/v/requests-cloudkit.svg?style=flat
.. _version: https://pypi.python.org/pypi/requests-cloudkit
