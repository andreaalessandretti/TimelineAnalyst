#https://dzone.com/articles/restful-web-services-with-python-flask
from flask import Flask
from flask import jsonify
from flask import request
import json
import sqlite3
from dataManager import initDb
from dbDataInterface import dbDataInterface

app = Flask(__name__)

dbname = 'codevscovid.sqlite'

dbname = 'codevscovid.sqlite'

@app.route('/getinfectedvisits',methods=['GET'])
def getInfectedVisits():
    di = dbDataInterface(dbname)
    di.connect()
    return jsonify(di.getInfectedVisits())

@app.route('/getusers',methods=['GET'])
def getUsers():
    di = dbDataInterface(dbname)
    di.connect()
    return jsonify(di.getUsers())

@app.route('/getinfectedvisitsofuser',methods=['POST'])
def getInfectedVisitsOfUser():
    di = dbDataInterface(dbname)
    di.connect()
    return jsonify(di.getInfectedVisitsOfUser(request.json['userId']))

@app.route('/getinfectedvisitsofusershort',methods=['POST'])
def getInfectedVisitsOfUserShort():
    di = dbDataInterface(dbname)
    di.connect()
    return jsonify(di.getInfectedVisitsOfUserShort(request.json['userId']))

@app.route('/getuseridorcreateit',methods=['POST'])
def getUserIdOrCreateIt():
    di = dbDataInterface(dbname)
    di.connect()
    userId = di.getUserIdOrCreateIt(request.json['email'])
    return jsonify({'id':userId})

@app.route('/updateuserid',methods=['POST'])
def updateUserId():
    di = dbDataInterface(dbname)
    di.connect()
    di.updateUserId(request.json['userId'],request.json['infectionTime'])
    return ''

@app.route('/addactivities',methods=['POST'])
def addActivities():
    di = dbDataInterface(dbname)
    di.connect()
    di.addActivities(request.json['data'])
    return ''

@app.route('/getvisitlistbyuseridwithdatetime',methods=['POST'])
def getVisitListByUserIdWithDatetime():
    di = dbDataInterface(dbname)
    di.connect()
    return jsonify(di.getVisitListByUserIdWithDatetime(request.json['userId']))


if __name__ == '__main__':
    app.debug = True

    di = dbDataInterface(dbname)
    di.connect()
    di.initDb()
    app.run()
