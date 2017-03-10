from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from sched import scheduler
from pytz import timezone
import time, os, sys 
import logging, gc

#-----------------------------------------------------------------------------------
# TODO:
# -Implement holiday tracking for StockMonitor
# -Documentation, reordering, renaming, refactoring
# -Create UI for data display
#-----------------------------------------------------------------------------------

# Return true if it's after trading hours for the NYSE.
def isAfterTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > "16:00:00"):
        return True
    else:
        return False

# Return true if it is currently trading hours, and false otherwise.
def isDuringTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > "09:20:00" and currentTime < "15:50:00"):
        return True
    else:
        return False

# Sets up a log directory and a log file if they do not exist.
def initializeLogDirectory() -> None:
    logsPath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/logs/"
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)
        
    # create a log file if necessary
    logFilePath = (logsPath + "stockTracker-" + 
        str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]) + ".log")
        
    try:
        file = open(logFilePath, "r")
    except IOError:
        file = open(logFilePath, "w")
    file.close()
        
    return logFilePath
        
# Main body of the program.
def main():
    gc.enable()
    logPath = initializeLogDirectory()
    logging.basicConfig(filename = logPath, level = logging.DEBUG, 
                        format="%(levelname)s::%(asctime)s: %(message)s")
    sd = StockDB("ben", "pass", "127.0.0.1", "stockbot")
    sb = StockBot(sd)
    
    dayHistoryUpdated = False
    trackerScheduler = scheduler(time.time, time.sleep)
    est_tz = timezone("US/Eastern")
    
    # Runs as a background process until terminated.
    while(True):
        gc.collect() # Force garbage collection
        currentTime = datetime.now(est_tz).strftime("%Y-%m-%d %H:%M:%S")[11:]
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
    