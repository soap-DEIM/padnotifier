import sys
import getopt
import urllib
from HTMLParser import HTMLParser

opts, args = getopt.getopt(sys.argv[1:], 'g:', ['group='])


def getGroup(options):
    # debug for group D
    g = 3
    for o, v in options:
        if o in ('-g', '--group'):
            g = int(v)
    return g

group = getGroup(opts)

time_today = []
time_tomorrow = []

event_time_today = []
event_time_tomorrow = []


def getTime(time, event_time):
    for i, v in enumerate(time):
        if i % 5 == group:
            if v.endswith('am'):
                v = v[:-3]
                if v == '12':
                    v = '0'
            elif v.endswith('pm'):
                v = v[:-3]
                if v != '12':
                    v = str((int(v) + 12) % 24)
            event_time.append(v)


class Parser(HTMLParser):

    def __init__(self, group):
        HTMLParser.__init__(self)
        self.metal = False
        self.today = False
        self.tomorrow = False
        self.group = group

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for name, value in attrs:
                if name == 'id' and value == 'today':
                    self.today = True
                if name == 'id' and value == 'tomorrow':
                    self.today = False
                    self.tomorrow = True
        if tag == 'td':
            for name, value in attrs:
                if name == 'class' and value == 'metaltime':
                    self.metal = True

    def handle_data(self, data):
        if self.metal:
            if self.today:
                time_today.append(data)
            elif self.tomorrow:
                time_tomorrow.append(data)

    def handle_endtag(self, tag):
        if tag == 'td':
            self.metal = False

ht = urllib.urlopen('http://www.puzzledragonx.com').read()
p = Parser(group)
p.feed(ht)
getTime(time_today, event_time_today)
getTime(time_tomorrow, event_time_tomorrow)

# DEBUG #
for i in event_time_today:
    print '[DEBUG] today', i

for i in event_time_tomorrow:
    print '[DEBUG] tomorrow', i
# END DEBUG #
