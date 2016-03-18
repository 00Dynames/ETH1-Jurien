#!/usr/bin/python
from __future__ import print_function

import sys
import socket

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 20000))
    return s.makefile('w+', 1)

def main():
    exchange = connect()
    print("HELLO jurien", file=exchange)
    hello_from_exchange = exchange.readline().strip()
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
