from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from yahoo_finance import Share
import os, sys, logging, argparse, gc

# Sets up a log directory and a log file if they do not exist.
# PARAMETERS: None
# RETURNS: Returns the file path for the log file
def initializeLogDirectory() -> str:
    # create the logs directory if it doesn't exist
    logsPath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/logs/"
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)
        
    # create a log file if it doesn't exist for this date
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
    parser.add_argument("--allTables", action = "store_true") #goes with remove
    parser.add_argument("-d", "--display", action = "store_true", 
                        help = "Display the stocks in the database.")
    #parser.add_argument("--run", action = "store_true", 
    #                   help = "Run the stock tracker as a background process.")
    #parser.add_argument("--stop", action = "store_true", 
    #                   help = "Stop the stock tracker background process if it is running.")
    
    args = parser.parse_args()

    # Handle --display command
    if args.display: # Will be updated to show a GUI instead of printing stock signs
        for stock in sd.getKeyValues('stock'):
            print(stock)
    # Handle --add command
    elif not args.add == None:
        stock = args.add.upper()
        yahoo = Share(stock)
        if not yahoo.get_price() == None:
            sb.postStock(stock)
            print("Stock '{}' posted to database.".format(stock))
            logging.info("Stock '{}' posted to database.".format(stock))
        else:
            print("Invalid stock argument passed with --add.")
            logging.warning("Invalid stock argument passed with --add.")
    # Handle --remove command                
    elif not args.remove == None:
        stock = args.remove.upper()
        if stock in sb.stocksToMonitor:
            sb.removeStock(stock, args.allTables)
            print("Stock '{}' removed from database. allTables = {}".format(stock, args.allTables))
            logging.info("Stock '{}' removed from database. allTables = {}".format(stock, args.allTables))
        else:
            print("Invalid stock argument passed with --remove.")
            logging.warning("Invalid stock argument passed with --remove.")      
    #elif args.run:
    #   StockMonitor.main() # hopefully runs the process
    #elif args.stop:
    #   x = 0 # kill the stock monitor process
        
    sd.close()

if __name__ == "__main__" :
    main()
    