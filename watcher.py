import os
import time

start = time.time()


def monitor(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            count_time = time.time() - start
            if count_time > 15:
                print "record finish"
                break
            continue
        yield line


if __name__ == '__main__':
    logfile = open(os.path.join(os.getcwd(), "events.txt"), "r")
    loglines = monitor(logfile)
    for line in loglines:
        print line
