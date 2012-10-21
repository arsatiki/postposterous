import requests
import json
import sys
from dateutil import parser
from dateutil.tz import gettz
import os

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

def write(site, p):
    slug = p['slug']
    path = '%s/%s' % (site, slug)
    root = os.getcwd()
    os.makedirs(path)
    os.chdir(path)
    with open('post.html', 'w') as f:
        f.write(p['body_cleaned'])
    with open('metadata.yaml') as f:
        if 'date' in p:
            f.write("date: %(date)s\n" % p)
    # TODO
    # Photos
    # Comments
    os.chdir(root)

def main():
    if len(sys.argv) < 3:
        sys.exit()

    tz = gettz(sys.argv[2])
    if tz is None:
        print "Bad timezone"
        sys.exit()

    site = sys.argv[1]

    posts = get_posts(site)

    print "Found", len(posts), "posts"
    for p in posts:
        if 'display_date' in p:
            p['date'] = fix_date(p['display_date'], tz)

        print "Processing", p['slug']
        write(site, p)

if __name__ == "__main__":
    main()
