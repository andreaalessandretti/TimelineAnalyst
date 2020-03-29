#https://dzone.com/articles/restful-web-services-with-python-flask
from flask import Flask
from flask import jsonify
from flask import request
import sqlite3
from dataManager import initDb

app = Flask(__name__)

dbname = 'codevscovid.sqlite'

empDB=[
 {
 'id':'101',
 'name':'Saravanan S',
 'title':'Technical Leader'
 },
 {
 'id':'201',
 'name':'Rajkumar P',
 'title':'Sr Software Engineer'
 }
 ]

dbname = 'codevscovid.sqlite'

@app.route('/empdb/employee',methods=['GET'])
def getAllEmp():
    return jsonify({'emps':empDB})

@app.route('/empdb/employee/<empId>',methods=['GET'])
def getEmp(empId):
    usr = [ emp for emp in empDB if (emp['id'] == empId) ]
    return jsonify({'emp':usr})

@app.route('/empdb/employee',methods=['POST'])
def createEmp():
    dat = {
        'id':request.json['id'],
        'name':request.json['name'],
        'title':request.json['title']
    }
    empDB.append(dat)
    return jsonify(dat)

if __name__ == '__main__':
    app.debug = True
    initDb(dbname)
    app.run()
