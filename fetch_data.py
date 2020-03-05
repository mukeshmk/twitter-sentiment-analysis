#https://pypi.org/project/GetOldTweets3/
#https://github.com/Mottl/GetOldTweets3#egg=GetOldTweets3


import GetOldTweets3 as got
import pandas as pd

start_date = "2019-11-08"
end_date = "2020-02-08"
language = "en"
emoji = "unicode"
maxtweets = 5

df = pd.DataFrame(columns=['count', 'date', 'username', 'to', 'replies', 'retweets' , 'text', 'mentions', 'hashtags', 'permalink'])
df.set_index('count',inplace = True)

def receiveBuffer(tweets):
    global df
    for t in tweets:
        data = [t.date.strftime("%Y-%m-%d %H:%M:%S"),
            t.username,
            t.to,
            t.replies,
            t.retweets,
            t.text,
            t.mentions,
            t.hashtags,
            t.permalink]
        df.loc[0 if pd.isnull(df.index.max()) else df.index.max() + 1] = data

tweetCriteria = got.manager.TweetCriteria().setQuerySearch("elections")\
                                            .setSince(start_date)\
                                            .setUntil(end_date)\
                                            .setMaxTweets(maxtweets)\
                                            .setLang(language)\
                                            .setEmoji(emoji)
tweets = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)

df.to_csv('test.csv')
