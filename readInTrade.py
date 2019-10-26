import time
from bot import read_from_exchange

bond = []
car = []
che = []
bdu = []
ali = []
tct = []
bat = []

def read_in_trade(exchange):
    count = 0
    while (count < 200):
        info = read_from_exchange(exchange)
        if not info:
            break
        type = info["type"]
        if (type == "close"):
            print("Server closed.")
            return
        if (type == "trade"):

            if (info["symbol"] == "BOND"):
                bond.append(info["price"])

            if (info["symbol"] == "CAR"):
                car.append(info["price"])

            if (info["symbol"] == "CHE"):
                che.append(info["price"])

            if (info["symbol"] == "BDU"):
                bdu.append(info["price"])

            if (info["symbol"] == "ALI"):
                ali.append(info["price"])

            if (info["symbol"] == "TCT"):
                tct.append(info["price"])

            if (info["symbol"] == "BAT"):
                bat.append(info["price"])

        time.sleep(0.01)
        count += 1