#!/usr/bin/python

# ~~~~~==============   HOW TO RUN   ==============~~~~~
# 1) Configure things in CONFIGURATION section
# 2) Change permissions: chmod +x bot.py
# 3) Run in loop: while true; do ./bot.py; sleep 1; done

from __future__ import print_function

import sys
import socket
import json

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
bond_buy = 0
bond_sell = 0

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
    write_to_exchange(exchange, {"type": "add", "order_id": idcnt,
                                 "symbol": symbol, "dir": "SELL", "price": price, "size": size})
    idcnt += 1
    if symbol == 'BOND':
        bond_sell += size


def buy_symbol(exchange, symbol, price, size):
    write_to_exchange(exchange, {"type": "add", "order_id": idcnt,
                                 "symbol": symbol, "dir": "BUY", "price": price, "size": size})
    idcnt += 1
    if symbol == 'BOND':
        bond_buy += size

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

    buy_symbol(exchange, "BOND", 999, 100)
    sell_symbol(exchange, "BOND", 1001, 100)

    while True:
        message = read_from_exchange(exchange)
        if message['type'] == 'fill':
            print("rep> ", message, file=sys.stderr)
            if message['symbol'] == 'BOND':
                if message['dir'] == 'BUY':
                    bond_buy -= message['size']
                    buy_symbol(exchange, "BOND", 999, message['size'])
                else:
                    bond_sell -= message['size']
                    sell_symbol(exchange, "BOND", 1001, message['size'])


if __name__ == "__main__":
    main()
