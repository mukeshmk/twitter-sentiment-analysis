# code for NLTK from
# https://www.digitalocean.com/community/tutorials/how-to-perform-sentiment-analysis-in-python-3-using-the-natural-language-toolkit-nltk

import os
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import twitter_samples, stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
import GetOldTweets3 as got
import pandas as pd
import emoji

import re, string, random

def remove_noise(tweet_tokens, stop_words = ()):

    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens):
        # regex to remove hyperlinks
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|'\
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+','', token)

        # regex to removes the @twitter_handle (mentions)
        token = re.sub("(@[A-Za-z0-9_]+)","", token)

        token = emoji.demojize(token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        # stemming / lemmstization - normalization
        # grouping together the inflected forms of a word so they can be analysed as a single item
        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        # removes punctuations and stop words
        if (len(token) > 0) and (token not in string.punctuation) and (token.lower() not in stop_words):
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def get_all_words(cleaned_tokens_list):
    for tokens in cleaned_tokens_list:
        for token in tokens:
            yield token

def get_tweets_for_model(cleaned_tokens_list):
    for tweet_tokens in cleaned_tokens_list:
        yield dict([token, True] for token in tweet_tokens)

if __name__ == "__main__":

    stop_words = stopwords.words('english')

    positive_tweet_tokens = twitter_samples.tokenized('positive_tweets.json')
    negative_tweet_tokens = twitter_samples.tokenized('negative_tweets.json')

    positive_cleaned_tokens_list = []
    negative_cleaned_tokens_list = []

    for tokens in positive_tweet_tokens:
        positive_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    for tokens in negative_tweet_tokens:
        negative_cleaned_tokens_list.append(remove_noise(tokens, stop_words))

    all_pos_words = get_all_words(positive_cleaned_tokens_list)

    freq_dist_pos = FreqDist(all_pos_words)
    # print(freq_dist_pos.most_common(10))

    positive_tokens_for_model = get_tweets_for_model(positive_cleaned_tokens_list)
    negative_tokens_for_model = get_tweets_for_model(negative_cleaned_tokens_list)

    positive_dataset = [(tweet_dict, "Positive")
                         for tweet_dict in positive_tokens_for_model]

    negative_dataset = [(tweet_dict, "Negative")
                         for tweet_dict in negative_tokens_for_model]

    dataset = positive_dataset + negative_dataset

    random.shuffle(dataset)

    train_data = dataset[:7000]
    test_data = dataset[7000:]

    print('Training the Classifier!')
    classifier = NaiveBayesClassifier.train(train_data)
    print("Accuracy is of Trained Classifier is:", classify.accuracy(classifier, test_data))

    # print(classifier.show_most_informative_features(10))

    print('Begin Classifying the Data!')

    data_dir = os.path.dirname(os.path.realpath(__file__)) + "\datasets"

    filelist = []
    for (dirpath, dirnames, filenames) in os.walk(data_dir):
        for f in filenames:
            filepath = dirpath + '\\' +f
            filelist.append(filepath)

    total_pos_count = {}
    total_neg_count = {}
    for f in filelist:
        df = pd.read_csv(f)

        print('\nClassifying the Data for ' + f)

        pos_count = 0
        neg_count = 0
        for index, row in df.iterrows():
            tokenised_tweet = remove_noise(word_tokenize(row['text']))
            if(classifier.classify(dict([token, True] for token in tokenised_tweet)) == 'Positive'):
                pos_count += 1
            else:
                neg_count += 1

        total_pos_count[f] = pos_count
        total_neg_count[f] = neg_count

        print('Positive Count ' + str(pos_count))
        print('Negative Count ' + str(neg_count))

    with open('pos_count.txt', 'w') as f1:
        for key1, value1 in total_pos_count.items():
            f1.write("%s - %s\n" % (key1, value1))

    with open('neg_count.txt', 'w') as f2:
        for key2, value2 in total_neg_count.items():
            f2.write("%s - %s\n" % (key2, value2))
