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

my_stock = {}

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
    
def hello():
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)

# Handles server responses    
def bestBuyPrice(symbol):
  global book
  return book[symbol]["buy"][0][0]

def bestSellPrice(symbol):
  global book
  return book[symbol]["sell"][0][0]

def processServerResponse(json_response):
  response_dict = json.loads(json_response)
  response_type = response_dict["type"]
  global my_stock
  global money
  global book
  if response_type == "hello":
    money = response_dict["cash"]

    for symbol_pair in response_dict["symbols"]:
      sym = symbol_pair["symbol"]
      pos = symbol_pair["position"]      
      
      my_stock[sym] = pos
    
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
    print response_dict
    hello()
    
    #this means that our order has been filled
    #so we should re-evaluate the state by saying hello
    
    json_string = '{"type": "hello", "team": "JURIEN"}'
    print(json_string, file=exchange)          


    pass
  elif response_type == "out":    
    pass
        
  return response_dict

def fairPrice(symbol):
  mid = (bestSellPrice(symbol) + bestBuyPrice(symbol)) / 2  
  return mid

def canBuy():
  global cash
  if cash <= -40000:
    return False
  else:
    return True    

# gives the lowest selling price to sell quickly
# returns "pennied" price to sell
def recommendedPriceToSell(symbol):
  fair_price = fairPrice(symbol)
  price_to_sell = bestSellPrice(symbol)
  for i in range(0, len(book[symbol]['sell'])):
    if price_to_sell > book[symbol]['sell'][i][0] and book[symbol]['sell'][i][0] > fair_price + 1:
      price_to_sell = books[symbol]['sell'][i][0] - 1 
  return price_to_sell  
    
# returns "pennied" price to buy
def recommendedPriceToBuy(symbol):
  fair_price = fairPrice(symbol)
  price_to_buy = bestBuyPrice(symbol)
  for i in range(0, len(book[symbol]['buy'])):
    if price_to_buy > book[symbol]['buy'][i][0] and book[symbol]['buy'][i][0] < fair_price - 1:
      price_to_buy = books[symbol]['buy'][i][0] + 1
  return price_to_buy   
    
def main():
  exchange = connect()
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)
  hello_from_exchange = json.loads(exchange.readline())
  print(hello_from_exchange)
  print(json_string, file=exchange)
 
  while 1:
    # Read everything the server says  
    # call nevins thingo here probs
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
