from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
import sched, time

# Return true if it is currently trading hours, and false otherwise.
# Based off of my timezone (US Central).
# TODO: update to allow alternate timezones to compare currentTime
def isDuringTrading(currentTime):
    if (currentTime > '08:30:00' and currentTime < '03:00:00'):
        return True
    else:
        return False

# Activates sb.monitor every 5 minutes to update stock_history information with a new price.
def monitorStocks(sb: StockBot, monitorScheduler: sched.scheduler):
    monitorScheduler.enter(300, 1, sb.monitor, ())
    monitorScheduler.run()

# Main body of the program.
def main():
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)
    monitorScheduler = sched.scheduler(time.time, time.sleep)

    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        if isDuringTrading(currentTime):
            monitorStocks(sb, monitorScheduler)

    sd.close()

if __name__ == "__main__" :
    main()
    