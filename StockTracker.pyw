from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from sched import scheduler
import time

#-----------------------------------------------------------------------------------
# TODO:
# -Update exception handling to create log files when necessary.
# -Update to run every x minutes starting at time x
# -Allow isDuringTrading/isAfterTrading to check based on the user's timezone.
# -Refactor more (and more and more)
# -Allow adding/removing stocks from the DB without directly altering the DB.
# -Allow usage of custom DB/multiple DBs in main
# -Create UI for data display?
#-----------------------------------------------------------------------------------

# Return true if it's after trading hours for the NYSE.
# Based off of my timezone (US Central).
def isAfterTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > '15:00:00'):
        return True
    else:
        return False

# Return true if it is currently trading hours, and false otherwise.
# Based off of my timezone (US Central).
def isDuringTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > '08:30:00' and currentTime < '15:00:00'):
        return True
    else:
        return False

# Main body of the program.
def main():
    dayHistoryUpdated = False
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)
    trackerScheduler = scheduler(time.time, time.sleep)

    # Runs as a background process until terminated.
    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        currentDay = datetime.today().weekday()
        
        # If it's not the weekend and during trading hours, monitor the stocks.
        if (currentDay < 5) and (isDuringTrading(currentTime)):
            dayHistoryUpdated = False
            trackerScheduler.enter(600, 1, sb.run, ())
            trackerScheduler.run()
            
        # Update stock_history table at the end of trading for the day.
        elif (currentDay < 5) and isAfterTrading(currentTime) and not dayHistoryUpdated:
            sb.postStockHistory()
            dayHistoryUpdated = True

    sd.close()

if __name__ == "__main__" :
    main()
    