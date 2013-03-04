#this script gets creates an XML document with the current users connections
#and using the id tags will create a text file of updates for each person

import oauth2 as oauth
import httplib2
import time, os, simplejson
import urlparse
import datetime
from xml.dom import minidom


#praful tokens
API_KEY = 'onwzvln0ksj5'
API_SECRET = 'oTmzJwbB9AFSHagM'
OAUTH_TOKEN = '420be95e-de13-4002-9023-42835b337245'
OAUTH_TOKEN_SECRET = 'f25efa3c-4d09-40e2-9045-171029899821'
#redundant, remove later
consumer_key      =   API_KEY
consumer_secret  =   API_SECRET
user_token           =   OAUTH_TOKEN
user_secret          =   OAUTH_TOKEN_SECRET

#instantiate objects to begin calls
consumer = oauth.Consumer(consumer_key, consumer_secret)
access_token = oauth.Token(
            key=user_token,
            secret=user_secret)
client = oauth.Client(consumer, access_token)




#get xml doc of connections
url = "http://api.linkedin.com/v1/people/~/connections:(id,first-name,last-name)"
resp,content = client.request(url)
f = open('contact_list.xml','w')
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

    def getID(self):
        return self.id

    def getFirst(self):
        return self.first

    def getLast(self):
        return self.last

    def addUpdate(self,u_type, u_time):
        self.updates.append((u_time, u_type))

    def getUpdates(self):
        print self.updates

    def getStamp(self):
        return self.time


##    class Updates(object):
##    _registry = []
##
##    def __init__(self, p_id, p_first, p_last, update_type, time):
##        self._registry.append(self)
##        self.id = p_id
##        self.first = p_first
##        self.last = p_last
##        self.type = update_type
##        self.time = time
##
##    def getID(self):
##        return self.id
##
##    def getFirst(self):
##        return self.first
##
##    def getLast(self):
##        return self.last
##
##    def getType(self):
##        return self.type
##
##    def getTime(self):
##        t = int(self.time)
##        t = t/1000.
##        return datetime.datetime.fromtimestamp(t).strftime("%a %b-%d-%Y %I:%m %p") #return string
##
##    def getStamp(self):
##        return self.time
##
##    def __str__(self):
##        t = self.getType()
##        return t
        




##
##class Person(object):
##    def __init__(self, p_id, p_first, p_last):
##        self.id = p_id
##        self.p_first = p_first
##        self.p_last = p_last
##        self._mods = []
##        
##    @property
##    def mods(self):
##        return self._mods
##
##    @modtypes.setter
##    def mods(self, value):
##        self._mods.append(value)
##
##class Update(object):
##    def __init__(self,person,modtype)
##        self.person = person
##        self.modtype = modtype
##
##        
##
##
##class ModType(object):
##    def __init__(self, timestamp):
##        self.timestamp = timestamp
##
##
##class ProfileModType(ModType):
##    pass
##
##
##class ConnectectionModType(ModType):
##    pass
##    


#parse xml doc and create a list of ids and names
ids = []
names = []
xmldoc = minidom.parse('contact_list.xml')
people = xmldoc.getElementsByTagName('person')
for person in people:
    if str(person.childNodes[1].childNodes[0].nodeValue) != ('private'):
        ids.append(str(person.childNodes[1].childNodes[0].nodeValue))
        #print person.childNodes[3].firstChild.nodeValue
        f = str(person.childNodes[3].firstChild.nodeValue.encode("utf-8"))
        l = str(person.childNodes[5].firstChild.nodeValue.encode("utf-8"))
        names.append([f,l])


#use id's to get list of update times, and update types
for i in range(len(ids)):
    #time = []
    #updates = []
    url = "http://api.linkedin.com/v1/people/id=%s/network/updates?scope=self" %ids[i]
    resp,content = client.request(url)
    xmldoc = minidom.parseString(content)
    timelist = xmldoc.getElementsByTagName('timestamp')
    typelist = xmldoc.getElementsByTagName('update-type')
    p = Person(ids[i],names[i][0],names[i][1])
    if len(typelist) > 0:
        for j in range(len(ids)):
            p.addUpdate(typelist[j].firstChild.nodeValue, timelist[j].firstChild.nodeValue)



    
##    if len(typelist) > 0:
##        for j in range(len(typelist)):
##            update = typelist[j].firstChild.nodeValue
##            time = timelist[j].firstChild.nodeValue
##            Updates(ids[i], names[i][0], names[i][1], update, time)
            


##    for t in timelist:
##        time.append(int(t.firstChild.nodeValue))
##
##    for t in typelist:
##        updates.append(str(t.firstChild.nodeValue))
##    
##    if len(typelist) > 0:
##        for j in range(len(typelist)):
##            u = Updates(ids[i],names[i][0],names[i][1],typelist[j],timelist[j])
##            print u

##    print "Name: ", names[i][0]," ",names[i][1]
##    print "Time: ", time
##    print "Updates: ", updates

    

    

    
    
    
    
    




