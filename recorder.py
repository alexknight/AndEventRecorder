# coding:utf-8
import os
import threading
import sys

import subprocess

import time

from eventparser import EventParser
from watcher import monitor_change

origin_event_file = os.path.join(os.getcwd(), "events.txt")
parser_event_file = os.path.join(os.getcwd(), "events.sh")

STOP_FLAG = False
PID = None


def record_daemon():
    shell_command("/home/alex/Android/Sdk/platform-tools/adb shell getevent -t > " + origin_event_file)


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


def prepare():
    if os.path.isfile(origin_event_file):
        os.remove(origin_event_file)
    if os.path.isfile(parser_event_file):
        os.remove(parser_event_file)
    shell_command("adb logcat -c")
    # shell_command("adb logcat -d > log/install.log")
    print "clear all log file."


def main():
    if sys.argv[1] == "start":
        prepare()
        t = threading.Thread(target=record_daemon, args=())
        t.setDaemon(True)
        t.start()
        time.sleep(3)
        start = time.time()
        monitor_change(origin_event_file)  # block job
        print "cost " + str(time.time() - start)
        if PID is not None:
            os.killpg(PID, 9)
        
        # parser result to sh scripts
        event_parser = EventParser(origin_event_file)
        event_parser.get_events().save(parser_event_file)

    elif sys.argv[1] == "play":
        shell_command("/usr/bin/sh " + parser_event_file)


if __name__ == '__main__':
    prepare()
    t = threading.Thread(target=record_daemon, args=())
    t.setDaemon(True)
    t.start()
    time.sleep(2)
    start = time.time()
    monitor_change(origin_event_file)  # block job
    print "cost " + str(time.time() - start)
    if PID is not None:
        os.kill(PID, 9)
        shell_command('ps -ef | grep "getevent" | grep -v "grep" | cut -c 9-15 | xargs kill -9')

    # parser result to sh scripts
    event_parser = EventParser(origin_event_file)
    event_parser.get_events().save(parser_event_file)
