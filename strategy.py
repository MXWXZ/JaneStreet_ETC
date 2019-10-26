import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import bot
import sys


def bond_buy_sell(exchange, message, data):
    if message['type'] == 'fill':
        print("rep> ", message, file=sys.stderr)
        if message['symbol'] == 'BOND':
            if message['dir'] == 'BUY':
                bot.buy_symbol(exchange, "BOND", 999, message['size'])
            else:
                bot.sell_symbol(exchange, "BOND", 1001, message['size'])


def mean_value():

    return


def std_value():

    return


def PE_Value():

    return


def increase_rate():

    return


def is_exchange_BAT(BAT_price, BOND_price, BDU_price, ALI_price, TCT_price):
    """
    return how many we buy least BAT can get get_value profit
    """
    price_isGood = BAT_price * 10 - BOND_price * 3 - \
        BDU_price * 2 - ALI_price * 3 - TCT_price * 2
    n = 100 / price_isGood
    n = int(n + 1) * 10
    get_value = n * price_isGood - 100

    return n, get_value


def is_exchange_CHE_or_CAR(CHE_price, CAR_price):
    """
    whether change CAR to CHE and how many is the least 
    """
    num = 0
    flag = "Buy_CHE"
    if (CHE_price > CAR_price):
        num = 10 / (CHE_price - CAR_price)
        num = int(num + 1)
        flag = "Buy_CAR"
    else:
        num = 10 / (CAR_price - CHE_price)
        num = int(num + 1)
        flag = "Buy_CHE"

    return flag, num


"""
下面这一段加到bot里面
"""


def is_exchange_four_stocks(BAT_price, BOND_price, BDU_price, ALI_price, TCT_price, BAT_NUM, BOND_NUM, BDU_NUM, ALI_NUM, TCT_NUM, exchange):
    # NUM是现有的持仓, 买入股票，卖出BAT
    price_isGood = BAT_price * 10 - BOND_price * 3 - \
        BDU_price * 2 - ALI_price * 3 - TCT_price * 2   # 可以套利的价格
    if price_isGood < 0:  # bat的价格比较低，买入bat，由邦总的程序处理
        tmp = min([(100 - BOND_NUM) / 3, (100 - BDU_NUM) / 2,
                   (100 - ALI_NUM) / 3, (100 - TCT_NUM) / 2])
        # 由于仓位的限制，tmp是最多的股票买入单位，其他的买多了也没法合成
        tmp = min(100 - BAT_NUM, 10 * tmp)

    else:  # bat 的价格比较高，买入四只股票的某一种或者某几种，
        tmp = min([(100 - BOND_NUM) / 3, (100 - BDU_NUM) / 2,
                   (100 - ALI_NUM) / 3, (100 - TCT_NUM) / 2])
        # 由于仓位的限制，tmp是最多的股票买入单位，其他的买多了也没法合成
        tmp = min(100 - BAT_NUM, 10 * tmp)

        # 取还可以买的bat数量和tmp的较小值
        bot.buy_symbol(exchange, 'BOND', BOND_price, 100 - BOND_NUM)
        bot.buy_symbol(exchange, 'BDU', BDU_price, 66 - BDU_NUM)
        bot.buy_symbol(exchange, 'ALI', ALI_price, 100 - ALI_NUM)
        bot.buy_symbol(exchange, 'TCT', TCT_price, 66 - TCT_NUM)

        tmp = int(min([(100 + BOND_NUM) / 3, (100 + BDU_NUM) / 2,
                       (100 + ALI_NUM) / 3, (100 + TCT_NUM) / 2]) / 1)
        if tmp > 45:
            bot.convert(exchange, 'BAT', BAT_price, tmp * 10)

        bot.sell_symbol(exchange, 'BAT', BAT_price, BAT_NUM)



def buy_sell_CHE_or_CAR(exchange, message, data_now):
    bond, car, che, bdu, ali, tct, bat = data_now.get_data()
    batprice = sum(bat[-30:]) / 30
    bong_price = sum(bond[-30:]) / 30
    bdu_price = sum(bdu[-30:]) / 30
    ali_price = sum(ali[-30:]) / 30
    tct_price = sum(tct[-30:]) / 30
    car_price = sum(tct[-30:]) / 30
    che_price = sum(tct[-30:]) / 30

    book = data_now.read_now_market()
    buyBAT, sellBAT = book['BAT']
    buyCAR, sellCAR = book['CAR']
    buyCHE, sellCHE = book['CHE']
    buyBDU, sellBDU = book['DBU']
    buyALI, sellALI = book['ALI']
    buyTCT, sellTCT = book['TCT']
    buyBOND, sellBOND = book['BOND']
    """
    [[4316, 1], [4314, 1], [4311, 1], [4297, 1], [4294, 3], [4291, 2], [4286, 4]] 买一
    [[4337, 1], [4338, 1], [4345, 1], [4355, 1]] 卖一
    """

    if (len(car_price) > 0 and len(che_price) > 0):
        flag, num = is_exchange_CHE_or_CAR(che_price, car_price)
        if (flag == "Buy_CHE") and (num<5):
            bot.buy_symbol(exchange, 'CHE', buyCHE[0][0] + 1, 7)
            bot.sell_symbol(exchange, 'CAR', sellCAR[0][0] - 1, 7)
        if (flag == "Buy_CAR") and (num<5):
            bot.buy_symbol(exchange, 'CAR', buyCAR[0][0] + 1, 7)
            bot.sell_symbol(exchange, 'CHE', sellCHE[0][0] - 1, 7)