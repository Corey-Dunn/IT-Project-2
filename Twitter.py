try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError, TwitterStream

# Import 'argv' in order to take keywords from the command line
from sys import argv

ACCESS_TOKEN = '1036757136150163456-Hkk9KC1HqyYeH7uJSniDNngdRNgKN1'  # Access Token
ACCESS_SECRET = '8p9QTSRpEb1A2UxXI91PGiIaLF9wzZuO0mL2zqP5GQSaC'  # Access Secret
CONSUMER_KEY = 'Dw0re9TrtgYtc8OOQeetOnlxJ'  # API Key
CONSUMER_SECRET = '3E8FCgp98AqYdMMu0U75o6wyNieaS06KQfmXdZC0ZArxrlfl9m'  # API Secret

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate a connection with the twitter streaming API
twitter_stream = TwitterStream(auth=oauth)

# Get a sample of the public data following through Twitter
iterator = twitter_stream.statuses.filter(track=str(argv[1]), language="en")

tweet_count = 100  # Number of tweets to display

# Print each tweet in the stream to the screen
for tweet in iterator:
    tweet_count -= 1
    # Twitter Python Tool wraps the data returned by Twitter
    # as a TwitterDictResponse object.
    # We convert it back to the JSON format to print/score
    print(json.dumps(tweet))

    # Break out of the loop once the count reaches 0
    if tweet_count <= 0:
        break






