import sell_symbol, buy_symbol, buy_convert, sell_convert

def mean(l):
    return sum(l) // len(l)

def operate_car(exchange, BAT_trade_price, BOND_trade_price, BDU_trade_price, ALI_trade_price, TCT_trade_price):
    tmp = 5
    BAT_mean_price = mean(BAT_trade_price[-tmp:])
    BOND_mean_price = mean(BOND_trade_price[-tmp:])
    BDU_mean_price = mean(BDU_trade_price[-tmp:])
    ALI_mean_price = mean(ALI_trade_price[-tmp:])
    TCT_mean_price = mean(TCT_trade_price[-tmp:])

    size = 2

    if (10 * BAT_mean_price + 100 < (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):
        buy_symbol(exchange, "BAT", BAT_mean_price+1, 10*size)

        sell_convert(exchange, "BAT", 10*size)

        sell_symbol(exchange, "BOND", BOND_mean_price-1, 3*size)
        sell_symbol(exchange, "BDU", BDU_mean_price-1, 2*size)
        sell_symbol(exchange, "ALI", ALI_mean_price-1, 3*size)
        sell_symbol(exchange, "TCT", TCT_mean_price-1, 2*size)

    elif (10 * BAT_mean_price - 100 > (3 * BOND_mean_price + 2 * BDU_mean_price + 3 * ALI_mean_price + 2 * TCT_mean_price)):

        buy_symbol(exchange, "BOND", BOND_mean_price + 1, 3 * size)
        buy_symbol(exchange, "BDU", BDU_mean_price + 1, 2 * size)
        buy_symbol(exchange, "ALI", ALI_mean_price + 1, 3 * size)
        buy_symbol(exchange, "TCT", TCT_mean_price + 1, 2 * size)

        buy_convert(exchange, "BAT", 10*size)

        sell_symbol(exchange, "BAT", BAT_mean_price - 1, 10*size)

