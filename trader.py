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
my_stock = {"BOND": 0, "VALBZ": 0, "VALE": 0, "GS": 0, "MS": 0, "WFC": 0, "XLF": 0}
order_id = 1

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("10.0.254.41", 25000))
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
  if not book.has_key(symbol):
    return 0
  return book[symbol]["buy"][0][0]

# The lowest someone is willing to sell out a share
def bestSellPrice(symbol):
  global book
  if not book.has_key(symbol):
    return 0
  return book[symbol]["sell"][0][0]


# Returns the fair price of the stock assuming the market is correct
def fairPrice(symbol):
  if symbol == "BOND":
    return 1000
  
  mid = (bestSellPrice(symbol) + bestBuyPrice(symbol)) / 2  
  return mid

def canSell(symbol):
  if not my_stock.has_key(symbol):
    return False
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
  size = 1 
 # price = bestSellPrice(symbol)
  price = recommendedPriceToBuy(symbol)
  for j in range(10):
    if canBuy(symbol) and price > 0:
      buy_request = add(int(round(time.time() * 1000)), symbol, "BUY", price, size)
      orders.append(buy_request)
      time.sleep(0.001)
  
  symbol = "VALBZ"
  size = "1"
  price = recommendedPriceToBuy(symbol)
  for j in range(5):
    if canBuy(symbol) and price > 0:
      buy_request = add(int(round(time.time() * 1000)), symbol, "BUY", price, size)
      orders.append(buy_request)
      time.sleep(0.001)
  symbol = "VALE"
  price = recommendedPriceToBuy(symbol)
  for j in range(5):
    if canBuy(symbol) and price > 0: 
      buy_request = add(int(round(time.time() * 1000)), symbol, "BUY", price, size)
      orders.append(buy_request)
      time.sleep(0.001)
  symbol = "GS"
  price = recommendedPriceToBuy(symbol)
  for j in range(3):
    if canBuy(symbol) and price > 0: 
      buy_request = add(int(round(time.time() * 1000)), symbol, "BUY", price, size)
      orders.append(buy_request)
      time.sleep(0.001)
  symbol = "MS"
  price = recommendedPriceToBuy(symbol)
  for j in range(5):
    if canBuy(symbol) and price > 0: 
      buy_request = add(int(round(time.time() * 1000)), symbol, "BUY", price, size)
      orders.append(buy_request)
      time.sleep(0.001)


# Generates sell requests and adds it onto the orders list
def whatToSell():
  global orders
  global order_id  
  symbol = "BOND"
  size = 1
  price = recommendedPriceToSell(symbol)
  for j in range(10):
    if canSell(symbol) and price > 0:
      sell_request = add(int(round(time.time() * 1000)), symbol, "SELL", price, size)
      orders.append(sell_request)
      time.sleep(0.001)
  symbol = "VALBZ"
  size = "1"
  price = recommendedPriceToSell(symbol)
  for j in range(5):
    if canSell(symbol) and price > 0:      
      sell_request = add(int(round(time.time() * 1000)), symbol, "SELL", price, size)
      orders.append(sell_request)
      time.sleep(0.001)
  symbol = "VALE"
  price = recommendedPriceToSell(symbol)
  for j in range(5):
    if canSell(symbol) and price > 0:      
      sell_request = add(int(round(time.time() * 1000)), symbol, "SELL", price, size)
      orders.append(sell_request)
      time.sleep(0.001)
  symbol = "GS"
  price = recommendedPriceToSell(symbol)
  for j in range(3):
    if canSell(symbol) and price > 0:      
      sell_request = add(int(round(time.time() * 1000)), symbol, "SELL", price, size)
      orders.append(sell_request)
      time.sleep(0.001)
  symbol = "MS"
  price = recommendedPriceToSell(symbol)
  for j in range(5):
    if canSell(symbol) and price > 0:      
      sell_request = add(int(round(time.time() * 1000)), symbol, "SELL", price, size)
      orders.append(sell_request)
      time.sleep(0.001)
      
      
# Sends all the orders to the exchange
def makeTrades(exchange):
  global orders
  for item in orders:
    print(item, file=exchange)
  orders = []

# Processes and handles the different server responses
def processServerResponse(json_response, exchange):
  response_dict = json.loads(json_response)
  response_type = response_dict["type"]
  global my_stock
  global money
  global book
  global order_id
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
    if response_dict["error"] == "DUPLICATE_ORDER_ID":
      order_id += 10
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
    if response_dict["dir"] == "BUY":
      my_stock[response_dict["symbol"]] += response_dict["size"] 
    else:
      my_stock[response_dict["symbol"]] -= response_dict["size"] 
    
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
    if not my_stock.has_key(symbol):
      return False
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
  if original_prices.has_key(symbol) and original_prices[symbol] > price_to_sell:
    return -1
  if not book.has_key(symbol) or price_to_sell == 0:
    return -1
  if not price_to_sell == fair_price:
    price_to_sell -= 1
  return price_to_sell  
    
# returns "pennied" price to buy
def recommendedPriceToBuy(symbol):
  fair_price = fairPrice(symbol)
  price_to_buy = bestBuyPrice(symbol)
<<<<<<< HEAD

  for i in range(0, len(book[symbol]['buy'])):
    if price_to_buy > book[symbol]['buy'][i][0] and book[symbol]['buy'][i][0] <= fair_price - 1:
      price_to_buy = books[symbol]['buy'][i][0] + 1
=======
  if not book.has_key(symbol) or price_to_buy == 0:
    return -1
  if not price_to_buy == fair_price:
    price_to_buy += 1
>>>>>>> 521b69c4d56db7c65baee7f2e25e1d2783f03999
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
    time.sleep(0.2)
     
if __name__ == "__main__":
  main()
