#!/usr/bin/env python

# Copyright 2016-2017 Lionheart Software LLC
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

import base64
import datetime
import ecdsa
import hashlib
import json
import requests
import pytz

class CloudKitAuth(requests.auth.AuthBase):
    """
    See: https://developer.apple.com/library/archive/documentation/DataManagement/Conceptual/CloudKitWebServicesReference/index.html
    """

    def __init__(self, key_id, pem=None, key_file_name=None):
        """
        The key_id is required. You can find it when you create a
        server-to-server certificate in your CloudKit Dashboard.
        """
        self.key_id = key_id
        self.pem = pem
        self.key_file_name = key_file_name

        if not self.pem and not self.key_file_name:
            raise Exception("Requires one of pem or key_file_name")

    def __call__(self, r):
        dt = datetime.datetime.now(tz=pytz.UTC)
        dt = dt.replace(microsecond=0)
        formatted_date = dt.isoformat().replace("+00:00", "Z")
        sig = self.make_signature(formatted_date, r.body, r.path_url)

        r.headers = {
            'Content-Type': "text/plain",
            'X-Apple-CloudKit-Request-SignatureV1': sig,
            'X-Apple-CloudKit-Request-KeyID': self.key_id,
            'X-Apple-CloudKit-Request-ISO8601Date': formatted_date
        }
        return r

    def make_signature(self, formatted_date, body, path):
        """
        See: "Accessing CloudKit Using a Server-to-Server Key"
        """
        to_sign = "{}:{}:{}".format(formatted_date,
                                    self.encode_body(body),
                                    path)

        sk = ecdsa.SigningKey.from_pem(self.get_key())
        signature = sk.sign(to_sign.encode(),
                            hashfunc=hashlib.sha256,
                            sigencode=ecdsa.util.sigencode_der)

        return base64.b64encode(signature)

    def get_key(self):
        """
        Return the private key PEM contents as a byte string.
        """
        if self.pem:
            return self.pem
        else:
            return open(self.key_file_name).read()

    def encode_body(self, body):
        """
        Return the request body. This is the base64 string encoded
        SHA-256 hash of the body.
        """
        if body is None:
            body = ""
        elif type(body) != str:
            body = json.dumps(body, separators=(',', ':'))

        h = hashlib.sha256(body.encode())
        return base64.b64encode(h.digest()).decode()
