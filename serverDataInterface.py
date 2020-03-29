import sqlite3
import requests
import json
from timeManager import datetime2ms, ms2datetime, ms2str
class serverDataInterface:
    url = ''

    def __init__(self,url):
        self.url = url

    def connect(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cur = self.conn.cursor()

    def getUserIdOrCreateIt(self,email):

        r = requests.post(url = self.url+'/getuseridorcreateit', json = {'email':email})
        data = r.json()
        return data['id']

    def updateUserId(self,userId,infectionTime):
        r = requests.post(url = self.url+'/updateuserid', json = {'userId':userId,'infectionTime':infectionTime})

    def addActivities(self,activityList):
        r = requests.post(url = self.url+'/addactivities', json = {'data':activityList})

    def getVisitListByUserIdWithDatetime(self,userId):
        r = requests.post(url = self.url+'/getvisitlistbyuseridwithdatetime', json = {'userId':userId})
        return r.json()

    def getInfectedVisits(self):
        r = requests.get(url = self.url+'/getinfectedvisits')
        return r.json()

    def getUsers(self):
        r = requests.get(url = self.url+'/getusers')
        return r.json()

    def getInfectedVisitsOfUser(self,userId):
        r = requests.post(url = self.url+'/getinfectedvisitsofuser', json = {'userId':userId})
        return r.json()
