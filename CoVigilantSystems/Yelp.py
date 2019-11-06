# coding=utf-8

import pandas as pd
import numpy as np
import sys
import importlib

# Deal with coding problems. - UnicodeDecodeError: 'utf8' codec can't decode byte 0xc3 in position 18: unexpected end of data
importlib.reload(sys)

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import matplotlib.pyplot as plt


import nltk
# download stopwords at first time.
# nltk.download('stopwords')
from nltk.corpus import stopwords
from fasttext import train_supervised
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import wordnet
import enchant

# Yelp review file has been processed into CSV format using https://github.com/Yelp/dataset-examples
yelp_file = "~/Desktop/yelp_dataset/review.csv"

# The max feature of bag_of_words model.
max_features = 5000

def words_to_vec(text):
    #build up bag of words, delete english stopwords
    # vectorizer = CountVectorizer(ngram_range=(2, 2), max_features=max_features,stop_words='english',lowercase=True) # 2-gram
    vectorizer = CountVectorizer(ngram_range=(1, 1), max_features=max_features, stop_words='english', lowercase=True)

    print("vectorize parameter:")
    print(vectorizer)
    #This object is going to count the tf-idf weight of each word.
    transformer = TfidfTransformer()
    # Process with 2-gram and TFIDF
    # x = transformer.fit_transform(vectorizer.fit_transform(text))
    x = vectorizer.fit_transform(text)
    return x

def load_reviews(filename, nrows):
    # Content of CSV's head：
    # funny,user_id,review_id,text,business_id,stars,date,useful,cool
    text = []
    stars = []

    ###
    # The first 10,000 lines are read during the development phase. It is very important to use the encoding='utf-8' parameter.
    df = pd.read_csv(filename, sep=',', header=0, encoding='utf-8', nrows=nrows)
    print(df.head())

    # Get data directly by column name. Convert list to list object
    text = list(df['text'])
    stars = list(df['stars'])

    # Show the number of individual ratings
    print(df.describe())

    # Draw figure
    plt.figure()
    count_classes = pd.value_counts(df['stars'], sort=True)

    print("stars counts:")
    print(count_classes)
    count_classes.plot(kind='bar', rot=0)
    plt.xlabel('stars')
    plt.ylabel('stars counts')
    plt.show()

    return text, stars


def dump_file(x, y, filename):
    with open(filename, 'w') as f:
        for i, v in enumerate(x):
            line = "%s __label__%d\n" % (v, y[i])
            f.write(line)
        f.close()


def clean_text(text):
    text_cleaned = []

    list_stopWords = list(set(stopwords.words('english')))
    english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%']
    d = enchant.Dict("en_US")

    for line in text:
        list_words = word_tokenize(line.lower())
        # Clean punctuation
        list_words = [word for word in list_words if word not in english_punctuations]
        # wordnet_Delete very common English words
        # list_words = [word for word in list_words if wordnet.synsets(word) ]
        list_words = [word for word in list_words if d.check(word)]
        # Clean stop words
        filtered_words = [w for w in list_words if not w in list_stopWords]
        text_cleaned.append(" ".join(filtered_words))
    return text_cleaned

def do_fasttext(text, stars):
    text_cleaned = clean_text(text)

    # Split training set and test set test set 20%
    # x_train, x_test, y_train, y_test = train_test_split(text, stars, test_size=0.2)
    x_train, x_test, y_train, y_test = train_test_split(text_cleaned, stars, test_size=0.2)

    # Generate training data and test data according to fasttest requirements
    dump_file(x_train, y_train, "yelp_train.txt")
    dump_file(x_test, y_test, "yelp_test.txt")

    model = train_supervised(
        input="yelp_train.txt", epoch=20, lr=0.6, wordNgrams=2, verbose=2, minCount=1
    )

    def print_results(N, p, r):
        print("N\t" + str(N))
        print("P@{}\t{:.3f}".format(1, p))
        print("R@{}\t{:.3f}".format(1, r))

    print_results(*model.test("yelp_test.txt"))


if __name__ == '__main__':
    text, stars = load_reviews(yelp_file, 100000)

    stars = [0 if star < 3 else 1 for star in stars]

    print("sentiment counts:")
    count_classes = pd.value_counts(stars, sort=True)
    print(count_classes)
    count_classes.plot(kind='bar', rot=0)
    plt.xlabel('sentiment ')
    plt.ylabel('sentiment  counts')
    plt.show()

    # Classify documents with "fasttext"
    do_fasttext(text, stars)
