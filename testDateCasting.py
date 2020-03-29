
from timeManager import datetime2ms, ms2datetime
from datetime import datetime

print(ms2datetime(datetime2ms( datetime.strptime('2020-03-1T10:00', '%Y-%m-%dT%H:%M'))))
