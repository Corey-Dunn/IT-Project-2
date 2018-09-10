# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

from sys import argv

# Load in the json file from 'Twitter.py'

try:
    tweets_filename = argv[1]
    tweets_file = open(tweets_filename, "r")

    for line in tweets_file:
        try:
            # Read in one line of the file, convert it into a json object
            tweet = json.loads(line.strip())
            if 'text' in tweet:  # Only messages containing a 'text' field is a tweet
                print("ID: ", tweet['id'])  # The tweet's id
                print("Created at: ", tweet['created_at'])  # When the tweet was posted
                print("Text: ", tweet['text'])  # Content of the tweet
                print("User ID: ", tweet['user']['id'])  # id of the user who posted the tweet
                print("User's Name: ", tweet['user']['name'])  # Name of the user
                print("Account Name: ", tweet['user']['screen_name'])  # Name of the users account

                # Print out the hashtags
                hashtags = []
                for hashtag in tweet['entities']['hashtags']:
                    hashtags.append(hashtag['text'])
                print("Hashtags: ", hashtags)

                print("\n")  # Print a new line

        except Exception:
            # read in a line is not in JSON format (sometimes error occured)
            continue

    tweets_file.close()

except FileNotFoundError:
    print("ERROR: File Not Found")

