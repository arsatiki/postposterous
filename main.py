import requests
import json
import sys

if len(sys.argv) < 2:
    sys.exit()

vals = dict(site=sys.argv[1])


r = requests.get('http://posterous.com/api/2/sites/%(site)s/posts/public' % vals)
print "Found", len(r.json), "items"
print "Keys:"
for k in sorted(r.json[0]):
    print "-", k


interesting =     '''
display_date
short_url
id
title
media
slug
full_url
tags
site
user
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
    print "Post", p['title']
    for k in interesting:
        print k, p[k]
    print

