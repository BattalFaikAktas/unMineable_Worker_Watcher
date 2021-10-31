#BFA

import os
import time
import requests
import argparse
from termcolor import colored
from awesome_progress_bar import ProgressBar

parser = argparse.ArgumentParser()
parser.add_argument("-c", required=True, dest="coin", type=str, help="Coin Name")
parser.add_argument("-w", required=True, dest="wallet", type=str, help="Wallet Address")
parser.add_argument("-a", required=True, dest="algorithm", type=str, help="ethash randomx x16rv2 etchash")
parser.add_argument("-t", required=True, dest="time", type=int, help="Refresh Time (minute(s))")
args = parser.parse_args()

version = 0.1

def UpdateCheck():
    #Update New Version
    pass

def Banner():
    os.system("reset")

    print(colored("[*] Start time: " + time.strftime("%c"), "white", attrs=["bold"]))
    print(colored("""
                    ___  ____                  _     _                  
                    |  \/  (_)                | |   | |                 
         _   _ _ __ | .  . |_ _ __   ___  __ _| |__ | | ___             
        | | | | '_ \| |\/| | | '_ \ / _ \/ _` | '_ \| |/ _ \            
        | |_| | | | | |  | | | | | |  __/ (_| | |_) | |  __/            
         \__,_|_| |_\_|  |_/_|_| |_|\___|\__,_|_.__/|_|\___|            
                                                                        
                                                                        
 _    _            _               _    _       _       _               
| |  | |          | |             | |  | |     | |     | |              
| |  | | ___  _ __| | _____ _ __  | |  | | __ _| |_ ___| |__   ___ _ __ 
| |/\| |/ _ \| '__| |/ / _ \ '__| | |/\| |/ _` | __/ __| '_ \ / _ \ '__|
\  /\  / (_) | |  |   <  __/ |    \  /\  / (_| | || (__| | | |  __/ |   
 \/  \/ \___/|_|  |_|\_\___|_|     \/  \/ \__,_|\__\___|_| |_|\___|_|   
                                                                        
                                                                        
 """, "white"))
    print(colored("v" + str(version), "white", attrs=["bold"]))
    print(colored("---" * 30, "white"))

def GetData():
    #Get All Data
    url = "https://api.unmineable.com/v3/stats/" + args.wallet + "?tz=3&coin=" + args.coin
    rawData = requests.get(url).json()

    WorkerStatus(rawData)

def WorkerStatus(rawData):
    onlineCounter = 0
    totalHashRate = 0
    downCounter = 0

    workers = rawData["data"]["workers"][args.algorithm]

    for worker in workers:
        if (worker["online"]):
            onlineCounter += 1
            totalHashRate += worker["h"]
        else:
            downCounter += 1
            print(colored("Worker '" + worker["name"] + "' is ", "white", attrs=["bold"]) + colored("DOWN !!!!!!!!!", "red", attrs=["bold", "blink"]))

    if (downCounter):
        print(colored("---" * 30, "white"))
        print(colored("Down Worker = ", "red", attrs=["bold"]) + colored(str(downCounter), "white", attrs=["bold"]))

    print(colored("Online Worker = ", "green", attrs=["bold"]) + colored(str(onlineCounter), "white", attrs=["bold"]))

    rewardUrl = "https://api.unminable.com/v3/calculate/reward"
    rewardRawData = requests.post(rewardUrl, data={"mh": str(totalHashRate), "algo": args.algorithm, "coin": args.coin}).json()

    SomeInfo(rawData, totalHashRate, rewardRawData)

def SomeInfo(rawData, totalHashRate, rewardRawData):
    print(colored("---" * 30, "white"))
    print(colored("Coin = ", "green", attrs=["bold"]) + colored(args.coin, "white", attrs=["bold"]))
    print(colored("Algorithm = ", "green", attrs=["bold"]) + colored(args.algorithm, "white", attrs=["bold"]))
    print(colored("Wallet = ", "green", attrs=["bold"]) + colored(rawData["data"]["address_"], "white", attrs=["bold"]))
    print(colored("---" * 30, "white"))
    print(colored("Total Paid = ", "green", attrs=["bold"]) + colored(str(rawData["data"]["total_paid"]), "white", attrs=["bold"]))
    print(colored("Pending Balance = ", "green", attrs=["bold"]) + colored(rawData["data"]["pending_balance"], "white", attrs=["bold"]))
    print(colored("---" * 30, "white"))
    print(colored("Hash Rate = ", "green", attrs=["bold"]) + colored(str(totalHashRate), "white", attrs=["bold"]))
    print(colored("Last 24H = ", "green", attrs=["bold"]) + colored(str(rawData["data"]["total_24h"]), "white", attrs=["bold"]))
    print(colored("---" * 30, "white"))
    print(colored("Per Day = ", "green", attrs=["bold"]) + colored(str(rewardRawData["per_day"]), "white", attrs=["bold"]))
    print(colored("Per Month = ", "green", attrs=["bold"]) + colored(str(rewardRawData["per_month"]), "white", attrs=["bold"]))
    print(colored("---" * 30, "white"))

def NextBar():
    total = (args.time * 550)
    try:
        bar = ProgressBar(total)
        for x in range(total):
            time.sleep(0.1)
            bar.iter()
    except:
        bar.stop()
    bar.wait()

if __name__ == '__main__':
    while(True):
        UpdateCheck()
        Banner()
        GetData()
        NextBar()