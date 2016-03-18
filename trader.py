`x#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25002))
    return s.makefile('w+', 1)


def add(order_id, symbol, direction, price, size):
    #direction is buying / selling

    json_string = '{"type": "add", "order_id": "' + order_id + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "price": "' + price + '", "size": "'+size +'"}'
    
def convert(order_id, symbol, direction, price, size):
    json_string = '{"type": "convert", "order_id": "' + order_id + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "size": "'+size +'"}'
    
def cancel(order_id):
    json_string = '{"type": "cancel", "order_id": "'+ order_id + '"}'
    

def main():
    exchange = connect()
    

    
    
    
    print("{'type': 'hello', 'team': 'JURIEN'}", file=exchange)
    
    hello_from_exchange = json.loads(exchange.readline())
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
