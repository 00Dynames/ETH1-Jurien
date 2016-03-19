#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json

#GLOBALS

money = 0
bond_fair = 1000
book = {}
orders = []

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25001))
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
    

# Handles server responses    
def processServerResponse(json_response):
  response_dict = json.loads(json_response)
  response_type = response_dict["type"]
  global money
  global book
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
    # Update our local copy of the book
    book[response_dict["symbol"]] = {"buy": response_dict["buy"], "sell": response_dict["sell"]}
    # After each state is recorded, we make decisions on what to buy and what to sell
    # Once we have a list of 100 actions, we send the requests to the exchange and then 
    # process the results.
    # whatToBuy()
    # whatToSell()
    pass

  elif response_type == "trade":
    pass
  elif response_type == "ack":
    # Our order went through
    pass

  elif response_type == "reject":
    # Remove the order from out local list
    print (response_dict["order_id"], response_dict["error"])

  elif response_type == "fill":        
    pass
  elif response_type == "out":    
    pass
        
  return response_dict
  

# Generates buy requests and adds it onto the orders list
def whatToBuy():
  # Max number of bonds we buy in 1 transaction is 5
  symbol = "BOND"
  size = 1
  order_id = getOrderId()
  price = bestSellPrice(symbol)
  for j in range(50):
    if canBuy(symbol) and price > 0
      buy_request = '{"type": "add", "order_id": ' + str(order_id) + ', "symbol": ' + symbol + ', "dir": "BUY", "price": ' + price + ', "size": ' + size + ' }'
      orders.insert(buy_request)



# Generates sell requests and adds it onto the orders list
def whatToSell():  
  symbol = "BOND"
  size = 1
  order_id = getOrderId()
  for j in range(100):
    if canSell(symbol) and price > 0
      sell_request = '{"type": "add", "order_id": ' + str(order_id) + ', "symbol": ' + symbol + ', "dir": "BUY", "price": ' + price + ', "size": ' + size + ' }'
      orders.insert(sell_request)



def main():
  exchange = connect()
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)
  hello_from_exchange = json.loads(exchange.readline())
  print(hello_from_exchange)
  print(json_string, file=exchange)
 
  while 1:
    # Read everything the server says  
    try:
      message_from_exchange = json.loads(exchange.readline())
      processServerResponse(message_from_exchange)
      print(message_from_exchange)
    except:
      pass

    for i in range(1, 100):
      json_string = '{"type": "add", "order_id": ' + str(i) + ', "symbol": "BOND", "dir": "BUY", "price": 999, "size": 1}'
      try:
        print(json_string, file=exchange)
#	print("i am trying to buy")
      except:
        pass
      json_string = '{"type": "add", "order_id": ' + str(i+100) + ', "symbol": "BOND", "dir": "SELL", "price": 1001, "size": 1}'
      try:
        print(json_string, file=exchange)
#	print("i am trying to sell")
      except:
        pass

if __name__ == "__main__":
  main()
