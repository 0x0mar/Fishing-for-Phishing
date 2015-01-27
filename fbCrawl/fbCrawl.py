from facepy.utils import get_extended_access_token
from facepy import GraphAPI
import sys

app_id = '763373250416428'
app_secret = '1ac36a48bdce4e6425a0962e44c7aec6'
short_lived_access_token = "CAAK2SK9sDywBAGaZC5HJAtIdryNqoZAWLTFmYEen9Qjgpo5bCZAg3vEZBROp9rSisWOPCt9kJYJyyqFINOZA6qigoND6TpegProYBChsZAk9dPNNV6SWwHHz0sq0Oaaez29z3Wj7G302ErZBLiiLcvNgkrYwRlP7Sc3l19G4HZCz07PGtDUJk1623HKdB64YX4coOLDZBeebfcJ4xbtD2e1oQ"

long_lived_access_token, expires_at = get_extended_access_token(
    short_lived_access_token,
    app_id, app_secret)

def user_id_to_username(userid):

    if userid is not None:

        userid = '/{0}'.format(userid)
        try:
            return  graph.get(userid)['name']

        except (exceptions.FacebookError, exceptions.OAuthError) as e:
            print e.message + "1"
            sys.exit(0)
graph = GraphAPI(long_lived_access_token)
print graph.get('/me')
print graph.get('/me/inbox')
