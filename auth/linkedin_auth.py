import string
import random
from .oauth2 import OAuth2

LINKEDIN_URL = 'https://www.linkedin.com/uas/oauth2'
AUTHORIZATION_URL = '/authorization'
TOKEN_URL = '/accessToken'

__all__ = ['LinkedInAuth']


class Token(object):
    def __init__(self, access_token, expires):
        self.access_token = access_token
        self.expires = expires


class LinkedInAuth(OAuth2):
    response_type = 'code'
    grant_type = 'authorization_code'

    def __init__(self,
                client_id, client_secret,
                redirect_uri, site=LINKEDIN_URL,
                authorization_url=AUTHORIZATION_URL, token_url=TOKEN_URL):
        self._state = self.unique_string()

        OAuth2.__init__(self,
                client_id=client_id, client_secret=client_secret,
                site=LINKEDIN_URL, redirect_uri=redirect_uri,
                authorization_url=authorization_url, token_url=token_url)

    @property
    def state(self):
        return self._state

    def unique_string(self, size=20, valid_chars=None):
        if valid_chars is None:
            valid_chars = string.letters + string.digits

        return ''.join(random.choice(valid_chars) for x in range(size))

    def authorize_url(self, scope='', **kwargs):
        state = self.state
        response_type = self.response_type

        return OAuth2.authorize_url(self,
                scope=scope, state=state, response_type=response_type,
                **kwargs)

    def get_token(self, code, **kwargs):
        token = OAuth2.get_token(self,
                code=code, grant_type=self.grant_type,
                **kwargs)
        return Token(token['access_token'], token['expires'])
