import sqlite3
from datetime import timedelta
from timeManager import ms2datetime
from dataManager import getMyInfectedVisits

# Configurations
dbname = 'codevscovid.sqlite'
expirationDays = timedelta(days=7)

conn = sqlite3.connect(dbname)
cur = conn.cursor()

#Return visits of infected people
cur.execute('''SELECT  vInfected.id, uInfected.id, vInfected.startTime, vInfected.stopTime
    FROM Visit AS vInfected
    JOIN User AS uInfected ON vInfected.userId = uInfected.id
    WHERE uInfected.infectionTime<>'' ''')

print('Infected visits')
print('(vInfected.id, uInfected.id, vInfected.startTime, vInfected.stopTime)')
infectedVisits = cur.fetchall()
for infectedVisit in infectedVisits:
    print(infectedVisit)

userId = 1
cur.execute('''SELECT vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime
    FROM(
        SELECT  vInfected.id AS vInfectedId, uInfected.id AS uInfectedId, vInfected.startTime AS vInfectedstartTime, vInfected.stopTime AS vInfectedstopTime
        FROM Visit AS vInfected
        JOIN User AS uInfected ON vInfected.userId = uInfected.id
        WHERE uInfected.infectionTime<>''
    )
    JOIN Visit AS vQuery
    WHERE vQuery.userId = ?''',(userId,))

print('Before AND')
print('(vQuery.id, uInfected.id, vInfected.startTime, vInfected.stopTime)')
infectedVisits = cur.fetchall()
for infectedVisit in infectedVisits:
    print(infectedVisit)



#userId = 1:Pippo,2:Pluto,3:Paperino,4:Gastone
getMyInfectedVisits(cur,1)
print('Pippo\'s infected events')
print('(vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId)')
infectedVisits = cur.fetchall()
for visit in infectedVisits:
    print(visit[0],visit[1],visit[2],ms2datetime(visit[3]),ms2datetime(visit[4]),visit[5])

infectedVisits = getMyInfectedVisits(cur,2)
print('Pluto\'s infected events')
print('(vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId)')

for visit in infectedVisits:
    print(visit[0],visit[1],visit[2],ms2datetime(visit[3]),ms2datetime(visit[4]),visit[5])

infectedVisits = getMyInfectedVisits(cur,3)
print('Paperino\'s infected events')
print('(vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId)')
for visit in infectedVisits:
    print(visit[0],visit[1],visit[2],ms2datetime(visit[3]),ms2datetime(visit[4]),visit[5])

infectedVisits = getMyInfectedVisits(cur,4)
print('Paperone\'s infected events')
print('(vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId)')
for visit in infectedVisits:
    print(visit[0],visit[1],visit[2],ms2datetime(visit[3]),ms2datetime(visit[4]),visit[5])

infectedVisits = getMyInfectedVisits(cur,5)
print('Gastone\'s infected events')
print('(vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId)')

for visit in infectedVisits:
    print(visit[0],visit[1],visit[2],ms2datetime(visit[3]),ms2datetime(visit[4]),visit[5])


conn.commit()
cur.close()
