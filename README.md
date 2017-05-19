# StockTracker

This project uses a locally hosted MySQL database to monitor stock information and activity. The Python Yahoo Finance package (https://github.com/lukaszbanasiak/yahoo-finance) is used to get market price information for each stock symbol.

StockMonitor.pyw can be run as a background process to update price information every 5 minutes, when it is during trading hours and not a stock exchange holiday. All hours and holiday information are imported from the New York Stock Exchange website (https://www.nyse.com/markets/hours-calendars).

The Rainmeter folder contains a custom skin to display the stock symbols being tracked, along with their most recent price. This information is stored in two .txt files, which are updated each time the program adds new entries to the StockBot database. There is also a corresponding `StockMonitor_1.0.0.rmskin` file, which allows for quick installation of the rainmeter skin. This skin is based on the "illustro" rainmeter theme, which comes with the program upon installation.

Stocks can be added, removed, or displayed from the database using the following command line arguments:

### --add (stock symbol)
Used to add a stock symbol to be tracked.

The command line example `python StockTracker.py --add GOOGL` would add Google's stock to be tracked.

The command "--add" can be optionally replaced with "-a" with the same effect, as in `python StockTracker.py -a GOOGL`.

### --remove (stock symbol) (optionally --allTables)
Used to remove a stock symbol that is already being tracked.

The command line example `python StockTracker.py --remove GOOGL` would remove Google's stock from only the stock database. This would not remove any stock activity or history data that had accumulated.

To remove stock information from all tables, simply add the `--allTables` argument.

For example, `python StockTracker.py --remove GOOGL --allTables` would remove all data from all tables where the stock symbol is GOOGL.

The command "--remove" can be optionally replaced with "-r" with the same effect, as in `python StockTracker.py -r GOOGL` or `python StockTracker.py -r GOOGL --allTables`.

### --display
Used to display the stock symbols that are currently being tracked.

The command line example `python StockTracker.py --display` would print any symbols being tracked to the command line.

The command "--display" can be optionally replaced with "-d" with the same effect, as in `python StockTracker.py -d`.
