#!/usr/bin/python

import sys
from zipfile import ZipFile
import os.path
from os import path
import requests
from datetime import datetime, timedelta
from serverDataInterface import serverDataInterface
import json
from timeManager import ms2str
from timeManager import datetime2ms, ms2datetime

if not len(sys.argv) == 6:
    print('usage: python3 client.py <email> <the user is Covid positive (1 if true, 0 otherwise)> <history length> <path to timeline zip file> <server address>')
    exit()

email = str(sys.argv[1])
userIsPositive = bool(int(sys.argv[2]))
expDays = int(sys.argv[3])
filename = str(sys.argv[4])
serverName = str(sys.argv[5])
print()
print('Please, check the data:')
print()
print('email                      :',email)
print('the user is Covid positive :',str(userIsPositive))
print('history length             :',expDays,'days')
print('path to timeline zip file  :',filename)
print('server address             :',serverName)
print()
ret = input('Do you confirm? [enter \'yes\' to confirm]: ')
print()
if not ret == 'yes': exit()
logFile = open("log.txt","w")

di = serverDataInterface(serverName)

if path.exists('temp'):
    print('The folder \\temp already exists. Probably, it contains the data from the last timeline extracted.')
    print('If you want to use the new data in ' + filename + ', please delete the \\temp folder.')
    print()
    input('Press a key to continue.')
    print()
if path.exists('temp'):
    print()
    print('Using data in existing \\temp folder.')
    print()
else:
    #https://takeout.google.com/settings/takeout/custom/location_history
    #filename = '/Users/andrea/Downloads/takeout-20200328T141106Z-001.zip'
    print()
    print("Unzipping file ... ", filename)

    with ZipFile(filename, 'r') as zipObj:
       zipObj.extractall('temp')



expirationDays = timedelta(days=int(expDays))
today = datetime.today()
now = datetime.now()
userId = di.getUserIdOrCreateIt(email)
logFile.write('UserId : %d \r\n'% userId)

if userIsPositive:
    di.updateUserId(userId,datetime2ms(now))
    logFile.write('Update user as infected.\r\n')

logFile.write('Now : %s \r\n'% str(now))

# Get list of json file that we want to process, i.e., within 'expirationDays' days from today
fileList = list()
startDay = today-expirationDays
monthStr = {1:'JANUARY',2:'FEBRUARY',3:'MARCH',4:'APRIL',5:'MAY',6:'JUNE',
7:'JULY',8:'AUGUST',9:'SEPTEMBER',10:'OCTOBER',11:'NOVEMBER',12:'DECEMBER'}

currentYear = startDay.year
currentMonth = startDay.month
while currentYear<today.year or (currentYear==today.year and currentMonth<=today.month):
    fileName = 'temp/Takeout/Location History/Semantic Location History/'+str(currentYear)+'/'+str(currentYear)+'_'+monthStr[currentMonth]+'.json'
    if path.exists(fileName): fileList.append(fileName)
    if currentMonth <12:
        currentMonth = currentMonth+1
    else:
        currentMonth = 1
        currentYear = currentYear+1

visitsList = list()

for file in fileList:
    data = json.load(open(file))
    for tlObj in data['timelineObjects']:
        if 'placeVisit' in tlObj:
            startTimeMs = int(tlObj['placeVisit']['duration']['startTimestampMs'])
            ageVisit = now-datetime.fromtimestamp(startTimeMs/1000)
            if ageVisit<expirationDays:
                logFile.write('\r\n')
                logFile.write('placeId : %s \r\n'% str(tlObj['placeVisit']['location']['placeId']))
                logFile.write('name : %s \r\n'% str(tlObj['placeVisit']['location']['name']))
                logFile.write('address : \r\n %s \r\n'% str(tlObj['placeVisit']['location']['address']))
                logFile.write('startTime : %s \r\n'% ms2str(startTimeMs))
                logFile.write('endTimestamp :  %s \r\n'% ms2str(int(tlObj['placeVisit']['duration']['endTimestampMs'])))

                visitsList.append({
                'userId':userId,
                'placeId':tlObj['placeVisit']['location']['placeId'],
                'name':tlObj['placeVisit']['location']['name'],
                'address':tlObj['placeVisit']['location']['address'],
                'startTime':tlObj['placeVisit']['duration']['startTimestampMs'],
                'stopTime':tlObj['placeVisit']['duration']['endTimestampMs']
                })

if len(visitsList)>0: di.addActivities(visitsList)
print()
print('Number of location added:',len(visitsList))
logFile.write('\r\n Number of location added: %d' % len(visitsList))
print()
if userIsPositive:
    print('Thanks for contribuiting!')
else:
    activitiesList = di.getInfectedVisitsOfUserShort(userId)
    if len(activitiesList)>0:
        locationFile = open("log_contact_times.txt","w")
        for i in range(len(activitiesList)):
            locationFile.write('\r\n ## %d\r\n'%i)
            locationFile.write('Name: %s\r\n'% activitiesList[i]['name'])
            locationFile.write('Address: \r\n%s\r\n'% activitiesList[i]['address'])
            locationFile.write('TimeStart: %s\r\n'% activitiesList[i]['vInfectedstartTime'])
            locationFile.write('TimeStop: %s\r\n'% activitiesList[i]['vInfectedstopTime'])

    print()
    logFile.write('\r\n Number of times this timeline crossed the timeline of a positive user: %d' % len(activitiesList))
    print('Number of times this timeline crossed the timeline of a positive user:',len(activitiesList))
    if len(activitiesList)>0:
        print('Check the file \\contact_times.txt from more details about the crossing locations.')
    print()
