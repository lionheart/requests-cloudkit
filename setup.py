#!/usr/bin/env/python
# -*- coding: utf-8 -*-

import unittest
import os
from requests_cloudkit import metadata
from distutils.cmd import Command
import re

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open(os.path.join(os.path.dirname(__file__), "README.rst")) as file:
    long_description = file.read()

    id_regex = re.compile(r"<\#([\w-]+)>")
    link_regex = re.compile(r"<(\w+)>")
    link_alternate_regex = re.compile(r"   :target: (\w+)")

    long_description = id_regex.sub(r"<https://github.com/lionheart/requests-cloudkit#\1>", long_description)
    long_description = link_regex.sub(r"<https://github.com/lionheart/requests-cloudkit/blob/master/\1>", long_description)
    long_description = link_regex.sub(r"<https://github.com/lionheart/requests-cloudkit/blob/master/\1>", long_description)
    long_description = link_alternate_regex.sub(r"   :target: https://github.com/lionheart/requests-cloudkit/blob/master/\1", long_description)

classifiers = [
    "Development Status :: 5 - Production/Stable",
    "Environment :: Console",
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Utilities",
    "License :: OSI Approved :: Apache Software License",
]

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test_requests_cloudkit import TestCloudKit
        suite = unittest.TestLoader().loadTestsFromTestCase(TestCloudKit)
        unittest.TextTestRunner(verbosity=2).run(suite)


setup(
    author=metadata.__author__,
    author_email=metadata.__email__,
    classifiers=classifiers,
    cmdclass={'test': TestCommand},
    description="Apple CloudKit server-to-server support for the requests Python library.",
    install_required=["requests>=2.0.0", "ecdsa>=0.13"],
    extras_require={'restmapper': ["requests>=2.0.0", "ecdsa>=0.13", "restmapper==0.1.0"]},
    keywords="requests cloudkit",
    license=metadata.__license__,
    long_description=long_description,
    name='requests-cloudkit',
    package_data={'': ['LICENSE', 'README.rst']},
    packages=['requests_cloudkit'],
    url="https://github.com/lionheart/requests-cloudkit",
    version=metadata.__version__,
)
