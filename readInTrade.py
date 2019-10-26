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
        self.count = 0 
    
    def get_data(self):
        return self.bond,self.car,self.che,self.bdu,self.ali,self.tct,self.bat

    def read_in_trade(self,exchange):
        
        if (self.count < 200):
            info = read_from_exchange(exchange)
            if not info:
                return
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


            self.count += 1
        else:
            info = read_from_exchange(exchange)
            if not info:
                return
            type = info["type"]
            if (type == "close"):
                print("Server closed.")
                return
            if (type == "trade"):

                if (info["symbol"] == "BOND"):
                    self.bond.append(info["price"])
                    self.bond.remove(self.bond[0])

                if (info["symbol"] == "CAR"):
                    self.car.append(info["price"])
                    self.car.remove(self.car[0])

                if (info["symbol"] == "CHE"):
                    self.che.append(info["price"])
                    self.che.remove(self.che[0])

                if (info["symbol"] == "BDU"):
                    self.bdu.append(info["price"])
                    self.bdu.remove(self.bdu[0])

                if (info["symbol"] == "ALI"):
                    self.ali.append(info["price"])
                    self.ali.remove(self.ali[0])

                if (info["symbol"] == "TCT"):
                    self.tct.append(info["price"])
                    self.tct.remove(self.tct[0])

                if (info["symbol"] == "BAT"):
                    self.bat.append(info["price"])
                    self.bat.remove(self.bat[0])
