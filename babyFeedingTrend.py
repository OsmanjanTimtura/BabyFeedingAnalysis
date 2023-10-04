import pandas as pd
from datetime import datetime, time
import numpy as np
import matplotlib.pyplot as plt

#reading data of baby drinking expressed milk
#
yalkunData = pd.read_csv("C:/Users/osmanjan/Downloads/csv/Yalkun_expressed.csv")
#assigning some global variables used in the program
fedTime = ""
morningOrAfternoon = ""
fedMonth = ""
fedAmount = 0.0
feedInfoList = list()
dayRange = 0
averageByMonthByRange = list()
monthlyData = list()


#This function takes date information and returns the month value.
def monthRange(myDate):
    try:
        if myDate[0] == "1":
            if myDate[0:2] == "10":
                return "October"
            elif myDate[0:2] == "11":
                return "November"
            elif myDate[0:2] == "12":
                return "December"
            else:
                return "January"
        elif myDate[0] == "2":
            return "February"
        elif myDate[0] == "3":
            return "March"
        elif myDate[0] == "4":
            return "April"
        elif myDate[0] == "5":
            return "May"
        elif myDate[0] == "6":
            return "June"
        elif myDate[0] == "7":
            return "July"
        elif myDate[0] == "8":
            return "August"
        elif myDate[0] == "9":
            return "September"
    except:
        print("Something went wrong while determining which month current data belongs to.")
    

#This function takes time data as string, converts it to time data, determines what range it belongs to 0-12. It can be either AM or PM.
def timeRange(myTime):
    try:
        # converts time data from string to time.
        myActualTime = datetime.strptime(myTime, "%H:%M").time()
        #Assigned 0 as default range value.
        myRange = 0
        #actual time range is assigned depending the actual time range of 1-12.
        for i in range (1, 12):
            if time(i, 0) <= myActualTime <= time(i, 59):
                myRange = i
    except:
        print("Something went wrong while finding out the time range of the time.")
    return myRange


#Afternoon ranges are separated from morning ranges. 
def timeRanges(my_MorningOrAfternoon, feedingTime):
    myRange = 0
    try:
        if my_MorningOrAfternoon == "AM":
            myRange = timeRange(feedingTime)
        else:
            myRange = timeRange(feedingTime) + 12
    except:
        print("Something is not right while separating morning ranges from afternoon ranges.")
    return myRange
           

#This function takes time data, splits it into date, time of the day, and AM/PM data. Stores these values in a list, and returns the list containing 3 values. 
def splitDateTime(myDateTime):
    try:                    #Time of a day           AM or PM                     date
        splitDateTimeInfo = [myDateTime.split()[1], myDateTime.split()[2], myDateTime.split()[0][:-1]]
    except:
        print("Something went wrong while splitting time/time info!")
    return splitDateTimeInfo


#This function takes monthly data, calculates the average by range of a day, returns the monthly average by range of a day. 
def monthlyAverageByRange(myMonthlyData):
    count_range = list()
    sum_range = list()
    range_average = list()
    monthlyAverageByRange = list()
    try:
        #This loop assigns 0 as initial value for count and sum of each range.
        for i in range(24):
            count_range.append(0)
            sum_range.append(0)
            range_average.append(0)
        #This loop loops through monthly data which includes range info of the data, and actual value. 
        #sums up values belong to each range, and counts the appearance of each range. 
        for data in myMonthlyData:
            for i in range(24):
                if data[0] == i:
                    sum_range[i] = sum_range[i] + data[1]
                    count_range[i] = count_range[i] + 1
        #This loop calculates the average of feedings at each time range and put the results in a list. 
        for i in range(24):
            if count_range[i] != 0:
                range_average[i] = sum_range[i] / count_range[i]
                monthlyAverageByRange.append([i, range_average[i]])
    except:
        print("Something went wrong while calculating the averages!")
    return monthlyAverageByRange


#This function isolates data of a given month from the list of data that includes month info, time info and amount info.
def monthlyData(month, feedingInfoList):
    myMonthlyData = list()
    try:
        for feedInfo in feedingInfoList:
            if feedInfo[0] == month:
                myMonthlyData.append([feedInfo[1], feedInfo[2]])
    except:
        print("There's something wrong splitting the monthly data.")
    return myMonthlyData


#This function takes monthly data, uses range as x axis, average value as y axis, puts them in an numpy array and returns the array. 
def showMonthlyGraph(thisMonthlyData):
    xList = list()
    yList = list()
    arrayXY = list()
    try:
        for average in thisMonthlyData:
            xList.append(average[0])
            yList.append(average[1])
        x = np.array(xList)
        y = np.array(yList)
        arrayXY.append(x)
        arrayXY.append(y)
    except:
        print("An error occured while converting the list to an numpy array!")
    return arrayXY


#This function extracts range average data by a given month.
def thisMonthData(month, babyFeedingList):
    try:
        thisMonthData = monthlyData(month, babyFeedingList)
        thisMonthAverageByRange = monthlyAverageByRange(thisMonthData)
    except:
        print("Something wrong occured while extracting range average data for {} month.".format(month))
    return thisMonthAverageByRange


#This function draws the plot for the given month taking the baby feeding data.
def plotThisMonth(babyFeedingInfoList, thisMonth, linestyle, linecolor):
    #x axis is time range.
    x = showMonthlyGraph(thisMonthData(thisMonth, babyFeedingInfoList))[0]
    #y axis is baby feeding info at that range
    y = showMonthlyGraph(thisMonthData(thisMonth, babyFeedingInfoList))[1]
    #makes the plot, linestyle and line color needs to be selected separately for each month.
    plt.plot(x, y, linestyle=linestyle, color=linecolor)
    #plot title, font size is 16.
    plt.title("Baby Feeding Trend", fontsize=16)
    #Label of x axis.
    plt.xlabel("Time Of Day")
    #Label of x axis, only shown 1-23, with 2 interval on the x axis.
    plt.xticks([1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23])
    #y axis is in range of 0-5.
    plt.ylim(0, 5)
    #Label of y axis.
    plt.ylabel("Amount (oz)")


#Actual non-functional code starts here.

#How many data entries there?
totalDataEntry = len(yalkunData)
#each data entry is analyzed.
for dataEntry in range(totalDataEntry):
    #This is feeding time of this entry.
    fedTime = splitDateTime(yalkunData["Time"].loc[dataEntry])[0]
    #This is in AM or PM?
    morningOrAfternoon = splitDateTime(yalkunData["Time"].loc[dataEntry])[1]
    #Which month is this entry belong to?
    fedMonth = monthRange(splitDateTime(yalkunData["Time"].loc[dataEntry])[2])
    #Amount of breast milk babe ate at this time.
    fedAmount = yalkunData["Amount (oz.)"].loc[dataEntry]
    #The time range of this data entry.
    dayRange = timeRanges(morningOrAfternoon, fedTime)
    #Storing a list of month, range, and amount into feed info list. 
    feedInfoList.append([fedMonth, dayRange, fedAmount])
#Plotting 3 selected months, July, August, September. With each one of the has different line features.
plotThisMonth(feedInfoList, "July", "dotted", "black")
plotThisMonth(feedInfoList, "August", "dashed", "black")
plotThisMonth(feedInfoList, "September", "solid", "black")
#Puts the figure legend at the top right.
plt.legend(loc="upper right", labels=["July", "August", "September"])
#Shows the plot. 
plt.show()