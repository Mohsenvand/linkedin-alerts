#this script gets creates an XML document with the current users connections
#and using the id tags will create a text file of updates for each person

import oauth2 as oauth
#import httplib2
#import time
#import os
#import simplejson
#import urlparse
import datetime
from xml.dom import minidom
#import pylab

#praful tokens
API_KEY = '149yt4504foj'
API_SECRET = 'V5149cV4nQyiDoF1'
OAUTH_TOKEN = '7f1c4382-3142-408c-baa6-6814f3f647d7'
OAUTH_TOKEN_SECRET = '5102a042-5cf3-4839-95ce-7b372e50e495'

#redundant, remove later
consumer_key = API_KEY
consumer_secret = API_SECRET
user_token = OAUTH_TOKEN
user_secret = OAUTH_TOKEN_SECRET

#instantiate objects to begin calls
consumer = oauth.Consumer(consumer_key, consumer_secret)
access_token = oauth.Token(key=user_token, secret=user_secret)
client = oauth.Client(consumer, access_token)

#get xml doc of connections
LINKEDIN_API = "http://api.linkedin.com/v1"
my_connections = LINKEDIN_API + "/people/~/connections:(id,first-name,last-name)"
resp, content = client.request(my_connections)
f = open('contact_list.xml', 'w')
f.write(content)
f.close()


#create data structure
class Person(object):
    _registry = []

    def __init__(self, p_id, p_first, p_last):
        self._registry.append(self)
        self.id = p_id
        self.first = p_first
        self.last = p_last
        self.updates = []
        self.times = []

    def getID(self):
        return self.id

    def getFirst(self):
        return self.first

    def getLast(self):
        return self.last

    def addUpdate(self, u_type, u_time):
        self.updates.append(u_type)
        self.times.append(u_time)

    def getUpdates(self):
        return self.updates

    def getStamp(self):
        return self.times

    def modTime(self, time):
        """
        Convert LinkedIn's epoch time (in ms) to Python datetime

        str (time in ms) --> str (Python formatted datetime)
        """
        t = int(time)
        t = t / 1000.
        epoch_to_date = datetime.datetime.fromtimestamp(t)
        return epoch_to_date.strftime("%a %b-%d-%Y %I:%m %p")


#parse xml doc and create a list of ids and names
ids = []
names = []
xmldoc = minidom.parse('contact_list.xml')
people = xmldoc.getElementsByTagName('person')
for person in people:
    person_id = str(person.childNodes[1].childNodes[0].nodeValue)
    if  person_id != ('private'):
        ids.append(person_id)
        #print person.childNodes[3].firstChild.nodeValue
        f_name = person.childNodes[3].firstChild.nodeValue.encode("utf-8")
        l_name = person.childNodes[5].firstChild.nodeValue.encode("utf-8")
        names.append([f_name, l_name])


#use id's to get list of update times, and update types
for i in range(len(ids)):
    #time = []
    #updates = []
    curr_id = ids[i]
    network_updates = LINKEDIN_API + "/people/id=%s/network/updates?scope=self" % curr_id
    resp, content = client.request(network_updates)
    xmldoc = minidom.parseString(content)
    f = open('update.xml', 'w')
    f.write(content)
    f.close()
    timelist = xmldoc.getElementsByTagName('timestamp')
    typelist = xmldoc.getElementsByTagName('update-type')
    p = Person(curr_id, names[i][0], names[i][1])
    if len(typelist) > 0:
        for j in range(len(typelist)):
            p.addUpdate(typelist[j].firstChild.nodeValue,
                    timelist[j].firstChild.nodeValue)
