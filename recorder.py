# coding:utf-8
import os
import threading

import time

import sys

from eventparser import EventParser

origin_event_file = os.path.join(os.getcwd(), "event.txt")
parser_event_file = os.path.join(os.getcwd(), "event.sh")

STOP_FLAG = False


def record_daemon():
    shell_command("adb shell getevent -t > " + origin_event_file)


def shell_command(cmd):
    print "cur cmd ==> " + cmd
    os.system(cmd)


def prepare():
    if os.path.isfile(origin_event_file):
        os.remove(origin_event_file)
    if os.path.isfile(parser_event_file):
        os.remove(parser_event_file)
    shell_command("adb logcat -c")
    shell_command("adb logcat -d > log/install.log")
    print "clear all log file."


def monitor_events():
    pass


def main():
    if sys.argv[1] == "start":
        prepare()
        t = threading.Thread(target=record_daemon, args=())
        t.setDaemon(True)
        t.start()

        event_parser = EventParser(origin_event_file)
        event_parser.get_events().save(parser_event_file)
    elif sys.argv[1] == "play":
        shell_command("/usr/bin/sh " + parser_event_file)


if __name__ == '__main__':
    main()
