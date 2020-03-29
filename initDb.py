
from dbDataInterface import dbDataInterface

di = dbDataInterface('codevscovid.sqlite')
di.connect()
di.initDb()
