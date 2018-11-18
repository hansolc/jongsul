import threading
from datetime import datetime
import time

hour = ""
minute = ""

end = False
def TaskCurrentTime():
    now = datetime.now()
    global end
    global hour
    global minute
    if end:
        return
    
    timer = threading.Timer(1,TaskCurrentTime)
    timer.start()
    hour = now.hour
    minute = now.minute

    #print("현재시간은 ", int(hour) , "시", int(minute), "분 입니다,")
