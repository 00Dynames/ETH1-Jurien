#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25000))
    return s.makefile('w+', 1)

def main():
    exchange = connect()
    json_string = '{"type": "hello", "team": "JURIEN"}'
    print(json_string, file=exchange)
    hello_from_exchange = json.loads(exchange.readline())


    json_string = '{"type": "add", "order_id": 1, "symbol": "BOND", "dir": "BUY", "price": 999 "size": 1}'
    print(json_string, file=exchange)
    while 1:
      hello_from_exchange = json.loads(exchange.readline())
      json_string = '{"type": "add", "order_id": 1, "symbol": "BOND", "dir": "SELL", "price": 1001 "size": 1}'      
      try:
        print(json_string, file=exchange)
      except:
        pass
      try:
        hello_from_exchange = json.loads(exchange.readline())
      except:
        pass

if __name__ == "__main__":
    main()
