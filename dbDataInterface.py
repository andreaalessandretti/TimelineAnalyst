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

    def getLocationIdOrCreateIt(self,data):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('SELECT * FROM Location WHERE placeId = ? ', (data['placeId'],))
        row = cur.fetchone()
        if row is None:
            cur.execute('''INSERT INTO Location (placeId,name,address)
                    VALUES (:placeId,:name,:address)''', (data))
            userId = cur.lastrowid;
            print('Email added wirh id:',userId)
        else:
            print('Email already existing')
            userId = row[0]
        return userId
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
            	"id"	INTEGER NOT NULL UNIQUE,
                "placeId" TEXT,
                "name" TEXT,
                "address" TEXT,
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
        data['locationId'] = self.getLocationIdOrCreateIt({'placeId':data['placeId'],'name':data['name'],'address':data['address']})
        cur.execute('''INSERT INTO Visit (userId,startTime,stopTime,locationId) VALUES (:userId,:startTime,:stopTime,:locationId)''',data)

    def addActivities(self,activityList):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        for activity in activityList:
            self.addActivity(activity)

    def getVisitListByUserIdWithDatetime(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('''
        SELECT l.name AS name, l.address AS address,v.startTime AS startTimeMs, v.stopTime AS stopTimeMs  FROM Visit AS v
            JOIN Location AS l ON l.id = v.locationId
            WHERE userId = ? ''', (userId,))
        visits = cur.fetchall()
        listVisit = [];
        for visit in visits:
            listVisit.append({
                'name':visit[0],
                'address':visit[1],
                 'startTimeStr':ms2str(visit[2]),
                 'stopTimeStr':ms2str(visit[3])
            })
        return listVisit

    def getSqlInfectedVisits(self):
        return '''SELECT  l.name AS name, l.address AS address, vInfected.id AS vInfectedId, uInfected.id AS uInfectedId, vInfected.startTime AS vInfectedstartTime, vInfected.stopTime AS vInfectedstopTime, vInfected.locationId AS vInfectedLocationId
            FROM Visit AS vInfected
            JOIN User AS uInfected ON vInfected.userId = uInfected.id
            JOIN Location AS l ON vInfected.locationId = l.id
            WHERE uInfected.infectionTime<>'' '''

    def getCoundedInfectedLocation(self):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('SELECT COUNT(*) AS nPositiveVisits, name, address FROM('+self.getSqlInfectedVisits()+') GROUP BY vInfectedLocationId ORDER BY nPositiveVisits DESC' )
        locations = cur.fetchall()
        listLocations = [];
        for location in locations:
            listLocations.append({
                'name':location[1],
                 'address':location[2],
                 'nPositiveVisits':location[0]
            })
        return listLocations

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
    def getSqlInfectedVisitsOfUserAfterSELECT(self):
        return '''FROM('''+self.getSqlInfectedVisits()+ ''')
        JOIN Visit AS vQuery
        WHERE vQuery.userId = ?
        AND NOT( vQuery.startTime>vInfectedstopTime OR vQuery.stopTime<vInfectedstartTime)
        AND vQuery.locationId =  vInfectedLocationId'''

    def getInfectedVisitsOfUser(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('''SELECT vQuery.id, vInfectedId, uInfectedId, vInfectedstartTime, vInfectedstopTime, vInfectedLocationId, name, address
            '''+self.getSqlInfectedVisitsOfUserAfterSELECT(),(userId,))
        visits = cur.fetchall()
        listVisit = [];
        for visit in visits:
            listVisit.append({
                'vQuery.id':visit[0],'vInfectedId':visit[1],'uInfectedId':visit[2],
                 'vInfectedstartTime':ms2str(visit[3]),
                 'vInfectedstopTime':ms2str(visit[4]),
                 'vInfectedLocationId':visit[5],
                 'name':visit[6],
                 'address':visit[7]
            })
        return listVisit

    def getInfectedVisitsOfUserShort(self,userId):
        if self.cur is None: raise Exception('connection', 'connection needed')
        cur = self.cur
        cur.execute('''SELECT name, address, vInfectedstartTime, vInfectedstopTime
            '''+self.getSqlInfectedVisitsOfUserAfterSELECT(),(userId,))
        visits = cur.fetchall()
        listVisit = [];
        for visit in visits:
            listVisit.append({
                'name':visit[0],'address':visit[1],
                 'vInfectedstartTime':ms2str(visit[2]),
                 'vInfectedstopTime':ms2str(visit[3])
            })
        return listVisit
