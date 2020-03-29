import json
from datetime import datetime
from datetime import timedelta
from dataManager import addTimeLine, getUserIdOrCreateIt, updateUserId
import sqlite3
import time

# User inputs
jsonFileName = "Takeout/Location History/Semantic Location History/2020/2020_MARCH.json"
email ='pippo@gmail.com'
infectionTimeMs = ''#int(time.mktime(datetime.now().timetuple())*1000)

# Configurations
dbname = 'codevscovid.sqlite'
expirationDays = timedelta(days=7)

conn = sqlite3.connect(dbname)
cur = conn.cursor()

f = open(jsonFileName, "r")
data = json.loads(f.read())

userId = getUserIdOrCreateIt(email,cur)

'''
updateUserId(userId,infectionTimeMs,cur)
print('expirationDays:',expirationDays.days)

(nPlaceVisit,nActiveSegments,nMoreThanOneType) = addTimeLine(data['timelineObjects'],expirationDays,userId,cur)

print('nPlaceVisit',nPlaceVisit)
print('nActiveSegments',nActiveSegments)
print('nMoreThanOneType',nMoreThanOneType)

'''

#Return visits of infected people
cur.execute('''SELECT  vInfected.id, uInfected.id, vInfected.startTime, vInfected.stopTime
    FROM Visit AS vInfected
    JOIN User AS uInfected ON vInfected.userId = uInfected.id
    WHERE uInfected.infectionTime<>'' ''')

print('(vInfected.id, uInfected.id, vInfected.startTime, vInfected.stopTime)')
infectedVisits = cur.fetchall()
for infectedVisit in infectedVisits:
    print(infectedVisit)

#(userId,)
cur.execute('''SELECT vQuery.id, vInfectedid, uInfectedid, vInfectedstartTime, vInfectedstopTime
    FROM(
        SELECT  vInfected.id AS vInfectedid, uInfected.id AS uInfectedid, vInfected.startTime AS vInfectedstartTime, vInfected.stopTime AS vInfectedstopTime
        FROM Visit AS vInfected
        JOIN User AS uInfected ON vInfected.userId = uInfected.id
        WHERE uInfected.infectionTime<>''
    )
    JOIN Visit AS vQuery
    WHERE vQuery.id = ?''',(userId,))

print('(vQuery.id, uInfected.id, vInfected.startTime, vInfected.stopTime)')
infectedVisits = cur.fetchall()
for infectedVisit in infectedVisits:
    print(infectedVisit)

conn.commit()
cur.close()
