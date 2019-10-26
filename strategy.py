import bot
import sys
from collections import deque

maxlen_de = 15

positive_order = deque(maxlen=maxlen_de)
negative_order = deque(maxlen=maxlen_de)


def bond_buy_sell(exchange, message, data):
    if message['type'] == 'fill' and message['symbol'] == 'BOND':
        if message['dir'] == 'BUY':
            bot.buy_symbol(exchange, "BOND", 999, message['size'])
        else:
            bot.sell_symbol(exchange, "BOND", 1001, message['size'])


def mean(l):
    return sum(l) // len(l)


def operate_car(exchange, message, data):
    if (message['type'] == 'reject'):
        try:
            positive_order.remove(message['order_id'])
            negative_order.remove(message['order_id'])
        except:
            pass
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
            positive_order.append(bot.buy_symbol(
                exchange, "BAT", BAT_mean_price + 1, 10 * size))

            bot.sell_convert(exchange, "BAT", 10 * size)

            positive_order.append(bot.sell_symbol(
                exchange, "BOND", BOND_mean_price - 1, 3 * size))
            positive_order.append(bot.sell_symbol(
                exchange, "BDU", BDU_mean_price - 1, 2 * size))
            positive_order.append(bot.sell_symbol(
                exchange, "ALI", ALI_mean_price - 1, 3 * size))
            positive_order.append(bot.sell_symbol(
                exchange, "TCT", TCT_mean_price - 1, 2 * size))

        elif (10 * BAT_mean_price > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
            for order_id in positive_order:
                bot.cancel_id(exchange, order_id)

        if (10 * BAT_mean_price - 100 > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):

            negative_order.append(bot.buy_symbol(
                exchange, "BOND", BOND_mean_price + 1, 3 * size))
            negative_order.append(bot.buy_symbol(
                exchange, "BDU", BDU_mean_price + 1, 2 * size))
            negative_order.append(bot.buy_symbol(
                exchange, "ALI", ALI_mean_price + 1, 3 * size))
            negative_order.append(bot.buy_symbol(
                exchange, "TCT", TCT_mean_price + 1, 2 * size))

            bot.buy_convert(exchange, "BAT", 10 * size)

            negative_order.append(bot.sell_symbol(
                exchange, "BAT", BAT_mean_price - 1, 10 * size))

        elif (10 * BAT_mean_price < (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
            for order_id in negative_order:
                bot.cancel_id(exchange, order_id)


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
    
    if len(price_list)<5:
        return 100
    else:
        ratel = []
        for item in range(len(price_list[-7:-1])):
            ratel.append((price_list[item+1]-price_list[item])/(price_list[item]+1e-10))
        if (ratel[-1]<0 and ratel[-2]<0 and ratel[-3]<0):
            return sum(ratel)
            

def is_sell(price_list):
    
    if len(price_list)<5:
        return -100
    else:
        ratel = []
        for item in range(len(price_list[-7:-1])):
            ratel.append((price_list[item+1]-price_list[item])/(price_list[item]+1e-10))
        if (ratel[-1]>0 and ratel[-2]>0 and ratel[-3]>0):
            return sum(ratel)


def rescent_buy(exchange,message,data):
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

        list1 = [is_buy(batprice),is_buy(bdu_price),is_buy(ali_price),is_buy(tct_price),is_buy(car_price),is_buy(che_price)]
        list2 = [is_sell(batprice),is_sell(bdu_price),is_sell(ali_price),is_sell(tct_price),is_sell(car_price),is_sell(che_price)]
        if min(list1)!=100:
            pos = list1.index(min(list1))

            if pos==0:
                bot.buy_symbol(exchange,'BAT', buyBAT[0][0] + 2, 10)
            if pos==1:
                bot.buy_symbol(exchange,'CAR', buyCAR[0][0] + 2, 10)
            if pos==2:
                bot.buy_convert(exchange,'CHE', buyCHE[0][0] + 2, 10)
            if pos==3:
                bot.buy_convert(exchange,'DBU', buyDBU[0][0] + 2, 10)
            if pos==4:
                bot.buy_convert(exchange,'ALI', buyALI[0][0] + 2, 10)
            if pos==5:
                bot.buy_convert(exchange,'TCT', buyTCT[0][0] + 2, 10)


        if max(list2)!=-100:
            pos = list2.index(max(list1))
        
            if pos==0:
                bot.sell_convert(exchange,'BAT', sellBAT[0][0] - 2, 10)
            if pos==1:
                bot.sell_convert(exchange,'CAR', sellCAR[0][0] - 2, 10)
            if pos==2:
                bot.sell_convert(exchange,'CHE', sellCHE[0][0] - 2, 10)
            if pos==3:
                bot.sell_convert(exchange,'DBU', sellDBU[0][0] - 2, 10)
            if pos==4:
                bot.sell_convert(exchange,'ALI', sellALI[0][0] - 2, 10)
            if pos==5:
                bot.sell_convert(exchange,'TCT', sellTCT[0][0] - 2, 10)





        # if 'BOND' in book:
        #     buyBOND, sellBOND = book['BOND']




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
