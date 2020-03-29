
from datetime import datetime
from datetime import timedelta
import time

def datetime2ms(dt):
    return int(time.mktime(dt.timetuple())*1000)

def ms2datetime(ms):
    return datetime.fromtimestamp(ms/1000)
def ms2str(ms):
    return ms2datetime(ms).strftime('%Y-%m-%dT%H:%M')
