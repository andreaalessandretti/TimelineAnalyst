
from timeManager import datetime2ms, ms2datetime
from datetime import datetime
from plotUtils import plotActivitiesList, plotInfectedActivitiesList, plotInfectedUserVisitList
import sqlite3
from dbDataInterface import dbDataInterface
from serverDataInterface import serverDataInterface

from dbDataInterface import dbDataInterface

#di = dbDataInterface('codevscovid.sqlite')
#di.connect()
#di.initDb()

di = serverDataInterface('http://127.0.0.1:5000/')


'''
Initialization DataInterface
'''

'''
Test Data Loading

    Pippo is infected and passed in two places
    Pluto not passed for any palces in common with others
    Paperino passed where pluto passed but in a different timedelta
    Paperone was detected infected by never crossed any other paths
    Gastone crossed pluto's at the same time

Timeline  1 2 3 4 5 6 7 8 9 10 11 12 13 March 2020
Pippo     |-1-|       |-2-|          * Detected infected
Pluto     |-3-|             |-4-|
Paperino        |-1-|       |-4-|
Paperone              |-4-|          * Detected infected
Gastone   |-3-|       |-2-|          => Probable Infected

'''

userIdPippo = di.getUserIdOrCreateIt('pippo@pippo.com')

di.updateUserId(userIdPippo,datetime2ms( datetime.strptime('2020-03-13T10:00', '%Y-%m-%dT%H:%M')))
userIdPluto = di.getUserIdOrCreateIt('pluto@pluto.com')
userIdPaperino = di.getUserIdOrCreateIt('paperino@paperino.com')
userIdPaperone = di.getUserIdOrCreateIt('paperone@paperone.com')
di.updateUserId(userIdPaperone,datetime2ms( datetime.strptime('2020-03-13T10:00', '%Y-%m-%dT%H:%M')))
userIdGastone = di.getUserIdOrCreateIt('gastone@gastone.com')

di.addActivities(
[{
'userId':userIdPippo,
'locationId':1,
'startTime':datetime2ms( datetime.strptime('2020-03-1T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-3T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPippo,
'locationId':2,
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPluto,
'locationId': 3,
'startTime':datetime2ms( datetime.strptime('2020-03-01T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-03T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPluto,
'locationId':4,
'startTime':datetime2ms( datetime.strptime('2020-03-10T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-11T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperino,
'locationId':1,
'startTime':datetime2ms( datetime.strptime('2020-03-04T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-06T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperino,
'locationId':4,
'startTime':datetime2ms( datetime.strptime('2020-03-10T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-11T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperone,
'locationId':4,
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdGastone,
'locationId':3,
'startTime':datetime2ms( datetime.strptime('2020-03-01T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-03T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdGastone,
'locationId':2,
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
}]
)


'''
Test data featching
'''

print('\nPippo\'s Visits ( userid:',userIdPippo,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPippo)
print(activitiesList)
plotActivitiesList(activitiesList)

print('\nPluto\'s Visits ( userid:',userIdPluto,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPluto)
plotActivitiesList(activitiesList)

print('\nPaperino\'s Visits ( userid:',userIdPaperino,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPaperino)
plotActivitiesList(activitiesList)

print('\nPaperone\'s Visits ( userid:',userIdPaperone,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPaperone)
plotActivitiesList(activitiesList)

print('\nGastone\'s Visits ( userid:',userIdGastone,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdGastone)
plotActivitiesList(activitiesList)

'''
Test core queries
'''

#Return infected visits
print('\nInfected Activities')
visitList = di.getInfectedVisits()
plotInfectedActivitiesList(visitList)


userList = di.getUsers()

if userList is None: exit()
for user in userList:
    print()
    print('User: ',user)
    print('Infected visits:')
    plotInfectedUserVisitList(di.getInfectedVisitsOfUser(int(user['id'])))


#TODO: If a new potential infected is fount, we should notify the other potential affected