#!/bin/python3

from binance.client import Client
from datetime import datetime, timezone
import os
# load in settings,
# load in pot
# get 4hour data from binance
# See if any buy/sells need to be placed
# execute transactions
# save transactions to separate file
# save pot file
## Pot concept :- When saving pot, if a sell is being placed ...update pot total with new pot total.  If buying, leave pot total alone

# api info
api_key = os.environ["api_key"]
api_secret = os.environ["api_secret"]
# filenames
transactions = "invest/transactions.txt"
settings = "invest/settings.txt"
pot = "invest/pot.txt"
testing = True
base_coin = "USDT"

coins =[]
pot_total = 0

#load settings information from Read Only file
def loadCoins(settings):
    coins_array = []
    try:
        with open(settings) as c:
            content = c.readlines()
    except IOError:
        print("Failed to load in file for coin data")
        return ["IOError"]
    except Exception (e):
        print("General exception triggered: ", e)
        return ["General Error"]

    for line in content:
        if "Coin" in line and len(line.split(":")) == 3 and line.startswith("C"):
            coinInfo = line.split(":");
            coin = {
                "ticker":coinInfo[1].strip('\n'),
                "weighting":coinInfo[2].strip('\n'),
                "active":None,
                "purchase_price":None
            }
            coins_array.append(coin)
    if(testing): print(coins_array)
    return coins_array

def loadPot(coins_array, pot_file):
    content = ""
    try:
        with open(pot_file) as p:
            content = p.readlines()
    except IOError:
        print("Failed to load in file for coin data")
        return ["IOError"]
    except Exception (e):
        print("General exception triggered: ", e)
        return ["General Error"]

    if content != "":
        for line in content:
            if not line.startswith("#"):
                if line.startswith("Total"):
                    pot_total = int(line.split(":")[1].strip("/n"))
                else:
                    coinInfo = line.split(":")
                    for coin in coins_array:
                        if coin["ticker"] == coinInfo[0]:
                            coin["active"] = coinInfo[1]
                            coin["purchase_price"] = int(coinInfo[2].strip("\n"))
                            coin["MA7"] = float(coinInfo[3])
                            coin["MA21"] = float(coinInfo[4])

    if testing: print(pot_total)
    if testing: print(coins_array)
    return coins_array

def checkBinance(ticker, current_time, api_key, api_secret, base_coin):
    api_data = None
    try:
        client = Client(api_key, api_secret)
        api_data = client.get_historical_klines(ticker+base_coin, Client.KLINE_INTERVAL_4HOUR, current_time)
        # if testing: print("------------------------------")
        # if testing: print(coin["ticker"])
        # if testing: print("------------------------------")
        if testing: print(api_data)

    except:
        if testing: print("API failed to respond")
        api_data = None # reset any modifications the try statement made

    return api_data

# Calulate the moving averages and return the values
# input:  api_data, (string)coinName
# output: tuple 7 item moving average, 21 item moving average
def getMovingAverages(api_data, coin_name):
    shortCalc = 7
    longCalc = 21
    maShort = 0
    maLong = 0
    if api_data:
        try:
            api_len = len(api_data)
            counter = 0
            for i in range(api_len-1, -1, -1):
                if counter < longCalc:
                    maLong += float(api_data[i][4])
                    if counter < shortCalc:
                        maShort += float(api_data[i][4])
                else:
                    break
                counter += 1
            maLong = maLong/longCalc
            maShort = maShort/shortCalc

        except Exception as e:
            print("Failed to calculate moving averages for: "+coin_name)
            print(e)
            maShort = None
            maLong = None

    return maShort, maLong

def makeTradeDecision(ma7, ma21):
    return ma7 < ma21

def savePot(coins_array, pot):
    with open(pot, "w") as p:
        p.write("### Current Pot - this file edited automatically ###\n")
        p.write("### <Coin Ticker>:Active/None:<$UsedFromPot>\n")
        p.write("Total:"+str(pot_total)+"\n")
        for coin in coins_array:
            p.write(coin["ticker"]+":"+coin["active"]+":"+str(coin["purchase_price"])+":"+str(coin["MA7"])+":"+str(coin["MA21"])+"\n")

def entry():
    current_time = datetime.now(timezone.utc).strftime("%Y/%m/%d")  # UTC date YYYY/MM/DD
    coins = loadCoins(settings)
    if coins == ["IOError"] or ["General Error"]:
        exit()
    coins = loadPot(coins, pot)
    for coin in coins:
        api_data = checkBinance(coin["ticker"], current_time, api_key, api_secret, base_coin)
        ma7, ma21 = getMovingAverages(api_data, coin["ticker"])

        if ma7 and ma21:
            ma7_above_ma21 = makeTradeDecision(ma7, ma21)
            prev_ma7_above_ma21 = makeTradeDecision(coin["MA7"], coin["MA21"])
            if ma7_above_ma21 and not prev_ma7_above_ma21:
                # .. and not in a trade ... buy
                if testing: print("Buy Trade recommended for coin: "+ coin["ticker"])
                pass
            elif prev_ma7_above_ma21 and not ma7_above_ma21:
                # .. and in a trade ... sell
                if testing: print("Sell Trade recommended for coin: "+ coin["ticker"])
                pass

        coin["MA7"] = ma7
        coin["MA21"] = ma21
    coins = savePot(coins, pot)
    return True
