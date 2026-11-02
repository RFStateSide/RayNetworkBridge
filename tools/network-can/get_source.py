#!/usr/bin/env python3
# Copyright (C) 2026 RF StateSide LLC; SPDX-License-Identifier: AGPL-3.0-or-later
"""Retrieve the offered deployment source ZIP; never transmit CAN or extract code."""
import argparse
import base64
import hashlib
import json
from pathlib import Path
import re
import socket
import time

MAX_BYTES = 2 * 1024 * 1024

def receive_source(host, port):
    deadline = time.monotonic() + 15
    with socket.create_connection((host, port), timeout=5) as connection:
        with connection.makefile('rwb') as stream:
            def read():
                remaining = deadline - time.monotonic()
                if remaining <= 0: raise ValueError('Source transfer deadline')
                connection.settimeout(remaining)
                line = stream.readline(1026)
                if not line or len(line) > 1024 or not line.endswith(b'\n'):
                    raise ValueError('Source envelope bound or premature EOF')
                item = json.loads(line)
                if not isinstance(item, dict): raise ValueError('Source envelope')
                return item
            hello = read()
            offer = hello.get('source', {})
            if hello.get('kind') != 'hello' or hello.get('version') != 1 or not isinstance(offer, dict):
                raise ValueError('RN2K/1 greeting required')
            size, digest = offer.get('bytes'), offer.get('sha256')
            if (type(size) is not int or not 0 < size <= MAX_BYTES or
                    not isinstance(digest, str) or not re.fullmatch('[0-9a-f]{64}', digest) or
                    offer.get('revision') != 'sha256:' + digest or offer.get('request') != 'source'):
                raise ValueError('Invalid or unavailable source offer')
            stream.write(b'{"kind":"source"}\n');stream.flush()
            content, index, skipped = bytearray(), 0, 0
            while True:
                item = read()
                if item.get('kind') == 'frame' and index == 0 and skipped < 1024:
                    skipped += 1
                    continue
                if item.get('kind') == 'source_end':
                    if item.get('bytes') != size or item.get('sha256') != digest: raise ValueError('Source receipt mismatch')
                    break
                if item.get('kind') != 'source_chunk' or type(item.get('index')) is not int or item['index'] != index:
                    raise ValueError('Source chunk order')
                chunk = base64.b64decode(item.get('data', ''), validate=True)
                if not 0 < len(chunk) <= 512 or len(content) + len(chunk) > size: raise ValueError('Source size bound')
                content.extend(chunk);index += 1
            if len(content) != size or hashlib.sha256(content).hexdigest() != digest:
                raise ValueError('Source checksum mismatch')
            return bytes(content), digest

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host');parser.add_argument('output', type=Path)
    parser.add_argument('--port', type=int, default=29501)
    args = parser.parse_args()
    if not 1 <= args.port <= 65535: parser.error('Port must be 1..65535')
    data, digest = receive_source(args.host, args.port)
    with args.output.open('xb') as target: target.write(data)
    print('Saved deployment source; SHA-256=' + digest)

if __name__ == '__main__':
    main()
