from StockDB import StockDB
from StockBot import StockBot
from datetime import datetime
from sched import scheduler
from pytz import timezone
from lxml import html
import requests
import time, os, sys 
import logging, gc

#-----------------------------------------------------------------------------------
# TODO:
# -Update holiday tracking to make note of early closes (handle * cases instead of removing them)
# -Create UI for data display
#-----------------------------------------------------------------------------------

_holidayList = []   # Global to store NYSE holidays, so we only import once.

# Removes any empty list [] from a list of lists
def _curateList(l: list) -> list:
    out = []
    for x in l:
        if not x == []:
            out.append(x)

    return out

# Converts a list of holiday data imported from the NYSE website into YYYY
def _holidaysToDates(dateList: list, year: str) -> list:
    months = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", 
                  "June": "06", "July": "07", "August": "08", "September": "09", 
                  "October": "10", "November": "11", "December": "12"}
    holidates = [] #lol "holidates"; master class pun
    
    for holiday in dateList:
        if len(holiday) == 1:
            date = [x.strip(',*') for x in holiday[0].split(" ")]
            dayNum = date[2]
            if len(dayNum) == 1:
                dayNum = "0" + dayNum
            holidates.append(year + "-" + months.get(date[1]) + "-" + dayNum)
            
        elif len(holiday) == 2:
            obDate = [x.strip(',*()') for x in holiday[1].split(" ")]
            dayNum = obDate[3]
            if len(dayNum) == 1:
                dayNum = "0" + dayNum
            holidates.append(year + "-" + months.get(obDate[2]) + "-" + dayNum)
            
    return holidates

# Converts a list of holidays into a dictionary grouped by year.
# Assuming 3 years at a time, based on current NYSE holiday posting.
def _makeYearDict(years: list, dateList: list) -> list:
    l1, l2, l3 = [], [], []
    for x in dateList:
        i = dateList.index(x)
        if i % 3 == 0:
            l1.append(x)
        elif i % 3 == 1:
            l2.append(x)
        elif i % 3 == 2:
            l3.append(x)

    yearDict = {years[0][0]: l1, years[1][0]: l2, years[2][0]: l3}
    return yearDict

# Generates a file of the holidays listed on the NYSE website.
def generateHolidayFile(filepath: str) -> None:
    page = requests.get("https://www.nyse.com/markets/hours-calendars")
    tree = html.fromstring(page.content)

    years = []
    for x in range(7, 10):
        pathStr = '//td[@data-reactid="' + str(x) + '"]/text()'
        years.append(tree.xpath(pathStr))
    
    holidayData = []
    for x in range(13, 56):
        pathStr = '//td[@data-reactid="' + str(x) + '"]/text()'
        holidayData.append(tree.xpath(pathStr))

    yearDict = _makeYearDict(_curateList(years), _curateList(holidayData))
      
    holidayFile = open(filepath, "ab")
    for key in yearDict.keys():
        hol = _holidaysToDates(yearDict.get(key), key)
        print(hol)
        for date in hol:
            holidayFile.write(bytes(date + ",", "UTF-8"))

    holidayFile.close()
    logging.info("Generated /resources/holidays.bin")
    
# Imports NYSE holidays to this StockMonitor instance. May create /resources/holidays.bin
def importHolidays():
    resourcePath = os.path.dirname(os.path.abspath(sys.argv[0])) + "/resources/"
    if not os.path.exists(resourcePath):
        os.makedirs(resourcePath)
        
    holidayFilePath = (resourcePath + "holidays.bin")
    try:
        file = open(holidayFilePath, "rb")
    except IOError:
        generateHolidayFile(holidayFilePath)
        file = open(holidayFilePath, "rb")  
        
    fileContent = file.read().decode("UTF-8")
    file.close()
    
    return fileContent.split(",")
    
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
    
# Return true if it's a NYSE holiday, and false otherwise.
def isHoliday(currentDate: str) -> bool:
    if currentDate in _holidayList:
        return True
    else:
        return False
        
# Main body of the program.
def main():
    gc.enable()
    logPath = initializeLogDirectory()
    logging.basicConfig(filename = logPath, level = logging.DEBUG, 
                        format="%(levelname)s::%(asctime)s: %(message)s")
    _holidayList = importHolidays()
    sd = StockDB("ben", "pass", "127.0.0.1", "stockbot")
    sb = StockBot(sd)
    
    dayHistoryUpdated = False
    trackerScheduler = scheduler(time.time, time.sleep)
    est_tz = timezone("US/Eastern")
    
    # Runs as a background process until terminated.
    while(True):
        gc.collect() # Force garbage collection
        timestamp = datetime.now(est_tz).strftime("%Y-%m-%d %H:%M:%S")
        currentDate = timestamp[:10]
        currentTime = timestamp[11:]
        currentDay = datetime.today().weekday()

        # If it's not the weekend and during trading hours, monitor the stocks.
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
