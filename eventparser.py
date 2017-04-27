# coding: utf-8
import os
import re

_re = re.compile(r'[^\d]*(?P<sec>\d+)[.-](?P<msec>\d+)[:\]] (?P<device>[^:]+):'
                 ' (?P<class>[0-9a-f]+) (?P<event>[0-9a-f]+) (?P<params>[0-9a-f]+)')


class EventParser(object):
    def __init__(self, event_file, regex=_re, t_fix=0.1, last_time=None):
        self.event_file = event_file
        self.regex = regex
        self.t_fix = t_fix
        self.last_time = last_time
        self.events = []

    def get_events(self):
        self.events.append('#!/bin/sh')
        for line in open(self.event_file, 'rt'):
            m = self.regex.match(line)
            if m is not None:
                d = m.groupdict()
                cur_time = float(d['sec']) + float(d['msec'][:2]) / 100
                if self.last_time is not None:
                    diff_time = (cur_time - self.last_time)
                    if diff_time > 0.2:
                        print 'sleep %.2f' % (diff_time - self.t_fix,)
                self.last_time = cur_time
                self.events.append('sendevent' +
                                   " " + d['device'] +
                                   " " + str(int(d['class'], 16)) +
                                   " " + str(int(d['event'], 16)) +
                                   " " + str(int(d['params'], 16)))
            else:
                self.events.append('#' + " " + line.strip('\n\r\t '))
        return self

    def save(self, file_path):
        # def _create_dir(dest):
        #     _parent = os.path.dirname(dest)
        #     if os.path.exists(_parent):
        #         _create_dir(_parent)
        #         os.mkdir(dest)
        #
        # _create_dir(os.path.dirname(file_path))

        with open(file_path, "wb") as f:
            for line in self.events:
                f.write(line + "\n")


# if __name__ == '__main__':
#     EventParser(os.path.join(os.getcwd(), "events.txt")).get_events().save(os.path.join(os.getcwd(), "events.sh"))
