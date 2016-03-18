#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25001))
    return s.makefile('w+', 1)

def main():
    exchange = connect()
    json_string = '{"type": "hello", "team": "JURIEN"}'
    print(json_string, file=exchange)
    hello_from_exchange = json.loads(exchange.readline())
    print("The exchange replied:", hello_from_exchange["cash"], file=sys.stderr)

if __name__ == "__main__":
    main()
