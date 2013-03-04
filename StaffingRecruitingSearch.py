# peopl-investment Account
##API_KEY = 'ghxn2rzq9hdi'
##API_SECRET = 'TaYCyB20AXb0t5o0'
##OAUTH_TOKEN = '908ac8c2-1574-4033-bbf3-d409dfe8baf0'
##OAUTH_TOKEN_SECRET = '5f15124b-13f6-4f7f-a372-5ce475435013'
##
#praful account
API_KEY = 'onwzvln0ksj5'
API_SECRET = 'oTmzJwbB9AFSHagM'
OAUTH_TOKEN = '420be95e-de13-4002-9023-42835b337245'
OAUTH_TOKEN_SECRET = 'f25efa3c-4d09-40e2-9045-171029899821'

##from linkedin import LinkedinAPI
##from pprint import pprint as pp
##import sys
##
##l = LinkedinAPI(api_key = API_KEY,
##              api_secret = API_SECRET,
##              oauth_token= OAUTH_TOKEN,
##              oauth_token_secret=OAUTH_TOKEN_SECRET,)
##
##
## Get search results
##
##try:
##    companies_search = l.get('company-search', params={'industry' : 104, 'facet': {"location":"us:84" }})
##    #print type(companies_search)
##    print companies_search
##
##except:
##    print "Fail"

import oauth2 as oauth
import httplib2
import time, os, simplejson
import urlparse
from xml.dom import minidom


#praf ID:  qxblPhxkQB 7rrjuyG_RY
#rishi ID: d3Fe0u8WpP, E5SBg8_W2j
#endpoint URL
#url = "http://api.linkedin.com/v1/people/~?count=10"
#url = "http://api.linkedin.com/v1/people/~/connections?count=10"
#url = "http://api.linkedin.com/v1/companies/1337:(id,website-url)"
#url = "http://api.linkedin.com/v1/company-search:(facets)?keywords={'industry' : 104}&facets=location"
#url = "http://api.linkedin.com/v1/company-search?keywords=google&facet=location%2Cus%3A84&count=10&sort=relevance"
#url = "http://api.linkedin.com/v1/people/~:(first-name,last-name,headline,location,industry,summary,positions)"
#url = "http://api.linkedin.com/v1/people/url={www.linkedin.com/in/prafulmathur}:(id,first-name,last-name,skills,picture-url,headline,location:(name),industry,num-connections,num-connections-capped,proposal-comments,positions:(title,start-date,end-date,is-current,company:(id,name,size)),languages,num-recommenders,public-profile-url)"
#url = "http://api.linkedin.com/v1/people/~/connections:(id,first-name,last-name)"
#url = "http://api.linkedin.com/v1/people/~:(first-name,last-name,skills)"
#url = "https://api.linkedin.com/v1/people/id=7rrjuyG_RY:(id,first-name,last-name,skills)" #picture-url,headline,location:(name),industry,num-connections,num-connections-capped,proposal-comments,positions:(title,start-date,end-date,is-current,company:(id,name,size)),languages,num-recommenders,public-profile-url)"
#url = "http://api.linkedin.com/v1/people-search?first-name=Rishi&last-name=Mathur&school-name=Rutgers:(people:(id,first-name,last-name,headline),num-results)"#:(id,first-name,last-name)"
#url = "https://api.linkedin.com/v1/people/url=http%3A%2F%2Fwww.linkedin.com%2Fpub%2Frishi-mathur%2F13%2F677%2F381:(first-name,last-name,skills)"
#url = "http://api.linkedin.com/v1/people/~/connections:(first-name,last-name,skills)"
url = "http://api.linkedin.com/v1/people/~/network/updates?scope=self"

# Fill the keys and secrets you retrieved after registering your app
consumer_key      =   API_KEY
consumer_secret  =   API_SECRET
user_token           =   OAUTH_TOKEN
user_secret          =   OAUTH_TOKEN_SECRET
 
# Use your API key and secret to instantiate consumer object
consumer = oauth.Consumer(consumer_key, consumer_secret)
 
# Use your developer token and secret to instantiate access token object
access_token = oauth.Token(
            key=user_token,
            secret=user_secret)
 
client = oauth.Client(consumer, access_token)
 
# Make call to LinkedIn to retrieve your own profile
resp,content = client.request(url)
#print resp
#print type(content)
#print client
#print content
#print resp
#response,c = client.request("http://api.linkedin.com/v1/people/~/connections?count=10", "GET", "")
#print response
#request_token = dict(urlparse.parse_qsl(content))
#print request_token
f = open('update.xml','w')
f.write(content)
f.close()



