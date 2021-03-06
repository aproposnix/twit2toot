"""Main functionality of the twit2toot package."""
import json

from mastodon import Mastodon

import tweepy

from .utils import process_tweet


try:
    with open('secrets.json') as f:
        secrets = json.loads(f.read())
except FileNotFoundError:  # pragma: no cover
    error_msg = 'secrets.json file is missing.'
    raise FileNotFoundError(error_msg)


# Twitter API instance
def get_twitter():
    """Return a Twitter API instance."""
    auth = tweepy.OAuthHandler(
        secrets['twitter']['consumer_key'],
        secrets['twitter']['consumer_secret'],
        )
    auth.set_access_token(
        secrets['twitter']['access_token'],
        secrets['twitter']['access_token_secret'],
        )

    return tweepy.API(auth)


# Mastodon API instance
def get_mastodon():
    """Return a Mastodon API instance."""
    mastodon = Mastodon(
        client_id=secrets['mastodon']['client_key'],
        client_secret=secrets['mastodon']['client_secret'],
        access_token=secrets['mastodon']['access_token'],
        api_base_url=secrets['mastodon']['api_base_url'],
    )

    return mastodon


def toot_latest_tweet():
    """Get the latest tweet from Twitter and toot it to Mastodon."""
    twitter = get_twitter()
    mastodon = get_mastodon()

    tweet = twitter.user_timeline(count=1)[0]
    response = mastodon.toot(tweet.text)

    return response


def crosspost_to_mastodon(tweet, mastodon):
    """Crosspost to Mastodon using a given instance and tweet."""
    toot_dict = process_tweet(tweet)

    response = mastodon.status_post(
        status=toot_dict['status'],
    )

    return response
