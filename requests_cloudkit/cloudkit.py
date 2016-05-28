#!/usr/bin/env python

import base64
import datetime
import ecdsa
import hashlib
import json
import pytz
import requests
import tempfile

class CloudKitAuth(requests.auth.AuthBase):
    def __init__(self, key_id, key_file_name):
        self.key_id = key_id
        self.key_file_name = key_file_name

    def __call__(self, r):
        dt = datetime.datetime.now(tz=pytz.UTC)
        dt = dt.replace(microsecond=0)
        formatted_date = dt.isoformat().replace("+00:00", "Z")

        r.headers = {
            'Content-Type': "text/plain",
            'X-Apple-CloudKit-Request-SignatureV1': self.make_signature(formatted_date, r.body, r.path_url),
            'X-Apple-CloudKit-Request-KeyID': self.key_id,
            'X-Apple-CloudKit-Request-ISO8601Date': formatted_date
        }
        return r

    def make_signature(self, formatted_date, body, path):
        signature = "{}:{}:{}".format(formatted_date, self.encode_body(body), path)

        with tempfile.NamedTemporaryFile() as signature_file, tempfile.NamedTemporaryFile() as body_file:
            body_file.write(signature)
            body_file.seek(0)

            sk = ecdsa.SigningKey.from_pem(open(self.key_file_name).read())
            signature = sk.sign(body_file.read(), hashfunc=hashlib.sha256, sigencode=ecdsa.util.sigencode_der)
            return base64.b64encode(signature)

    def encode_body(self, body):
        if body is None:
            body = ""
        elif type(body) != str:
            body = json.dumps(body, separators=(',', ':'))

        h = hashlib.sha256(body)
        return base64.b64encode(h.digest())

