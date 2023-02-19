from datetime import datetime
import math

def getStamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return math.floor(timestamp)