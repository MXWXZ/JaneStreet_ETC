import time
from bot import read_from_exchange



class Data():
    def __init__(self):
        self.bond = []
        self.car = []
        self.che = []
        self.bdu = []
        self.ali = []
        self.tct = []
        self.bat = []
    
    def get_data(self):
        return self.bond,self.car,self.che,self.bdu,self.ali,self.tct,self.bat

    def read_in_trade(self,exchange):
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
                    self.bond.append(info["price"])

                if (info["symbol"] == "CAR"):
                    self.car.append(info["price"])

                if (info["symbol"] == "CHE"):
                    self.che.append(info["price"])

                if (info["symbol"] == "BDU"):
                    self.bdu.append(info["price"])

                if (info["symbol"] == "ALI"):
                    self.ali.append(info["price"])

                if (info["symbol"] == "TCT"):
                    self.tct.append(info["price"])

                if (info["symbol"] == "BAT"):
                    self.bat.append(info["price"])

            time.sleep(0.01)
            count += 1