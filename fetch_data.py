import os, re
import GetOldTweets3 as got
import pandas as pd

dataset_foler = "datasets"
file_name = ""
file_ext = ".csv"

start_date = "2020-02-06"
end_date = "2020-02-08"
language = "en"
emoji = "unicode"
maxtweets = 100000

# creating new DF everytime this program is run
# to avoid repeat of data if the df is being appended
df = pd.DataFrame(columns=['date', 'username', 'to', 'replies', 'retweets' , 'text', 'mentions', 'hashtags', 'permalink'])

def receiveBuffer(tweets):
    global df
    for t in tweets:
        data = pd.Series([
            t.date.strftime("%Y-%m-%d %H:%M:%S"),
            t.username,
            t.to,
            t.replies,
            t.retweets,
            t.text,
            t.mentions,
            t.hashtags,
            t.permalink], index=df.columns)
        df = df.append(data, ignore_index=True)

query = input("Enter Search Query: ")
try:
    tweetCriteria = got.manager.TweetCriteria().setQuerySearch(query)\
                                                .setSince(start_date)\
                                                .setUntil(end_date)\
                                                .setMaxTweets(maxtweets)\
                                                .setLang(language)\
                                                .setEmoji(emoji)
    tweets = got.manager.TweetManager.getTweets(tweetCriteria, receiveBuffer)
except Exception as err:
    pass

# creating the dataset directory if it doesn't exist
if not os.path.exists(dataset_foler):
        os.makedirs(dataset_foler)

# creating file name based on the query
file_name = re.sub("[@#]","", query) + '_' + start_date + '_to_' + end_date + '_' + str(df.size)

# to avoid duplicate file names in folder
path = dataset_foler + '/%s%s' % (file_name, file_ext)
uniq = 1
while os.path.exists(path):
  path = dataset_foler + '/%s_%d%s' % (file_name, uniq, file_ext)
  uniq += 1

df.to_csv(path, index=False)
