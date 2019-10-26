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
        self.books = {}

    def get_data(self):
        return self.bond, self.car, self.che, self.bdu, self.ali, self.tct, self.bat

    def read_now_market(self, book):
        return self.books

    def read_in_trade(self, info):
        type1 = info["type"]


        if (type1 == "trade"):

            if (info["symbol"] == "BOND"):
                if (len(self.bond) >= 50):
                    self.bond.remove(self.bond[0])
                self.bond.append(info["price"])

            if (info["symbol"] == "CAR"):
                if (len(self.car) >= 50):
                    self.car.remove(self.bond[0])
                self.car.append(info["price"])

            if (info["symbol"] == "CHE"):
                if (len(self.che) >= 50):
                    self.che.remove(self.bond[0])
                self.che.append(info["price"])

            if (info["symbol"] == "BDU"):
                if (len(self.bdu) >= 50):
                    self.bdu.remove(self.bond[0])
                self.bdu.append(info["price"])

            if (info["symbol"] == "ALI"):
                if (len(self.ali) >= 50):
                    self.ali.remove(self.bond[0])
                self.ali.append(info["price"])

            if (info["symbol"] == "TCT"):
                if (len(self.tct) >= 50):
                    self.tct.remove(self.bond[0])
                self.tct.append(info["price"])

            if (info["symbol"] == "BAT"):
                if (len(self.bat) >= 50):
                    self.bat.remove(self.bond[0])
                self.bat.append(info["price"])

        if (type1 == "book"):
            self.books[info["symbol"]] = [info["buy"], info["sell"]]
