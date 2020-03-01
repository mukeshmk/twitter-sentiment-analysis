import csv, re
import GetOldTweets3 as got
from textblob import TextBlob

def app():
    # input for term to be searched and how many tweets to search
    searchTerm = input("Enter Keyword/Tag to search about: ")
    nooftweets = int(input("Enter how many tweets to search: "))

    # Open/create a file to append data to
    csvFile = open('result.csv', 'a')

    # Use csv writer
    csvWriter = csv.writer(csvFile)

    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(searchTerm)\
                                            .setSince("2019-12-08")\
                                            .setUntil("2020-01-08")\
                                            .setMaxTweets(nooftweets)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria)

    print(tweets[0])
    # for t in tweets:
    #     print(t.text + "\n")


    tweetText = []


    # creating some variables to store info
    polarity = 0
    positive = 0
    wpositive = 0
    spositive = 0
    negative = 0
    wnegative = 0
    snegative = 0
    neutral = 0

    if(tweets.count == 0):
        print('no tweets found!')
    # iterating through tweets fetched
    for tweet in tweets:
        #Append to temp so that we can store in csv later. I use encode UTF-8
        tweetText.append(cleanTweet(tweet.text).encode('utf-8'))
        # print (tweet.text.translate(non_bmp_map))    #print tweet's text
        analysis = TextBlob(tweet.text)
        # print(analysis.sentiment)  # print tweet's polarity
        polarity += analysis.sentiment.polarity  # adding up polarities to find the average later

    if (analysis.sentiment.polarity == 0):  # adding reaction of how people are reacting to find average later
        neutral += 1
    elif (analysis.sentiment.polarity > 0 and analysis.sentiment.polarity <= 0.3):
        wpositive += 1
    elif (analysis.sentiment.polarity > 0.3 and analysis.sentiment.polarity <= 0.6):
        positive += 1
    elif (analysis.sentiment.polarity > 0.6 and analysis.sentiment.polarity <= 1):
        spositive += 1
    elif (analysis.sentiment.polarity > -0.3 and analysis.sentiment.polarity <= 0):
        wnegative += 1
    elif (analysis.sentiment.polarity > -0.6 and analysis.sentiment.polarity <= -0.3):
        negative += 1
    elif (analysis.sentiment.polarity > -1 and analysis.sentiment.polarity <= -0.6):
        snegative += 1


    # Write to csv and close csv file
    csvWriter.writerow(tweetText)
    csvFile.close()

    # finding average of how people are reacting
    positive = percentage(positive, nooftweets)
    wpositive = percentage(wpositive, nooftweets)
    spositive = percentage(spositive, nooftweets)
    negative = percentage(negative, nooftweets)
    wnegative = percentage(wnegative, nooftweets)
    snegative = percentage(snegative, nooftweets)
    neutral = percentage(neutral, nooftweets)

    # finding average reaction
    polarity = polarity / nooftweets

    # printing out data
    print("How people are reacting on " + searchTerm + " by analyzing " + str(nooftweets) + " tweets.")
    print()
    print("General Report: ")

    if (polarity == 0):
        print("Neutral")
    elif (polarity > 0 and polarity <= 0.3):
        print("Weakly Positive")
    elif (polarity > 0.3 and polarity <= 0.6):
        print("Positive")
    elif (polarity > 0.6 and polarity <= 1):
        print("Strongly Positive")
    elif (polarity > -0.3 and polarity <= 0):
        print("Weakly Negative")
    elif (polarity > -0.6 and polarity <= -0.3):
        print("Negative")
    elif (polarity > -1 and polarity <= -0.6):
        print("Strongly Negative")

    print()
    print("Detailed Report: ")
    print(str(positive) + "% people thought it was positive")
    print(str(wpositive) + "% people thought it was weakly positive")
    print(str(spositive) + "% people thought it was strongly positive")
    print(str(negative) + "% people thought it was negative")
    print(str(wnegative) + "% people thought it was weakly negative")
    print(str(snegative) + "% people thought it was strongly negative")
    print(str(neutral) + "% people thought it was neutral")

def cleanTweet(tweet):
    # Remove Links, Special Characters etc from tweet
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) | (\w +:\ / \ / \S +)", " ", tweet).split())

# function to calculate percentage
def percentage(part, whole):
    temp = 100 * float(part) / float(whole)
    return format(temp, '.2f')

if __name__ == "__main__":
    app()