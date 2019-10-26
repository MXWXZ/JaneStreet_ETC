class Data:
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

    def read_now_market(self):
        return self.books

    def read_in_trade(self, info):
        type1 = info["type"]

        if (type1 == "trade"):

            if (info["symbol"] == "BOND"):
                if (len(self.bond) >= 1000):
                    self.bond.remove(self.bond[0])
                self.bond.append(info["price"])

            if (info["symbol"] == "CAR"):
                if (len(self.car) >= 1000):
                    self.car.remove(self.car[0])
                self.car.append(info["price"])

            if (info["symbol"] == "CHE"):
                if (len(self.che) >= 1000):
                    self.che.remove(self.che[0])
                self.che.append(info["price"])

            if (info["symbol"] == "BDU"):
                if (len(self.bdu) >= 1000):
                    self.bdu.remove(self.bdu[0])
                self.bdu.append(info["price"])

            if (info["symbol"] == "ALI"):
                if (len(self.ali) >= 1000):
                    self.ali.remove(self.ali[0])
                self.ali.append(info["price"])

            if (info["symbol"] == "TCT"):
                if (len(self.tct) >= 1000):
                    self.tct.remove(self.tct[0])
                self.tct.append(info["price"])

            if (info["symbol"] == "BAT"):
                if (len(self.bat) >= 1000):
                    self.bat.remove(self.bat[0])
                self.bat.append(info["price"])

        if (type1 == "book"):
            self.books[info["symbol"]] = [info["buy"], info["sell"]]
