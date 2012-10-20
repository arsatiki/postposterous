import requests
import json
import sys
from dateutil import parser
from dateutil.tz import gettz

def fix_date(s, tz):
    if not s:
        return None
    return parser.parse(s).astimezone(tz)

if len(sys.argv) < 3:
    sys.exit()

tz = gettz(sys.argv[2])
if tz is None:
    print "Bad timezone"
    sys.exit()

vals = dict(site=sys.argv[1])


r = requests.get('http://posterous.com/api/2/sites/%(site)s/posts/public' % vals)
print "Found", len(r.json), "items"

interesting =     '''
media
slug
tags
replies_count
number_of_comments
comments_count
'''.split()
# bodies:
# body_full
# body_excerpt
# body_cleaned
# body_html

for p in r.json:
    # Fix date
    other = {}
    if 'display_date' in p:
        p['date'] = fix_date(p['display_date'], tz)
    
    print "Post", p['title']
    print "Date", p['date']
    for k in interesting:
        print k, p[k]
    print

