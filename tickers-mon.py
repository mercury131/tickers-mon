import csv
from finviz.screener import Screener
import finviz
import time
import requests 
import os
from os import environ


csvfile='tickers.csv'

bot_chatID = ''

bot_token = ''

timeout=300

wtrigger=2

ctrigger=5

tickers = []

if environ.get('csvfile') is not None:
    csvfile = str(os.environ['csvfile'])

if environ.get('bot_chatID') is not None:
    bot_chatID = str(os.environ['bot_chatID'])

if environ.get('bot_token') is not None:
    bot_token = str(os.environ['bot_token'])

if environ.get('timeout') is not None:
    timeout = int(os.environ['timeout'])

def telegram_bot_sendtext(bot_message,bot_token,bot_chatID):
    
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

with open(csvfile, "r") as a_file:
  for line in a_file:
    stripped_line = line.strip()
    tickers.append(stripped_line)

print(tickers)
olddata = dict()
while True:
  data = dict()
  for ticker in tickers:
      print("Processing ticker: ",ticker)
      current_price=float((finviz.get_stock(ticker.replace(".","-"))['Price']))
      data.update({ticker: current_price})
      if not olddata:
        n=''
      else:
        key_list = list(olddata.keys())
        val_list = list(olddata.values())
        position = key_list.index(ticker)
        prevprice= val_list[position]
        percent=round(float((prevprice / current_price) * 100 - 100))
        if percent > ctrigger:
          print("Current price: ",current_price, "Previos price: ",prevprice, "Change %:",percent)
          telegram_bot_sendtext( ("Current price: " + current_price + " Previos price: " + prevprice + " Change %:" + percent) ,bot_token,bot_chatID)
        elif percent > wtrigger:
          print("Current price: ",current_price, "Previos price: ",prevprice, "Change %:",percent)
          telegram_bot_sendtext( ("Current price: " + current_price + " Previos price: " + prevprice + " Change %:" + percent) ,bot_token,bot_chatID)
  print("Current data: ",data)
  print("Old data",olddata)
  olddata=data  
  print("Waiting",timeout,"Seconds..")
  time.sleep(timeout)