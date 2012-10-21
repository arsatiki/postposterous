import requests
import json
import sys
from dateutil import parser
from dateutil.tz import gettz

def fix_date(s, tz):
    if not s:
        return None
    return parser.parse(s).astimezone(tz)

def get_posts(site):
    url = 'http://posterous.com/api/2/sites/%s/posts/public' % site
    p = []
    page = 1
    while True:
        params = {'page': page}
        r = requests.get(url, params=params)
        if not r.json:
            break
        p.extend(r.json)
        page += 1
    return p
    

if len(sys.argv) < 3:
    sys.exit()

tz = gettz(sys.argv[2])
if tz is None:
    print "Bad timezone"
    sys.exit()

vals = dict(site=sys.argv[1])

posts = get_posts(sys.argv[1])

print "Found", len(posts), "items"

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

for p in posts:
    # Fix date
    other = {}
    if 'display_date' in p:
        p['date'] = fix_date(p['display_date'], tz)
    
    print "Post", p['title']
    print "Date", p['date']
    for k in interesting:
        print k, p[k]
    print

