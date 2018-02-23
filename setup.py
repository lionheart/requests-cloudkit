#!/usr/bin/env/python
# -*- coding: utf-8 -*-

# Copyright 2012-2017 Lionheart Software LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from distutils.cmd import Command
import os
import re
import unittest
import runpy

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

metadata_filename = "requests_cloudkit/metadata.py"
metadata = runpy.run_path(metadata_filename)

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
    "License :: OSI Approved :: Apache Software License",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python :: 2.6",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python",
    "Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries",
    "Topic :: Software Development :: Libraries :: Python Modules",
    "Topic :: Utilities",
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
    author=metadata['__author__'],
    author_email=metadata['__email__'],
    classifiers=classifiers,
    cmdclass={'test': TestCommand},
    description="Apple CloudKit server-to-server support for the requests Python library.",
    install_requires=["requests>=2.0.0", "ecdsa>=0.13"],
    extras_require={'restmapper': ["requests>=2.0.0", "ecdsa>=0.13", "restmapper>=0.1.0"]},
    keywords="requests cloudkit",
    license=metadata['__license__'],
    long_description=long_description,
    name='requests-cloudkit',
    package_data={'': ['LICENSE', 'README.rst']},
    packages=['requests_cloudkit'],
    url="https://github.com/lionheart/requests-cloudkit",
    version=metadata['__version__'],
)
