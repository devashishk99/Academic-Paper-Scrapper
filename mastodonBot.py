from mastodon import Mastodon

ACCESS_TOKEN = '' # register your app on Mastodon and add its access token here

class MastodonBot():
    """
    The Mastodon Class connects to the user account
    based on the access token and toots a status
    """
    def __init__(self):
        self.api = self.connect_to_mastodon_OAuth() # calls the function on instantiation

    # returns object having access to Mastodon account
    def connect_to_mastodon_OAuth(self):
        if not ACCESS_TOKEN:
            return 0
        mastodon = Mastodon(
            access_token = ACCESS_TOKEN,
            api_base_url = 'https://mastodon.social/'
        )
        return mastodon

    # toots a status along with ability to reply to certain toot
    def toot(self, msg, id=None):
        self.api.status_post(status = msg, in_reply_to_id=id)