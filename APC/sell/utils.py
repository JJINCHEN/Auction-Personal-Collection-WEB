import time


def get_stamp_by_time(mytime):
    timeArray = time.strptime(mytime, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_time_by_stamp(mystamp):
    timeArray = time.localtime(int(mystamp))
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


def get_now_stamp():
    return str(int(time.time()))

if __name__ == "__main__":
    print(get_stamp_by_time("2021-02-18 00:00:00"))
