import bot
import sys


def bond_buy_sell(exchange, message, data):
    if message['type'] == 'fill' and message['symbol'] == 'BOND':
        if message['dir'] == 'BUY':
            bot.buy_symbol(exchange, "BOND", 999, message['size'])
        else:
            bot.sell_symbol(exchange, "BOND", 1001, message['size'])


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


def buy_sell_CHE_or_CAR(exchange, message, data):
    bond, car, che, bdu, ali, tct, bat = data.get_data()
    batprice = sum(bat[-30:]) / 30
    bong_price = sum(bond[-30:]) / 30
    bdu_price = sum(bdu[-30:]) / 30
    ali_price = sum(ali[-30:]) / 30
    tct_price = sum(tct[-30:]) / 30
    car_price = sum(car[-30:]) / 30
    che_price = sum(che[-30:]) / 30

    book = data.read_now_market()
    print(book)
    if 'BAT' in book:
        buyBAT, sellBAT = book['BAT']
    if 'CAR' in book:
        buyCAR, sellCAR = book['CAR']
    if 'CHE' in book:       
        buyCHE, sellCHE = book['CHE']
    if 'DBU' in book:
        buyBDU, sellBDU = book['DBU']
    if 'ALI' in book:    
        buyALI, sellALI = book['ALI']
    if 'TCT' in book:
        buyTCT, sellTCT = book['TCT']
    if 'BOND' in book:    
        buyBOND, sellBOND = book['BOND']
    """
    [[4316, 1], [4314, 1], [4311, 1], [4297, 1], [4294, 3], [4291, 2], [4286, 4]]
    [[4337, 1], [4338, 1], [4345, 1], [4355, 1]]
    """

    if (len(car_price) > 0 and len(che_price) > 0):
        flag, num = is_exchange_CHE_or_CAR(che_price, car_price)
        if (flag == "Buy_CHE") and (num < 5):
            bot.buy_symbol(exchange, 'CHE', buyCHE[0][0] + 1, 7)
            bot.buy_convert(exchange, 'CHE', 10)
            bot.sell_symbol(exchange, 'CAR', sellCAR[0][0] - 1, 7)
        if (flag == "Buy_CAR") and (num < 5):
            bot.buy_symbol(exchange, 'CAR', buyCAR[0][0] + 1, 7)
            bot.buy_convert(exchange, 'CAR', 10)
            bot.sell_symbol(exchange, 'CHE', sellCHE[0][0] - 1, 7)
