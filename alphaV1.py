# this script gets creates an XML document with the current users connections
# and using the id tags will create a text file of updates for each person

import oauth2 as oauth
#import httplib2
#import time
#import os
#import simplejson
#import urlparse
import datetime
from xml.dom import minidom


# praful tokens
API_KEY = 'a7fcc7d3x3m2'
API_SECRET = 'e7w5Hy2fZ8sSOKA5'
OAUTH_TOKEN = 'c17196d5-bb1e-4efe-b23a-442c7bc6ff77'
OAUTH_TOKEN_SECRET = 'b42e9b1b-e3bd-4de1-a1e0-41514dd3fb5f'

# redundant, remove later
consumer_key = API_KEY
consumer_secret = API_SECRET
user_token = OAUTH_TOKEN
user_secret = OAUTH_TOKEN_SECRET

# instantiate objects to begin calls
consumer = oauth.Consumer(consumer_key, consumer_secret)
access_token = oauth.Token(
    key=user_token,
    secret=user_secret)
client = oauth.Client(consumer, access_token)

# get xml doc of connections
LINKEDIN_API = "http://api.linkedin.com/v1"
url = LINKEDIN_API + "people/~/connections:(id,first-name,last-name)"
resp, content = client.request(url)
f = open('xml/contact_list.xml', 'w')
f.write(content)
f.close()


# create data structure
class Person(object):
    _registry = []

    def __init__(self, p_id, p_first, p_last):
        self._registry.append(self)
        self.id = p_id
        self.first = p_first
        self.last = p_last
        self.updates = []

    def getID(self):
        return self.id

    def getFirst(self):
        return self.first

    def getLast(self):
        return self.last

    def addUpdate(self, u_type, u_time):
        self.updates.append((u_type, self.modTime(u_time)))

    def getUpdates(self):
        return self.updates

    def getStamp(self):
        return self.time

    def modTime(self, time):
        """
        Convert LinkedIn's epoch time (in ms) to Python datetime

        str (time in ms) --> str (Python formatted datetime)
        """
        t = int(time)
        t = t / 1000.
        epoch_to_date = datetime.datetime.fromtimestamp(t)
        return epoch_to_date.strftime("%a %b-%d-%Y %I:%m %p")

# parse xml doc and create a list of ids and names
ids = []
names = []
xmldoc = minidom.parse('xml/contact_list.xml')
people = xmldoc.getElementsByTagName('person')
for person in people:
    if str(person.childNodes[1].childNodes[0].nodeValue) != ('private'):
        ids.append(str(person.childNodes[1].childNodes[0].nodeValue))
        f = str(person.childNodes[3].firstChild.nodeValue.encode("utf-8"))
        l = str(person.childNodes[5].firstChild.nodeValue.encode("utf-8"))
        names.append((f, l))


# use id's to get list of update times, and update types
errors = []
#max_len = 30  # len(ids)
for i in ids[:max_len]:
    updates = []
    url = LINKEDIN_API + "/people/id=%s/network/updates?scope=self&count=25" % i
    resp, content = client.request(url)

    if resp.status == 200:
        filename = 'xml/update_%s.xml' % (i)
        with open(filename, 'w') as f:
            f.write(content)
    else:
        errors.append((i, filename))
        print resp.reason

print errors
