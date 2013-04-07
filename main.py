# encoding: utf-8
import requests
import json
import sys
from dateutil import parser
from dateutil.tz import gettz
import os
import codecs

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

def write_images(p):
    images = p['media']['images']
    for img in images:
        url = img['full']['url']
        _, _, filename = url.rpartition('/')
        print '\t', filename
        
        r = requests.get(url)
        with open(filename, 'w') as f:
            f.write(r.content)

def write(site, p):
    slug = p['slug']
    ymd = p['date'].strftime("%Y-%m-%d")
    path = '%s/%s-%s' % (site, ymd, slug)
    root = os.getcwd()
    try:
        os.makedirs(path)
    except OSError:
        pass
    os.chdir(path)
    with codecs.open('post.html', 'w', 'utf-8') as f:
        f.write(p['body_cleaned'])
    with codecs.open('metadata.yaml', 'w', 'utf-8') as f:
        f.write("title: %(title)s\n" % p)
        f.write("date: %(date)s\n" % p)
    write_images(p)
    # TODO
    # Comments
    os.chdir(root)

def main():
    if len(sys.argv) < 3:
        print "Usage: main.py site timezone"
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
