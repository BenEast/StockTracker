from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
import time, sched

#-----------------------------------------------------------------------------------
# TODO:
# -Refactor more (type restraints; naming; method ordering;
# -Update exception handling to create log files when necessary.
# -Allow isDuringTrading/isAfterTrading to check based on the user's timezone.
# -Allow adding/removing stocks from the DB without directly altering the DB.
# -Refactor more (and more and more)
# -Allow usage of custom DB/multiple DBs in main
#-----------------------------------------------------------------------------------

# Return true if it is currently trading hours, and false otherwise.
# Based off of my timezone (US Central).
def isDuringTrading(currentTime):
    if (currentTime > '08:30:00' and currentTime < '15:00:00'):
        return True
    else:
        return False

# Return true if it's after trading hours for the NYSE.
# Based off of my timezone (US Central).
def isAfterTrading(currentTime):
    if (currentTime > '15:00:00'):
        return True
    else:
        return False

# Main body of the program.
def main():
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)
    trackerScheduler = sched.scheduler(time.time, time.sleep)

    dayHistoryUpdated = False
    # Runs as a background process until terminated.
    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        currentDay = datetime.today().weekday()
        
        # If it's not the weekend and during trading hours, monitor the stocks.
        if (currentDay < 5) and (isDuringTrading(currentTime)):
            trackerScheduler.enter(5, 1, sb.run, ())
            trackerScheduler.run()
            
        # Update stock_history table at the end of trading for the day.
        elif (currentDay < 5) and isAfterTrading(currentTime) and not dayHistoryUpdated:
            sb.updateStockHistory()
            dayHistoryUpdated = True

    sd.close()

if __name__ == "__main__" :
    main()
    