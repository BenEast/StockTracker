from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
import sched, time

#-----------------------------------------------------------------------------------
# TODO:
# -FIX BUG IN STOCKBOT MONITOR
# -Update avgStockOpen and avgStockClose MySQL statements to change based on time.
# -Make use of stock_history based on stock_activity and stock
#-----------------------------------------------------------------------------------
# -REFACTOR EXISTING CODEBASE
#-----------------------------------------------------------------------------------
# -Update exception handling to create log files when necessary.
# -Allow adding/removing stocks from the DB without directly altering the DB.
# -Allow usage of custom DB/multiple DBs in main
#-----------------------------------------------------------------------------------

# Return true if it is currently trading hours, and false otherwise.
# Based off of my timezone (US Central).
# TODO: update to allow alternate timezones to compare currentTime
def isDuringTrading(currentTime):
    if (currentTime > '08:30:00' and currentTime < '15:00:00'):
        return True
    else:
        return False

# Activates sb.monitor every 10 minutes to update stock_history information with a new price.
def monitorStocks(sb: StockBot):
    sb.monitor()
    sb.updateAverages()

# Main body of the program.
def main():
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)
    trackerScheduler = sched.scheduler(time.time, time.sleep)

    # Runs as a background process until terminated.
    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        currentDay = datetime.today().weekday()
        
        # If it's not the weekend and during trading hours, monitor the stocks.
        #if (currentDay < 5) and (isDuringTrading(currentTime)):
        trackerScheduler.enter(5, 1, sb.run, ())
        trackerScheduler.run()

    sd.close()

if __name__ == "__main__" :
    main()
    