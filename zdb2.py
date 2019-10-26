
import bot
import sys


def is_buy(price_list):

    if len(price_list) < 9:
        return 10000
    else:
        ratel = []
        for item in range(len(price_list[-7:-1])):
            ratel.append(
                (price_list[item + 1] - price_list[item]) / (price_list[item] + 1e-10))
        if (ratel[-1] < 0 and ratel[-2] < 0 and ratel[-3] < 0 and ratel[-4] < 0 and ratel[-5] < 0 and ratel[-6] < 0):
            return sum(ratel) - 0.1
        else:
            return 10000


def is_sell(price_list):

    if len(price_list) < 9:
        return -10000
    else:
        ratel = []
        for item in range(len(price_list[-7:-1])):
            ratel.append(
                (price_list[item + 1] - price_list[item]) / (price_list[item] + 1e-10))
        if (ratel[-1] > 0 and ratel[-2] > 0 and ratel[-3] > 0):
            return sum(ratel) + 0.1
        else:
            return -10000


def rescent_buy(exchange, message, data):
    if (message['type'] == 'trade'):
        bond, car, che, bdu, ali, tct, bat = data.get_data()
        batprice = sum(bat[-30:]) / 30
        bond_price = sum(bond[-30:]) / 30
        bdu_price = sum(bdu[-30:]) / 30
        ali_price = sum(ali[-30:]) / 30
        tct_price = sum(tct[-30:]) / 30
        car_price = sum(car[-30:]) / 30
        che_price = sum(che[-30:]) / 30

        book = data.read_now_market()
        if 'BAT' in book:
            buyBAT, sellBAT = book['BAT']
        if 'CAR' in book:
            buyCAR, sellCAR = book['CAR']
        if 'CHE' in book:
            buyCHE, sellCHE = book['CHE']
        if 'DBU' in book:
            buyBDU, sellBDU = book['BDU']
        if 'ALI' in book:
            buyALI, sellALI = book['ALI']
        if 'TCT' in book:
            buyTCT, sellTCT = book['TCT']

        list1 = [is_buy(bat), is_buy(bdu), is_buy(
            ali), is_buy(tct), is_buy(car), is_buy(che)]
        list2 = [is_sell(bat), is_sell(bdu), is_sell(
            ali), is_sell(tct), is_sell(car), is_sell(che)]
        if min(list1) != 10000:
            pos = list1.index(min(list1))

            if pos == 0:
                bot.buy_convert(exchange, 'BAT', buyBAT[0][0] + 2, 10)
            if pos == 1:
                bot.buy_convert(exchange, 'CAR', buyCAR[0][0] + 2, 10)
            if pos == 2:
                bot.buy_convert(exchange, 'CHE', buyCHE[0][0] + 2, 10)
            if pos == 3:
                bot.buy_convert(exchange, 'BDU', buyBDU[0][0] + 2, 10)
            if pos == 4:
                bot.buy_convert(exchange, 'ALI', buyALI[0][0] + 2, 10)
            if pos == 5:
                bot.buy_convert(exchange, 'TCT', buyTCT[0][0] + 2, 10)

        if max(list2) != -10000:
            pos = list2.index(max(list1))

            if pos == 0:
                bot.sell_convert(exchange, 'BAT', sellBAT[0][0] - 2, 10)
            if pos == 1:
                bot.sell_convert(exchange, 'CAR', sellCAR[0][0] - 2, 10)
            if pos == 2:
                bot.sell_convert(exchange, 'CHE', sellCHE[0][0] - 2, 10)
            if pos == 3:
                bot.sell_convert(exchange, 'BDU', sellBDU[0][0] - 2, 10)
            if pos == 4:
                bot.sell_convert(exchange, 'ALI', sellALI[0][0] - 2, 10)
            if pos == 5:
                bot.sell_convert(exchange, 'TCT', sellTCT[0][0] - 2, 10)
