import csv
import os
from datetime import datetime
from src.Entities import *
from concurrent.futures import ProcessPoolExecutor as PoolExecutor

directory_name = "..\\data\\"
directory = os.path.join(directory_name)
def Parse():
    list=[]
    for root, dirs, files in os.walk(directory):
        with PoolExecutor(max_workers=4) as executor:
            for fileIndex, fund in enumerate(executor.map(ParseInternal, files)):
                list.append(fund)
                pass

    return list

def ParseInternal(file):
    month = 0
    if file.endswith(".csv"):
        with open(directory_name + file, 'r') as csvfile:
            streamReader = csv.reader(csvfile, delimiter=' ')
            data = []
            for stream in streamReader:
                data.append(stream)
            calendarData = []
            metaData = []
            indexDataStart = 0
            for index in range(0, len(data)):
                if data[index][0] == 'Program':
                    indexDataStart = index
                    break
                calendarData.append(data[index])
            for index in range(indexDataStart, len(data)):
                metaData.append(data[index])
            fund = HedgeFund(csvfile.name)
            fund.Statistics = []
            stat = Statistics()
            monthPerform = MonthPerform()
            for index, row in enumerate(calendarData):
                if index != 0:
                    for j, word in enumerate(row):
                        if isFloat(word):
                            date = TryParse('01/01/' + word)
                            if date is not None:
                                month = 1
                                stat = Statistics()
                                monthPerform = MonthPerform()
                                monthPerform.Month = month
                                monthPerform.Year = date.year
                                stat.Year = date.year
                                continue
                            elif month <= 12:
                                monthPerform.Perfomance = float(word)
                                monthPerform.Year = stat.Year
                                monthPerform.Month = month
                                stat.MonthPerform.append(monthPerform)
                                monthPerform = MonthPerform()
                                month += 1
                            else:
                                if month == 13:
                                    month += 1
                                    stat.Ytd = word
                                elif month == 14:
                                    stat.Dd = word
                                    if stat.Year != 2021:
                                        fund.Statistics.append(stat)
            for row in metaData:
                for j, word in enumerate(row):
                    if word == 'Minimum':
                        fund.MinInvest = int(row[j + 3].rstrip('k')) * 1000
                    elif word == 'Sharpe':
                        fund.SharpeRatioData = float(row[j + 2])
            csvfile.close()
    return fund

def isFloat(n):
    try:
       float(n)
       return True
    except ValueError:
       return False

def TryParse(n):
    date = None
    try:
       date=datetime.strptime(n, "%d/%m/%Y")
       return date
    except ValueError:
       return date