import sqlite3
import json
from timeManager import datetime2ms, ms2datetime, ms2str
class dbDataInterface:
    dbname = ''
    cur = None
    conn = None

    def __init__(self,dbname):
        self.dbname = dbname

    def __del__(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.commit()

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def addTimeLine(self,timelineObjects,expirationDays,userId):#data['timelineObjects']
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur

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

    def getUsers(self):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('SELECT * FROM User')
        users = cur.fetchall()
        userList = [];
        for user in users:
            if user[2] is None:
                infectionTime = ''
            else:
                infectionTime = ms2str(user[2])
            userList.append({
                'id':user[0],
                'email':user[1],
                'infectionTime':infectionTime
            })
        return userList

    def getUserIdOrCreateIt(self,email):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
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

    def updateUserId(self,userId,infectionTime):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('UPDATE User SET infectionTime = ? WHERE id = ?',
                    (infectionTime,userId,))

    def getMyInfectedVisits(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
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

    def initDb(self):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        conn = self.conn
        try:

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

            print('#############################')
            print('Database',self.dbname,'initialized')
            print('#############################')
        except Exception as ex:
            print('Error creating Database',self.dbname,':')
            print(ex)
            exit()

    def addActivity(self,data):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
    #    cur.execute('''INSERT INTO Visit (userId,startTime,stopTime,locationId) VALUES (?,?,?,?)''',
    #        (data['userId'], data['startTime'], data['stopTime'], data['locationId']))
        cur.execute('''INSERT INTO Visit (userId,startTime,stopTime,locationId) VALUES (:userId,:startTime,:stopTime,:locationId)''',data)

    def addActivities(self,activityList):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        for activity in activityList:
            self.addActivity(activity)

    def getVisitListByUserIdWithDatetime(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
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

    def getSqlInfectedVisits(self):
        return '''SELECT  vInfected.id AS vInfectedId, uInfected.id AS uInfectedId, vInfected.startTime AS vInfectedstartTime, vInfected.stopTime AS vInfectedstopTime, vInfected.locationId AS vInfectedLocationId
            FROM Visit AS vInfected
            JOIN User AS uInfected ON vInfected.userId = uInfected.id
            WHERE uInfected.infectionTime<>'' '''

    def getInfectedVisits(self):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute(self.getSqlInfectedVisits())
        visits = cur.fetchall()
        listVisit = [];
        for visit in visits:
            listVisit.append({
                'vInfected.id':visit[0],'uInfected.id':visit[1],
                 'vInfected.startTime':ms2str(visit[2]),
                 'vInfected.stopTime':ms2str(visit[3]),
                 'vInfected.locationId':visit[4]
            })
        return listVisit

    def getInfectedVisitsOfUser(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('''SELECT vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId
            FROM('''+self.getSqlInfectedVisits()+
                ''')
            JOIN Visit AS vQuery
            WHERE vQuery.userId = ?
            AND NOT( vQuery.startTime>vInfectedstopTime OR vQuery.stopTime<vInfectedstartTime)
            AND vQuery.locationId =  vInfectedLocationId''',(userId,))
        visits = cur.fetchall()
        listVisit = [];
        for visit in visits:
            listVisit.append({
                'vQuery.id':visit[0],'vInfectedId':visit[1],'uInfectedId':visit[2],
                 'vInfectedstartTime':ms2str(visit[3]),
                 'vInfectedstopTime':ms2str(visit[4]),
                 'vInfectedLocationId':visit[5]
            })
        return listVisit
