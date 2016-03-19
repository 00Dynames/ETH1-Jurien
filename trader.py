#!/usr/bin/python
from __future__ import print_function

import sys
import socket
import json
import time

#GLOBALS

# The amount of money we have
money = 0
bond_fair = 1000
# The current state of the market
book = {}
# The buy/sell requests that are sent to the exchange
orders = []

# buy original prices
original_prices = {}

# The stocks that we own
my_stock = {}
order_id = 1

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25001))
    return s.makefile('w+', 1)

# Converts to JSON string given the parameters below
def add(order_id, symbol, direction, price, size):
  #direction is buying / selling

  json_string = '{"type": "add", "order_id": ' + str(order_id) + ', "symbol": "' + symbol + '", "dir": "' + direction + '", "price": ' + str(price) + ', "size": '+ str(size) +'}'
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

# The highest price someone is willing to offer for a share    
def bestBuyPrice(symbol):
  global book
  return book[symbol]["buy"][0][0]

# The lowest someone is willing to sell out a share
def bestSellPrice(symbol):
  global book
  return book[symbol]["sell"][0][0]


# Returns the fair price of the stock assuming the market is correct
def fairPrice(symbol):
  if symbol == "BOND":
    return 1000
  
  mid = (bestSellPrice(symbol) + bestBuyPrice(symbol)) / 2  
  return mid

def canSell(symbol):
  if symbol == "VALBZ" and my_stock[symbol] > -10:
    return True
  elif symbol == "VALE" and my_stock[symbol] > -10:
    return True
  elif my_stock[symbol] > -100:
    return True
  return False

 
# Generates buy requests and adds it onto the orders list
def whatToBuy():
  global orders
  global order_id
  # Max number of bonds we buy in 1 transaction is 5
  symbol = "BOND"
  size = 5
 # price = bestSellPrice(symbol)
  price = recommendedPriceToBuy(symbol)
  for j in range(10):
    if canBuy() and price > 0:
      buy_request = add(order_id, symbol, "BUY", price, size)
      orders.append(buy_request)
      order_id += 1
  
  symbol = "VALBZ"
  price = recommendedPriceToBuy(symbol)
  for j in range(10):
    if canBuy() and price > 0:
      buy_request = add(order_id, symbol, "BUY", price, size)
      orders.append(buy_request)
      order_id += 1
      
  symbol = "VALE"
  price = recommendedPriceToBuy(symbol)
  for j in range(10):
    if canBuy() and price > 0: 
      buy_request = add(order_id, symbol, "BUY", price, size)
      orders.append(buy_request)
      order_id += 1


# Generates sell requests and adds it onto the orders list
def whatToSell():
  global orders
  global order_id  
  symbol = "BOND"
  size = "5"
  price = recommendedPriceToSell(symbol)
  for j in range(10):
    if canSell() and price > 0:
      sell_request = add(order_id, symbol, "SELL", price, size)
      orders.append(sell_request)
      order_id += 1

  symbol = "VALBZ"
  price = recommendedPriceToSell(symbol)
  for j in range(10):
    if canSell() and price > 0:      
      sell_request = add(order_id, symbol, "SELL", price, size)
      orders.append(sell_request)
      order_id += 1

  symbol = "VALE"
  price = recommendedPriceToSell(symbol)
  for j in range(10):
    if canSell() and price > 0:      
      sell_request = add(order_id, symbol, "SELL", price, size)
      orders.append(sell_request)
      order_id += 1
      
      
# Sends all the orders to the exchange
def makeTrades(exchange):
  global orders
  for item in orders:
    print(item, file=exchange)

# Processes and handles the different server responses
def processServerResponse(json_response, exchange):
  response_dict = json.loads(json_response)
  response_type = response_dict["type"]
  global my_stock
  global money
  global book
  print(response_dict)
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
    # After each state is recorded, we make decisions on what to buy and what to sell
    # Once we have a list of 100 actions, we send the requests to the exchange and then 
    # process the results.
    #whatToBuy()
    #whatToSell()
#    makeTrades(exchange)
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
    print(response_dict)
    hello()
    
    #this means that our order has been filled
    #so we should re-evaluate the state by saying hello
    if response_dict["dir"] == "BUY":
      if respose_dict["price"] > original_prices[response_dict["symbol"]]:
        original_prices[response_dict["order_id"]] = response_dict["price"]
     
    json_string = '{"type": "hello", "team": "JURIEN"}'
    print(json_string, file=exchange)          


    pass
  elif response_type == "out":    
    pass
        
  return response_dict


def canBuy(symbol):
  global money
  if money <= -40000:
    return False
  else:
    if symbol == "BOND" and my_stock[symbol] < 100: 
      return True   
    elif symbol == "VALBZ" and my_stock[symbol] < 10:
      return True
    elif symbol == "VALE" and my_stock[symbol] < 10:
      return True
  return False

# gives the lowest selling price to sell quickly
# returns "pennied" price to sell
def recommendedPriceToSell(symbol):
  fair_price = fairPrice(symbol)
  price_to_sell = bestSellPrice(symbol)
  for i in range(0, len(book[symbol]['sell'])):
    if price_to_sell > book[symbol]['sell'][i][0] and book[symbol]['sell'][i][0] >= fair_price + 1:
      price_to_sell = books[symbol]['sell'][i][0] - 1 
  return price_to_sell  
    
# returns "pennied" price to buy
def recommendedPriceToBuy(symbol):
  fair_price = fairPrice(symbol)
  price_to_buy = bestBuyPrice(symbol)

  for i in range(0, len(book[symbol]['buy'])):
    if price_to_buy > book[symbol]['buy'][i][0] and book[symbol]['buy'][i][0] <= fair_price - 1:
      price_to_buy = books[symbol]['buy'][i][0] + 1
  return price_to_buy   
    
def main():
  exchange = connect()
  json_string = '{"type": "hello", "team": "JURIEN"}'
  print(json_string, file=exchange)
  hello_from_exchange = json.loads(exchange.readline())
  print(hello_from_exchange)
  print(json_string, file=exchange)
  global book
  while 1:
    # Read everything the server says  
    try:
      message_from_exchange = exchange.readline()
      processServerResponse(message_from_exchange, exchange)
      print(message_from_exchange)
    except:
      pass

    whatToBuy()
    whatToSell()
    makeTrades(exchange)

    time.sleep(0.1)
     
if __name__ == "__main__":
  main()
