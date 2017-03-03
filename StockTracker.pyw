from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
import sched, time

# TODO:
# -Update exception handling to create log files if necessary.
# -Allow adding/removing stocks from the DB without directly altering the DB.
# -Update table schema in stock and stock_history, perhaps create another?
# -Add attributes to table schema to track more data

# Return true if it is currently trading hours, and false otherwise.
# Based off of my timezone (US Central).
# TODO: update to allow alternate timezones to compare currentTime
def isDuringTrading(currentTime):
    if (currentTime > '08:30:00' and currentTime < '15:00:00'):
        return True
    else:
        return False

# Activates sb.monitor every 10 minutes to update stock_history information with a new price.
def monitorStocks(sb: StockBot, monitorScheduler: sched.scheduler):
    monitorScheduler.enter(600, 1, sb.monitor, ())
    monitorScheduler.run()
    updateStocks(sb)

# Update the stocks in the database with the new information.
def updateStocks(sb: StockBot):
    sb.updateAverages()
    
# Main body of the program.
def main():
    sd = StockDB('ben', 'pass', '127.0.0.1', 'stockbot')
    sb = StockBot(sd)
    monitorScheduler = sched.scheduler(time.time, time.sleep)

    # Runs as a background process until terminated.
    while(True):
        currentTime = datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')[11:]
        currentDay = datetime.today().weekday()
        
        # If it's not the weekend and during trading hours, monitor the stocks.
        if (currentDay < 5) and (isDuringTrading(currentTime)):
            monitorStocks(sb, monitorScheduler)

    sd.close()

if __name__ == "__main__" :
    main()
    