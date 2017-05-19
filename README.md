# StockTracker

This project uses a locally hosted MySQL database to monitor stock information and activity. The Python Yahoo Finance package (https://github.com/lukaszbanasiak/yahoo-finance) is used to get market price information for each stock symbol.

StockMonitor.pyw can be run as a background process to update price information every 5 minutes, when it is during trading hours and not a stock exchange holiday. All hours and holiday information are imported from the New York Stock Exchange website (https://www.nyse.com/markets/hours-calendars).

Stocks can be added, removed, or displayed from the database using the following command line arguments:

### --add (stock symbol)
Used to add a stock symbol to be tracked.

The command line example "python StockTracker.py --add GOOGL" would add Google's stock to be tracked.

### --remove (stock symbol) (optionally --allTables)
Used to remove a stock symbol that is already being tracked.

The command line example "python StockTracker.py --remove GOOGL" would remove Google's stock from only the stock database. This would not remove any stock activity or history data that had accumulated.

To remove stock information from all tables, simply add the "--allTables" argument.

For example, "python StockTracker.py --remove GOOGL --allTables" would remove all data from all tables where the stock symbol is GOOGL.

### --display
Used to display the stock symbols that are currently being tracked.

The command line example "python StockTracker.py --display" would print any symbols being tracked to the command line.

