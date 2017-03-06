from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from yahoo_finance import Share
import os, sys, logging, argparse, gc

#-----------------------------------------------------------------------------------
# TODO:
# -Allow usage of custom DB/multiple DBs in main
# -Refactor (a lot)
# -Create UI for data display
#-----------------------------------------------------------------------------------

# Sets up a log directory and a log file if they do not exist.
def initializeLogDirectory():
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
    
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--add", type = str, help = "Add a stock to the database.")
    parser.add_argument("-r", "--remove", type = str, help = "Remove a stock from the database.")
    parser.add_argument("--allTables", action="store_true")
    parser.add_argument("-d", "--display", action="store_true", help = "Display the stocks in the database.")
    args = parser.parse_args()
    
    # Display all stocks
    if args.display:
        for stock in sd.getKeyValues('stock'):
            print(stock)
    # Handle /add command
    elif not args.add == None:
        stock = args.add.upper()
        yahoo = Share(stock)
        if not yahoo.get_price() == None:
            sb.postStock(stock)
            logging.info("Stock '{}' posted to database.".format(stock))
        else:
            print("Invalid stock argument passed with --add.")
            logging.warning("Invalid stock argument passed with --add.")
    # Handle /remove command                
    elif not args.remove == None:
        stock = args.remove.upper()
        if stock in sb.stocksToMonitor:
            sb.removeStock(stock, args.allTables)
            logging.info("Stock '{}' removed from database. allTables = {}".format(stock, args.allTables))
        else:
            print("Invalid stock argument passed with --remove.")
            logging.warning("Invalid stock argument passed with --remove.")      

    sd.close()

if __name__ == "__main__" :
    main()
    