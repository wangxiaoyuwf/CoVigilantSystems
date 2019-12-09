#!/usr/bin/python3
# Author:Xiaoyu Wang
# data:12/8/2019
# This file is used to analysis the key words for positive and negative and get the polarity of them
# Then return the json data to the front side
# # The executed command is : python3 KeywordsAnalysis.py -n 'SpinalWorks Chiropractic'

import csv
import sys
import SampleGetData as sql
import pandas as pd
import getopt
import re
import matplotlib.pyplot as plt
import seaborn as sns
import json
from nltk.corpus import stopwords
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC
pd.set_option('display.float_format', lambda x: '%.4f' % x)


# convert reviews to words
def ReviewsToWords(reviews, positive_words, negative_words):
    stop_words = set(stopwords.words("english"))
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    unuseful_positive_words = ['great','amazing','love','best','awesome','excellent','good',
                                                   'favorite','loved','perfect','gem','perfectly','wonderful',
                                                    'happy','enjoyed','nice','well','super','like','better','decent','fine',
                                                    'pretty','enough','excited','impressed','ready','fantastic','glad','right',
                                                    'fabulous']
    unuseful_negative_words =  ['bad','disappointed','unfortunately','disappointing','horrible',
                                                    'lacking','terrible','sorry']
    unuseful_words = unuseful_positive_words + unuseful_negative_words
    Words = []
    for i in range(len(reviews)):
        review = reviews[i]
        words = re.sub("[^a-zA-Z]", " ", review).lower().split()
        words = [word for word in words if word in positive_words + negative_words]
        words = [word for word in words if word not in stop_words]
        words = [word for word in words if word not in english_punctuations]
        words = [word for word in words if word not in unuseful_words]
        words = ' '.join(words)
        Words.append(words)
    return Words


# label the key word with positive, neural and negative
# and then get the keywords and polarity
def get_labeled_data_set(df):
    # label positive and negative by stars
    df['labels'] = ''
    df.loc[df.stars >= 4, 'labels'] = 'positive'
    df.loc[df.stars == 3, 'labels'] = 'neural'
    df.loc[df.stars < 3, 'labels'] = 'negative'
    # remove the neutral reviews
    df.drop(df[df['labels'] == 'neural'].index, axis=0, inplace=True)
    df.reset_index(drop=True, inplace=True)
    # load positive and negative words
    file_positive = open('positive.txt', encoding='ISO-8859-1')
    reader = csv.reader(file_positive)
    positive_words = [word[0] for word in reader]
    file_negative = open('negative.txt', encoding='ISO-8859-1')
    reader = csv.reader(file_negative)
    negative_words = [word[0] for word in reader]

    # filter the data_set
    df = df[['text', 'labels']]
    df.reset_index(drop=True, inplace=True)

    # train data and test data
    train_data, test_data = train_test_split(df[['text', 'labels']], test_size=0.2)
    terms_train = ReviewsToWords(list(train_data['text']), positive_words, negative_words)
    class_train = list(train_data['labels'])
    terms_test = ReviewsToWords(list(test_data['text']), positive_words, negative_words)
    class_test = list(test_data['labels'])

    vectorizer = CountVectorizer()
    feature_train_counts = vectorizer.fit_transform(terms_train)
    feature_train_counts.shape
    svm = LinearSVC()
    svm.fit(feature_train_counts, class_train)
    score_coef = svm.coef_[0]
    words_score = pd.DataFrame({'score': score_coef, 'word': vectorizer.get_feature_names()})
    reviews = pd.DataFrame(feature_train_counts.toarray(), columns=vectorizer.get_feature_names())
    reviews['labels'] = class_train
    frequency = reviews[reviews['labels'] == 'positive'].sum()[:-1]
    words_score.set_index('word', inplace=True)
    polarity_score = words_score
    polarity_score['frequency'] = frequency
    polarity_score['polarity'] = polarity_score.score * polarity_score.frequency / \
                                        reviews.shape[0]
    polarity_score.polarity = polarity_score.polarity.astype(float)
    polarity_score.frequency = polarity_score.frequency.astype(float)
    # polarity_score[polarity_score.polarity>0].sort_values('polarity', ascending=False)[:20]
    polarity_score.drop(['score', 'frequency'], axis=1, inplace=True)
    dict_positive = (polarity_score[polarity_score.polarity>0].sort_values('polarity', ascending=False)[:30]).groupby('word')['polarity'].apply(lambda x:x).to_dict()
    dict_negative = (polarity_score[polarity_score.polarity<0].sort_values('polarity', ascending=False)[:30]).groupby('word')['polarity'].apply(lambda x:x).to_dict()
    # print(polarity_score[polarity_score.polarity>0].sort_values('polarity', ascending=False)[:20])
    # print(polarity_score[polarity_score.polarity<0].sort_values('polarity', ascending=True)[:20])
    dict_key_words = {'positive': dict_positive, 'negative': dict_negative}
    json_key_words = json.dumps(dict_key_words)
    print(json_key_words)


# get parameter from the command line and analysis the data that users input
def main(argv):
    business_id = ''
    try:
        opts, args = getopt.getopt(argv, "i:", ["id="])
    except getopt.GetoptError:
        print('KeywordsAnalysis.py -i <id>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--id"):
            business_id = arg
    print('RESTAURANT ID : ', business_id)

    sql_command = 'select stars, text from review where business_id = "' + business_id + '";'
    print(sql_command)
    review = sql.query_data_by_sql(sql_command)
    get_labeled_data_set(review)


if __name__ == "__main__":
    main(sys.argv[1:])

    