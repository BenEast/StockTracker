from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from sched import scheduler
from pytz import timezone
from lxml import html
import requests
import time, os, sys 
import logging, gc

_holidayList = []   # Global to store NYSE holidays, so we only import once.

# Removes any empty lists [] from a list of lists
# PARAMETERS: lists: a list of lists;
# RETURNS: Returns a list of lists without any empty lists.
def _removeEmptyLists(lists: list) -> list:
    return [lst for lst in lists if not lst == []]

# Converts a list of holiday data imported from the NYSE website into YYYY-MM-DD
# PARAMETERS: dateList: a list of dates not in MySQL date format.
#             year: the year of the dates.
# RETURNS: Returns a list of holiday dates in the MySQL date format.
def _holidaysToDates(dateList: list, year: str) -> list:
    months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", 
                  "June": "06", "July": "07", "August": "08", "September": "09", 
                  "October": "10", "November": "11", "December": "12"}
    holidayDates = []
    
    # Format the date information pulled from the NYSE website into MySQL date format.
    for holiday in dateList:
        if len(holiday) == 1:
            date = [x.strip(',*') for x in holiday[0].split(" ")]
            dayNum = date[2] # the day is always at index 2 due to the layout of the website.
            if len(dayNum) == 1:
                dayNum = "0" + dayNum # add leading 0 if the date is a single character
            holidayDates.append(year + "-" + months.get(date[1]) + "-" + dayNum)
            
        elif len(holiday) == 2:
            obDate = [x.strip(',*()') for x in holiday[1].split(" ")]
            dayNum = obDate[3] # the day is always at index 3 due to the layout of the website.
            if len(dayNum) == 1:
                dayNum = "0" + dayNum # add leading 0 if the date is a single character
            holidayDates.append(year + "-" + months.get(obDate[2]) + "-" + dayNum)
            
    return holidayDates

# Converts a list of holidays into a dictionary grouped by year.
# Assuming 3 years at a time, based on current NYSE holiday posting.
# PARAMETERS: years: the years to create a dictionary for
#             dateList: a list of dates
# RETURNS: Returns
def _makeYearDict(years: list, dateList: list) -> list:
    # need 3 lists due to the formatting of the NYSE website after html parsing
    l1, l2, l3 = [], [], []
    for date in dateList:
        index = dateList.index(date)
        
        # Assign date to a list based on it's index
        if index % 3 == 0:
            l1.append(date)
        elif index % 3 == 1:
            l2.append(date)
        elif index % 3 == 2:
            l3.append(date)

    yearDict = {years[0][0]: l1, years[1][0]: l2, years[2][0]: l3}
    return yearDict

# Generates a file of the holidays listed on the NYSE website.
# PARAMETERS: filepath: The filepath to open/create.
# RETURNS: None
def generateHolidayFile(filepath: str) -> None:
    page = requests.get("https://www.nyse.com/markets/hours-calendars")
    tree = html.fromstring(page.content)

    # Get the years posted from the NYSE holiday page
    years = []
    for htmlReactIdValue in range(7, 10): # nums 7-10 are the HTML ReactID tags that contain holiday info
        pathStr = '//td[@data-reactid="' + str(htmlReactIdValue) + '"]/text()'
        years.append(tree.xpath(pathStr))
    
    # Import all holiday data correspoding with those years
    holidayData = []
    for x in range(13, 56):
        pathStr = '//td[@data-reactid="' + str(x) + '"]/text()'
        holidayData.append(tree.xpath(pathStr))

    # Join the  years and holiday data into a dictionary
    yearDict = _makeYearDict(_removeEmptyLists(years), _removeEmptyLists(holidayData))
      
    # Create a holiday dictionary from the year dictionary
    for key in yearDict.keys():
        holidaysDict = _holidaysToDates(yearDict.get(key), key)
        
        holidayFile = open(filepath, "ab")
        for date in holidaysDict:
            holidayFile.write(bytes(date + ",", "UTF-8"))

    holidayFile.close()
    logging.info("Generated /resources/holidays.bin")
    
