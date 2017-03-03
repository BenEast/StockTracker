from StockDB import StockDB
from StockBot import StockBot
import sched, time
from datetime import datetime


def isDuringTrading(currentTime):
    if (currentTime > '08:30:00' and currentTime < '03:00:00'):
        return True
    else:
        return False
    
def monitorStocks(sb: StockBot):
    monitorScheduler = sched.scheduler(time.time, time.sleep)
    monitorScheduler.enter(300, 1, sb.monitor, ())
    monitorScheduler.run()

def main():
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)

    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        if isDuringTrading(currentTime):
            monitorStocks(sb)

if __name__ == "__main__" :
    main()
    