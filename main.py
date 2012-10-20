import requests
import json

r = requests.get('http://posterous.com/api/2/sites/arsatiki/posts/public')
print "Found", len(r.json[0]), "items"
print "Keys:"
for k in r.json[0]:
    print "-", k