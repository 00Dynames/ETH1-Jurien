`x#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

#GLOBALS

money = 0
bond_fair = 1000


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25002))
    return s.makefile('w+', 1)


def add(order_id, symbol, direction, price, size):
    #direction is buying / selling

    json_string = '{"type": "add", "order_id": "' + str(order_id) + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "price": "' + str(price) + '", "size": "'+ str(size) +'"}'
    return json_string
    
    
def convert(order_id, symbol, direction, price, size):
    json_string = '{"type": "convert", "order_id": "' + str(order_id) + '", "symbol": "' + symbol + '", "dir": "' + direction + '", "size": "'+size +'"}'
    return json_string
    
def cancel(order_id):
    json_string = '{"type": "cancel", "order_id": "'+ str(order_id) + '"}'
    return json_string
    
    
def processServerResponse(json_response):
    response_dict = json.loads(json_response)
    response_type = response_dict["type"]
    global money
    if response_type == "hello":
        money = response_dict["cash"]
    elif response_type == "open":
        #update list of open orders
        pass
    elif response_type == "close":
        pass
    elif response_type == "error":
        print(response_dict["error"])
    elif response_type == "book":
        #update our local copy of the book
        pass
    elif response_type == "trade":
        pass
    elif response_type == "ack":
        #our order went through
        pass

    elif response_type == "reject":
        #remove the order from out local list
        print response_dict["order_id"], response_dict["error"]

    elif response_type == "fill":        
        pass
    elif response_type == "out":    
        pass
        
    return response_dict
    




def main():
    exchange = connect()
    

    
    
    
    print("{'type': 'hello', 'team': 'JURIEN'}", file=exchange)
    
    hello_from_exchange = json.loads(exchange.readline())
    print("The exchange replied:", hello_from_exchange, file=sys.stderr)

if __name__ == "__main__":
    main()
