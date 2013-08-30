import random
import string
import oauth2 as oauth

API_KEY = 'ghxn2rzq9hdi'
API_SECRET = 'TaYCyB20AXb0t5o0'

consumer = oauth.Consumer(API_KEY, API_SECRET)
client = oauth.Client(consumer)

LINKEDIN_URL = 'https://www.linkedin.com/uas/oauth2'
AUTHORIZATION_URL = '/authorization'
TOKEN_URL = '/accessToken'


def unique_string(size=20, valid_chars=None):
    if valid_chars is None:
        valid_chars = string.letters + string.digits

    return ''.join(random.choice(valid_chars) for x in range(size))


STATE = unique_string()
print client.request(LINKEDIN_URL + TOKEN_URL, "GET")
