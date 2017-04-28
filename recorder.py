# coding:utf-8
import os


import subprocess

import re

import sys

origin_event_file = os.path.join(os.getcwd(), "events.sh")

STOP_FLAG = False
PID = None

EVENT_LINE_RE = re.compile(r"\[.+?(\d+)\.(\d+)\] (\S+): (\S+) (\S+) (\S+)")


def shell_command(cmd, result=False):
    print "cur cmd ==> " + cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.STDOUT)
    global PID
    PID = p.pid
    while True:
        buff = p.stdout.readline()
        if buff == '' and p.poll() != None:
            break
        elif result is True:
            return buff


def record(fpath, t_fix=0.1, last_time=None, eventNum=None):
    record_command = "adb shell getevent -t"
    adb = subprocess.Popen(record_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    outputFile = open(fpath, 'w')
    outputFile.write("#!/bin/sh\n")
    while adb.poll() is None:
        try:
            line = adb.stdout.readline().decode('utf-8', 'replace').strip()
            match = EVENT_LINE_RE.match(line.strip())
            if match is not None:
                tsec, tmsec, dev, etype, ecode, data = match.groups()
                cur_time = float(tsec) + float(tmsec[:2]) / 100

                if last_time is not None:
                    diff_time = (cur_time - last_time)
                    if diff_time > 0.2:
                        outputFile.write('sleep %.2f\n' % (diff_time - t_fix,))
                last_time = cur_time

                if eventNum is not None and '/dev/input/event%s' % (eventNum) != dev:
                    continue
                etype, ecode, data = int(etype, 16), int(ecode, 16), int(data, 16)
                outputFile.write("sendevent %s %s %s %s\n" % (dev, etype, ecode, data))
        except KeyboardInterrupt:
            break
        if len(line) == 0:
            break
    outputFile.close()


def play():
    shell_command("adb push events.sh /data/local/tmp/")
    shell_command("adb shell chmod 755 /data/local/tmp/events.sh")
    shell_command("adb shell sh /data/local/tmp/events.sh")


def prepare():
    if os.path.isfile(origin_event_file):
        os.remove(origin_event_file)
    shell_command("adb logcat -c")
    print "clear all log file."


if __name__ == '__main__':
    if sys.argv[1] == "record":
        prepare()
        record(origin_event_file)
    elif sys.argv[1] == "play":
        shell_command("adb push events.sh /data/local/tmp/")
        shell_command("adb shell chmod 755 /data/local/tmp/events.sh")
        shell_command("adb shell sh /data/local/tmp/events.sh")
