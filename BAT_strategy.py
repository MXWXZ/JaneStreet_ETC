import sell_symbol
import buy_symbol
import buy_convert
import sell_convert
import cancel_id
from collections import deque

maxlen_de = 15

positive_order = deque(maxlen=maxlen_de)
negative_order = deque(maxlen=maxlen_de)


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
        current_market = data.read_now_market()
        tmp = 5

        if len(bat) == 0 or len(bond) == 0 or len(bdu) == 0 or len(ali) == 0 or len(tct) == 0:
            return

        BAT_mean_price = mean(bat[-tmp:])
        BOND_mean_price = mean(bond[-tmp:])
        BDU_mean_price = mean(bdu[-tmp:])
        ALI_mean_price = mean(ali[-tmp:])
        TCT_mean_price = mean(tct[-tmp:])

        BAT_buy_price = current_market['BAT'][0][0][0]
        BAT_sell_price = current_market['BAT'][1][0][0]

        BOND_buy_price = current_market['BOND'][0][0][0]
        BOND_sell_price = current_market['BOND'][1][0][0]

        BDU_buy_price = current_market['BDU'][0][0][0]
        BDU_sell_price = current_market['BDU'][1][0][0]

        ALI_buy_price = current_market['ALI'][0][0][0]
        ALI_sell_price = current_market['ALI'][1][0][0]

        TCT_buy_price = current_market['TCT'][0][0][0]
        TCT_sell_price = current_market['TCT'][1][0][0]

        size = 2

        if (10 * BAT_mean_price + 100 < (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
            positive_order.append(buy_symbol(
                exchange, "BAT", BAT_buy_price + 1, 10 * size))

            sell_convert(exchange, "BAT", 10 * size)

            positive_order.append(sell_symbol(
                exchange, "BOND", BOND_sell_price - 1, 3 * size))
            positive_order.append(sell_symbol(
                exchange, "BDU", BDU_sell_price - 1, 2 * size))
            positive_order.append(sell_symbol(
                exchange, "ALI", ALI_sell_price - 1, 3 * size))
            positive_order.append(sell_symbol(
                exchange, "TCT", TCT_sell_price - 1, 2 * size))

            for order_id in positive_order:
                cancel_id(exchange, order_id)

        # elif (10 * BAT_mean_price > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
        #     for order_id in positive_order:
        #         cancel_id(exchange, order_id)

        if (10 * BAT_mean_price - 100 > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):

            negative_order.append(buy_symbol(
                exchange, "BOND", BOND_buy_price + 1, 3 * size))
            negative_order.append(buy_symbol(
                exchange, "BDU", BDU_buy_price + 1, 2 * size))
            negative_order.append(buy_symbol(
                exchange, "ALI", ALI_buy_price + 1, 3 * size))
            negative_order.append(buy_symbol(
                exchange, "TCT", TCT_buy_price + 1, 2 * size))

            buy_convert(exchange, "BAT", 10 * size)

            negative_order.append(sell_symbol(
                exchange, "BAT", BAT_sell_price - 1, 10 * size))

            for order_id in negative_order:
                cancel_id(exchange, order_id)

        # elif (10 * BAT_mean_price < (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
        #     for order_id in negative_order:
        #         cancel_id(exchange, order_id)
