
from datetime import datetime
from datetime import timedelta
from timeManager import datetime2ms, ms2datetime, ms2str
import sqlite3
def addTimeLine(timelineObjects,expirationDays,userId,cur):#data['timelineObjects']
    nActiveSegments  = 0
    nPlaceVisit = 0
    nMoreThanOneType = 0
    now = datetime.now()
    print('NOW:',now)
    for d in timelineObjects:
        if 'activitySegment' in d: nActiveSegments = nActiveSegments + 1
        if 'placeVisit' in d:
            visit = d['placeVisit']
            nPlaceVisit = nPlaceVisit + 1
            startTimeMs = int(visit['duration']['startTimestampMs'])
            endTimeMs = int(visit['duration']['startTimestampMs'])

            ageVisit = now-datetime.fromtimestamp(startTimeMs/1000)

            if ageVisit>expirationDays:
                print(ageVisit,'DISCARDED')
            else:
                visitTuple = (userId, startTimeMs, endTimeMs, visit['location']['placeId'])
                cur.execute('''INSERT INTO Visit (userId, startTime, stopTime,locationId)
                                VALUES (?, ?, ?, ?)''', visitTuple)
                print('added',visitTuple)

        if len(d) > 1: nMoreThanOneType = nMoreThanOneType + 1
    return (nPlaceVisit,nActiveSegments,nMoreThanOneType)

def getUserIdOrCreateIt(email,cur):
    cur.execute('SELECT * FROM User WHERE email = ? ', (email,))
    row = cur.fetchone()
    if row is None:
        cur.execute('''INSERT INTO User (email)
                VALUES (?)''', (email,))
        userId = cur.lastrowid;
        print('Email added wirh id:',userId)
    else:
        print('Email already existing')
        userId = row[0]
    return userId

def updateUserId(userId,infectionTime,cur):

    cur.execute('UPDATE User SET infectionTime = ? WHERE id = ?',
                (infectionTime,userId,))

def getMyInfectedVisits(cur,userId):
    cur.execute('''SELECT vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId
        FROM(
            SELECT  vInfected.id AS vInfectedId, uInfected.id AS uInfectedId, vInfected.startTime AS vInfectedstartTime, vInfected.stopTime AS vInfectedstopTime, vInfected.locationId AS vInfectedLocationId
            FROM Visit AS vInfected
            JOIN User AS uInfected ON vInfected.userId = uInfected.id
            WHERE uInfected.infectionTime<>''
        )
        JOIN Visit AS vQuery
        WHERE vQuery.userId = ?
        AND NOT( vQuery.startTime>vInfectedstopTime OR vQuery.stopTime<vInfectedstartTime)
        AND vQuery.locationId =  vInfectedLocationId''',(userId,))

    return cur.fetchall()
def initDb(dbname):
    try:
        conn = sqlite3.connect(dbname)
        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS Location')
        cur.execute('DROP TABLE IF EXISTS User')
        cur.execute('DROP TABLE IF EXISTS Visit')

        cur.execute('''
            CREATE TABLE "Location" (
        	"id"	TEXT NOT NULL UNIQUE,
        	PRIMARY KEY("id"))''')
        cur.execute('''
            CREATE TABLE "Visit" (
        	"id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "userId" INTEGER NOT NULL,
        	"startTime"	INTEGER NOT NULL,
        	"stopTime"	INTEGER NOT NULL,
        	"locationId"	INTEGER NOT NULL
        )''')
        cur.execute('''
            CREATE TABLE User (
            "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
            "email" TEXT NOT NULL,
            "infectionTime"	INTEGER)''')
        conn.commit()
        cur.close()
        print('#############################')
        print('Database',dbname,'initialized')
        print('#############################')
    except Exception as ex:
        print('Error creating Database',dbname,':')
        print(ex)
        exit()

def addActivity(cur,data):

#    cur.execute('''INSERT INTO Visit (userId,startTime,stopTime,locationId) VALUES (?,?,?,?)''',
#        (data['userId'], data['startTime'], data['stopTime'], data['locationId']))
    cur.execute('''INSERT INTO Visit (userId,startTime,stopTime,locationId) VALUES (:userId,:startTime,:stopTime,:locationId)''',data)

def addActivities(cur,activityList):
    for activity in activityList:
        addActivity(cur,activity)
def getVisitListByUserIdWithDatetime(cur,userId):
    cur.execute('SELECT * FROM Visit WHERE userId = ? ', (userId,))
    visits = cur.fetchall()
    listVisit = [];
    for visit in visits:
        listVisit.append({
            'id':visit[0],'userId':visit[1],
             'startTimeStr':ms2str(visit[2]),
             'stopTimeStr':ms2str(visit[3]),
             'locationId':visit[4]
        })
    return listVisit
