import bot
import sys


def bond_buy_sell(exchange, message, data):
    if message['type'] == 'fill' and message['symbol'] == 'BOND':
        if message['dir'] == 'BUY':
            bot.buy_symbol(exchange, "BOND", 999, message['size'])
        else:
            bot.sell_symbol(exchange, "BOND", 1001, message['size'])


def mean(l):
    return sum(l) // len(l)


def operate_car(exchange, message, data):
    if (message['type'] == 'trade') and (message['symbol'] == 'BAT'):
        bond, car, che, bdu, ali, tct, bat = data.get_data()
        tmp = 5
        if len(bat) == 0 or len(bond) == 0 or len(bdu) == 0 or len(ali) == 0 or len(tct) == 0:
            return
        BAT_mean_price = mean(bat[-tmp:])
        BOND_mean_price = mean(bond[-tmp:])
        BDU_mean_price = mean(bdu[-tmp:])
        ALI_mean_price = mean(ali[-tmp:])
        TCT_mean_price = mean(tct[-tmp:])

        size = 2

        if (10 * BAT_mean_price + 100 < (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
            bot.buy_symbol(exchange, "BAT", BAT_mean_price, 10 * size)

            bot.sell_convert(exchange, "BAT", 10 * size)

            bot.sell_symbol(exchange, "BOND", BOND_mean_price, 3 * size)
            bot.sell_symbol(exchange, "BDU", BDU_mean_price, 2 * size)
            bot.sell_symbol(exchange, "ALI", ALI_mean_price, 3 * size)
            bot.sell_symbol(exchange, "TCT", TCT_mean_price, 2 * size)

        elif (10 * BAT_mean_price - 100 > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):

            bot.buy_symbol(exchange, "BOND", BOND_mean_price, 3 * size)
            bot.buy_symbol(exchange, "BDU", BDU_mean_price, 2 * size)
            bot.buy_symbol(exchange, "ALI", ALI_mean_price, 3 * size)
            bot.buy_symbol(exchange, "TCT", TCT_mean_price, 2 * size)

            bot.buy_convert(exchange, "BAT", 10 * size)

            bot.sell_symbol(exchange, "BAT", BAT_mean_price, 10 * size)


def is_exchange_CHE_or_CAR(CHE_price, CAR_price):
    """
    whether change CAR to CHE and how many is the least 
    """
    num = 0
    flag = "INVALID"
    if (CHE_price > CAR_price):
        num = 10 / (CHE_price - CAR_price)
        num = int(num + 1)
        flag = "Buy_CAR"
    elif (CHE_price < CAR_price):
        num = 10 / (CAR_price - CHE_price)
        num = int(num + 1)
        flag = "Buy_CHE"

    return flag, num


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
        if 'BDU' in book:
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
                bot.buy_symbol(exchange, 'BAT', buyBAT[0][0] + 2, 10)
            if pos == 1:
                bot.buy_symbol(exchange, 'CAR', buyCAR[0][0] + 2, 10)
            if pos == 2:
                bot.buy_symbol(exchange, 'CHE', buyCHE[0][0] + 2, 10)
            if pos == 3:
                bot.buy_symbol(exchange, 'BDU', buyBDU[0][0] + 2, 10)
            if pos == 4:
                bot.buy_symbol(exchange, 'ALI', buyALI[0][0] + 2, 10)
            if pos == 5:
                bot.buy_symbol(exchange, 'TCT', buyTCT[0][0] + 2, 10)

        if max(list2) != -10000:
            pos = list2.index(max(list2))

            if pos == 0:
                bot.sell_symbol(exchange, 'BAT', sellBAT[0][0] - 2, 10)
            if pos == 1:
                bot.sell_symbol(exchange, 'CAR', sellCAR[0][0] - 2, 10)
            if pos == 2:
                bot.sell_symbol(exchange, 'CHE', sellCHE[0][0] - 2, 10)
            if pos == 3:
                bot.sell_symbol(exchange, 'BDU', sellBDU[0][0] - 2, 10)
            if pos == 4:
                bot.sell_symbol(exchange, 'ALI', sellALI[0][0] - 2, 10)
            if pos == 5:
                bot.sell_symbol(exchange, 'TCT', sellTCT[0][0] - 2, 10)


def buy_sell_CHE_or_CAR(exchange, message, data):
    if (message['type'] == 'trade') and ((message['symbol'] == 'CHE') or (message['symbol'] == 'CAR')):
        bond, car, che, bdu, ali, tct, bat = data.get_data()
        # batprice = sum(bat[-30:]) / 30
        # bong_price = sum(bond[-30:]) / 30
        # bdu_price = sum(bdu[-30:]) / 30
        # ali_price = sum(ali[-30:]) / 30
        # tct_price = sum(tct[-30:]) / 30
        car_price = sum(car[-30:]) / 30
        che_price = sum(che[-30:]) / 30

        book = data.read_now_market()
        # print(book)
        # if 'BAT' in book:
        #     buyBAT, sellBAT = book['BAT']
        if 'CAR' in book:
            buyCAR, sellCAR = book['CAR']
        if 'CHE' in book:
            buyCHE, sellCHE = book['CHE']
        # if 'DBU' in book:
        #     buyBDU, sellBDU = book['DBU']
        # if 'ALI' in book:
        #     buyALI, sellALI = book['ALI']
        # if 'TCT' in book:
        #     buyTCT, sellTCT = book['TCT']
        # if 'BOND' in book:
        #     buyBOND, sellBOND = book['BOND']
        """
        [[4316, 1], [4314, 1], [4311, 1], [4297, 1], [4294, 3], [4291, 2], [4286, 4]]
        [[4337, 1], [4338, 1], [4345, 1], [4355, 1]]
        """

        if (len(car) > 0 and len(che) > 0 and ('CHE' in book) and ('CAR' in book)):
            flag, num = is_exchange_CHE_or_CAR(che_price, car_price)
            if (flag == "Buy_CHE") and (num < 5):
                bot.buy_symbol(exchange, 'CHE', buyCHE[0][0] + 1, 7)
                bot.buy_convert(exchange, 'CHE', 10)
                bot.sell_symbol(exchange, 'CAR', sellCAR[0][0] - 1, 7)
            if (flag == "Buy_CAR") and (num < 5):
                bot.buy_symbol(exchange, 'CAR', buyCAR[0][0] + 1, 7)
                bot.buy_convert(exchange, 'CAR', 10)
                bot.sell_symbol(exchange, 'CHE', sellCHE[0][0] - 1, 7)
