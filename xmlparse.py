#parse through xml from API
import xml
import datetime

def convert_time(t):
    t = int(t)
    t = t/1000.
    return datetime.datetime.fromtimestamp(t).strftime("%a %b-%d-%Y %I:%m %p") #return string
    
##from xml.dom.minidom import parseString
##
##file = open("update.xml",'r')
##data = file.read()
##file.close()
##dom = parseString(data)
##xmlTag = dom.getElementsByTagName('updated-fields')[0].toxml()
##xmlData = xmlTag.replace('<updated-fields>','').replace('</updated-fields>','')
##
##print xmlTag
##print xmlData

from xml.dom import minidom
xmldoc = minidom.parse('update1.xml')
timelist = xmldoc.getElementsByTagName('timestamp')
keylist = xmldoc.getElementsByTagName('update-type')
update_typelist = xmldoc.getElementsByTagName('updated-fields')
print len(timelist)
for s in timelist:
    print s.nodeName
    t = s.firstChild.nodeValue
    print convert_time(t)

for s in keylist:
    print s.nodeName
    print s.firstChild.nodeValue
    
print "number of updated fields: ", len(update_typelist)
for s in update_typelist:
    print "-------------------"
    #print s.nodeName
    print s.childNodes[1].childNodes[1].firstChild.nodeValue
    #child_one = s.firstChild.firstChild
    #print child_one
    #print dir(child_one)
    #child_two = child_one.firstChild
   

##import xml.etree.ElementTree as etree
##
##tree = etree.parse('update.xml')
##print 'tree.findall - timestamp', tree.findall('/timestamp')
##root = tree.getroot()
##print 'root.findall - timestamp', root.findall('/timestamp')
##
##print 'root[3] - ', root[3]
