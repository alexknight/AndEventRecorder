import os
import time


def monitor_change(path):
    count = 0
    thefile = open(path, "r")
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            count += 1
            print "count: " + str(count)
            if count > 150:
                print "record finish"
                thefile.close()
                break
            continue


# if __name__ == '__main__':
#     logfile = open(os.path.join(os.getcwd(), "events.txt"), "r")
#     loglines = monitor(logfile)
#     for line in loglines:
#         print line
