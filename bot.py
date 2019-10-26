#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json
from readInTrade import Data
import strategy

# ~~~~~============== CONFIGURATION  ==============~~~~~
# replace REPLACEME with your team name!
team_name = "DRAX"
# This variable dictates whether or not the bot is connecting to the prod
# or test exchange. Be careful with this switch!
test_mode = True

# This setting changes which test exchange is connected to.
# 0 is prod-like
# 1 is slower
# 2 is empty
test_exchange_index = 0
prod_exchange_hostname = "production"

port = 25000 + (test_exchange_index if test_mode else 0)
exchange_hostname = "test-exch-" + \
    team_name if test_mode else prod_exchange_hostname

idcnt = 1

# ~~~~~============== NETWORKING CODE ==============~~~~~


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((exchange_hostname, port))
    return s.makefile('rw', 1)


def write_to_exchange(exchange, obj):
    json.dump(obj, exchange)
    exchange.write("\n")


def read_from_exchange(exchange):
    return json.loads(exchange.readline())


def sell_symbol(exchange, symbol, price, size):
    global idcnt
    write_to_exchange(exchange, {"type": "add", "order_id": idcnt,
                                 "symbol": symbol, "dir": "SELL", "price": price, "size": size})
    idcnt += 1
    return idcnt - 1


def buy_symbol(exchange, symbol, price, size):
    global idcnt
    write_to_exchange(exchange, {"type": "add", "order_id": idcnt,
                                 "symbol": symbol, "dir": "BUY", "price": price, "size": size})
    idcnt += 1
    return idcnt - 1


def buy_convert(exchange, symbol, size):
    global idcnt
    write_to_exchange(exchange,
                      {"type": "convert", "order_id": idcnt, "symbol": symbol, "dir": "BUY", "size": size})
    idcnt += 1
    return idcnt - 1


def sell_convert(exchange, symbol, size):
    global idcnt
    write_to_exchange(exchange,
                      {"type": "convert", "order_id": idcnt, "symbol": symbol, "dir": "SELL", "size": size})
    idcnt += 1
    return idcnt - 1


def cancel_id(exchange, id):
    write_to_exchange(exchange, {"type": "cancel", "order_id": id})

# ~~~~~============== MAIN LOOP ==============~~~~~


def main():
    exchange = connect()
    write_to_exchange(exchange, {"type": "hello", "team": team_name.upper()})
    hello_from_exchange = read_from_exchange(exchange)
    # A common mistake people make is to call write_to_exchange() > 1
    # time for every read_from_exchange() response.
    # Since many write messages generate marketdata, this will cause an
    # exponential explosion in pending messages. Please, don't do that!
    print("rep> ", hello_from_exchange, file=sys.stderr)

    data = Data()
    buy_symbol(exchange, "BOND", 999, 50)
    sell_symbol(exchange, "BOND", 1001, 50)

    while True:
        message = read_from_exchange(exchange)
        if message['type'] == 'close':
            exit()
        elif message['type'] != 'book' and message['type'] != 'trade':
            print("rep> ", message, file=sys.stderr)

        data.read_in_trade(message)

        # strategy
        strategy.bond_buy_sell(exchange, message, data)
        # strategy.operate_car(exchange, message, data)
        strategy.buy_sell_CHE_or_CAR(exchange, message, data)
        strategy.rescent_buy(exchange, message, data)


if __name__ == "__main__":
    main()
