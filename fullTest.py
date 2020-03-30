
from timeManager import datetime2ms, ms2datetime
from datetime import datetime
import plotUtils
import sqlite3
from dbDataInterface import dbDataInterface
from serverDataInterface import serverDataInterface


dbTestOnly = False
if dbTestOnly:
    di = dbDataInterface('codevscovid.sqlite')
    di.connect()
    di.initDb()
else:
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
Paperone              |-1-|          * Detected infected
Gastone   |-3-|       |-2-|          => Probable Infected

'''

userIdPippo = di.getUserIdOrCreateIt('pippo@pippo.com')

di.updateUserId(userIdPippo,datetime2ms( datetime.strptime('2020-03-13T10:00', '%Y-%m-%dT%H:%M')))
userIdPluto = di.getUserIdOrCreateIt('pluto@pluto.com')
userIdPaperino = di.getUserIdOrCreateIt('paperino@paperino.com')
userIdPaperone = di.getUserIdOrCreateIt('paperone@paperone.com')
di.updateUserId(userIdPaperone,datetime2ms( datetime.strptime('2020-03-13T10:00', '%Y-%m-%dT%H:%M')))
userIdGastone = di.getUserIdOrCreateIt('gastone@gastone.com')


inputVisits = [{
'userId':userIdPippo,
'placeId':'uno','name':'casa1','address':'via1',
'startTime':datetime2ms( datetime.strptime('2020-03-1T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-3T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPippo,
'placeId':'due','name':'casa2','address':'via2',
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPluto,
'placeId':'tre','name':'casa3','address':'via3',
'startTime':datetime2ms( datetime.strptime('2020-03-01T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-03T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPluto,
'placeId':'quattro','name':'casa4','address':'via4',
'startTime':datetime2ms( datetime.strptime('2020-03-10T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-11T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperino,
'placeId':'uno','name':'casa1','address':'via1',
'startTime':datetime2ms( datetime.strptime('2020-03-04T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-06T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperino,
'placeId':'quattro','name':'casa4','address':'via4',
'startTime':datetime2ms( datetime.strptime('2020-03-10T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-11T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdPaperone,
'placeId':'uno','name':'casa1','address':'via1',
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdGastone,
'placeId':'tre','name':'casa3','address':'via3',
'startTime':datetime2ms( datetime.strptime('2020-03-01T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-03T10:00', '%Y-%m-%dT%H:%M'))
},{
'userId':userIdGastone,
'placeId':'due','name':'casa2','address':'via2',
'startTime':datetime2ms( datetime.strptime('2020-03-07T10:00', '%Y-%m-%dT%H:%M')),
'stopTime':datetime2ms( datetime.strptime('2020-03-09T10:00', '%Y-%m-%dT%H:%M'))
}]

di.addActivities(inputVisits)
print('Input data')

print(plotUtils.plotInputVisitListShort(inputVisits))

'''
Test data featching
'''

print('\nPippo\'s Visits ( userid:',userIdPippo,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPippo)
print(activitiesList)
print(plotUtils.plotActivitiesList(activitiesList))

print('\nPluto\'s Visits ( userid:',userIdPluto,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPluto)
print(plotUtils.plotActivitiesList(activitiesList))

print('\nPaperino\'s Visits ( userid:',userIdPaperino,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPaperino)
print(plotUtils.plotActivitiesList(activitiesList))

print('\nPaperone\'s Visits ( userid:',userIdPaperone,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdPaperone)
print(plotUtils.plotActivitiesList(activitiesList))

print('\nGastone\'s Visits ( userid:',userIdGastone,')')
activitiesList = di.getVisitListByUserIdWithDatetime(userIdGastone)
print(plotUtils.plotActivitiesList(activitiesList))

'''
Test core queries
'''

#Return infected visits
print('\nInfected Visits')
visitList = di.getInfectedVisits()
print(plotUtils.plotInfectedActivitiesList(visitList))

userList = di.getUsers()

if userList is None: exit()
for user in userList:
    print()
    print('User: ',user)
    print('Infected visits:')
    if dbTestOnly:
        print(plotUtils.plotInfectedUserVisitList(di.getInfectedVisitsOfUser(int(user['id']))))
    else:
        print(plotUtils.plotInfectedUserVisitListShort(di.getInfectedVisitsOfUserShort(int(user['id']))))

print(plotUtils.plotCoundedInfectedLocation(di.getCoundedInfectedLocation()))
#TODO: If a new potential infected is fount, we should notify the other potential affected