# Imports NYSE holidays to this StockMonitor instance. May create /resources/holidays.bin.
# PARAMETERS: None
# RETURNS: Returns a list of holidays for the NYSE.
def importHolidays() -> list:
    # create the resources directory if it doesn't exist
    resourcePath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/resources/"
    if not os.path.exists(resourcePath):
        os.makedirs(resourcePath)
        
    holidayFilePath = (resourcePath + "holidays.bin")
    
    # Open the holiday file, or create it if it doesn't exist
    try:
        file = open(holidayFilePath, "rb")
    except IOError:
        generateHolidayFile(holidayFilePath)
        file = open(holidayFilePath, "rb")  
        
    fileContent = file.read().decode("UTF-8")
    file.close()
    
    return fileContent.split(",")
    
# Sets up a log directory and a log file if they do not exist.
# PARAMETERS: None
# RETURNS: Returns a string of the path to the log file.
def initializeLogDirectory() -> str:
    # create the logs directory if it doesn't exist
    logsPath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/logs/"
    if not os.path.exists(logsPath):
        os.makedirs(logsPath)
        
    # create a log file if one doesn't exist for this date
    logFilePath = (logsPath + "stockTracker-" + 
        str(datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:10]) + ".log")
        
    try:
        file = open(logFilePath, "r")
    except IOError:
        file = open(logFilePath, "w")
    file.close()
        
    return logFilePath
    
# Return true if it's after trading hours for the NYSE.
# PARAMETERS: currentTime: the time to check.
# RETURNS: Returns True if it is after NYSE trading hours and False otherwise.
def isAfterTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > "16:00:00"):
        return True
    else:
        return False

# Return true if it is currently trading hours, and false otherwise.
# PARAMETERS: currentTime: the time to check.
# RETURNS: Returns True if it is during trading hours and False otherwise.
def isDuringTrading(currentTime: str) -> bool:
    currentTime = str(currentTime)
    if (currentTime > "09:20:00" and currentTime < "15:50:00"):
        return True
    else:
        return False
    
# Return true if it's a NYSE holiday, and false otherwise.
# PARAMETERS: currentDate: the date to check.
# RETURNS: Returns True if the date is an NYSE holiday and False otherwise.
def isHoliday(currentDate: str) -> bool:
    if currentDate in _holidayList:
        return True
    else:
        return False
        
# Main body of the program.
def main():
    gc.enable()
    
    # initialize logging for the program
    logPath = initializeLogDirectory()
    logging.basicConfig(filename = logPath, level = logging.DEBUG, 
                        format="%(levelname)s::%(asctime)s: %(message)s")
    
    # Get holiday information for the NYSE
    _holidayList = importHolidays()
    
    sd = StockDB("ben", "pass", "127.0.0.1", "stockbot")
    sb = StockBot(sd)
    
    dayHistoryUpdated = False
    trackerScheduler = scheduler(time.time, time.sleep)
    est_tz = timezone("US/Eastern")
    
    # Runs as a background process until terminated.
    while(True):
        gc.collect() # Force garbage collection
        
        # Get date/time information
        timestamp = datetime.now(est_tz).strftime("%Y-%m-%d %H:%M:%S")
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        currentDay = datetime.today().weekday()

        # If it's not the weekend AND during trading hours: monitor the stocks.
        if currentDay < 5 and isDuringTrading(currentTime) and not isHoliday(currentDate):
            dayHistoryUpdated = False
            trackerScheduler.enter(600, 1, sb.run, ())
            trackerScheduler.run()

        # Update stock_history table at the end of trading for the day.
        elif (currentDay < 5 and isAfterTrading(currentTime) 
                and not isHoliday(currentDate) and not dayHistoryUpdated):
            sb.postStockHistory()
            dayHistoryUpdated = True

    sd.close()

if __name__ == "__main__" :
    main()
