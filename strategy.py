import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt  
from readInTrade import Data

def mean_value():


    return

def std_value():

    return

def PE_Value():

    return



def increase_rate():


    return


def is_exchange_BAT(BAT_price,BOND_price,BDU_price,ALI_price,TCT_price):
    """
    return how many we buy least BAT can get get_value profit
    """
    price_isGood = BAT_price*10 - BOND_price*3 - BDU_price * 2 - ALI_price * 3 -TCT_price * 2
    n = 100 / price_isGood
    n = int(n+1)*10
    get_value = n*price_isGood - 100

    return n,get_value

def is_exchange_CHE_or_CAR(CHE_price,CAR_price):
    """
    whether change CAR to CHE and how many is the least 
    """
    num = 0
    flag = "Buy_CHE"
    if (CHE_price>CAR_price):
        num = 10 / (CHE_price-CAR_price)
        num = int(num+1)
        flag = "Buy_CHE"
    else:
        num = 10 / (CAR_price-CHE_price)
        num = int(num+1)
        flag = "Buy_CAR"

    return flag,num



"""
下面这一段加到bot里面
"""

data_now = Data()
data_now.read_in_trade(exchange)
bond,car,che,bdu,ali,tct,bat = data_now.get_data

