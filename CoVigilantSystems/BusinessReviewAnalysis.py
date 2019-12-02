#!/usr/bin/python3
# Author:Xiaoyu Wang
# data:12/1/2019


import SampleGetData as sql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def merge_business_review(business_df, review_df):
    restaurants_reviews_df = pd.merge(business, review, on='business_id')
    ## update column names
    restaurants_reviews_df.rename(columns={'stars_x': 'avg_star', 'stars_y': 'stars'}, inplace=True)

    ## add column of number of words in review and label of negative and postive reviews
    restaurants_reviews_df['num_words_review'] = restaurants_reviews_df.text.str.replace('\n', ''). \
        str.replace('[!"#$%&\()*+,-./:;<=>?@[\\]^_`{|}~]', '').map(lambda x: len(x.split()))
    # label reviews as positive or negative
    restaurants_reviews_df['labels'] = ''
    restaurants_reviews_df.loc[restaurants_reviews_df.stars >= 4, 'labels'] = 'positive'
    restaurants_reviews_df.loc[restaurants_reviews_df.stars == 3, 'labels'] = 'neural'
    restaurants_reviews_df.loc[restaurants_reviews_df.stars < 3, 'labels'] = 'negative'

    # drop neutral reviews for easy analysis
    restaurants_reviews_df.drop(restaurants_reviews_df[restaurants_reviews_df['labels'] == 'neural'].index, axis=0,
                                inplace=True)
    restaurants_reviews_df.reset_index(drop=True, inplace=True)

    restaurants_reviews_df.head()

    return restaurants_reviews_df


def count_of_restaurants_by_category(business_df):
    plt.figure(figsize=(11, 7))
    grouped = business_df.restaurants_categories.value_counts()
    sns.countplot(y='restaurants_categories', data=business_df, order=grouped.index)
    plt.xlabel('Number of restaurants', fontsize=14, labelpad=10)
    plt.ylabel('Category', fontsize=14)
    plt.title('Count of Restaurants by Category', fontsize=15)
    plt.tick_params(labelsize=14)
    for i, v in enumerate(business_df.restaurants_categories.value_counts()):
        plt.text(v, i + 0.15, str(v), fontweight='bold', fontsize=14)
    # pause for 3 seconds as you display the histograms
    plt.pause(3.0)
    plt.savefig('Count of Restaurants by Category')
    plt.show(block=False)


def percentage_of_positive_reviews(df):
    table = pd.pivot_table(df, values=["review_id"], index=["restaurants_categories"], columns=["labels"],
                           aggfunc=len, margins=True, dropna=True, fill_value=0)
    table_percentage = table.div(table.iloc[:, -1], axis=0).iloc[:-1, -2].sort_values(ascending=False)
    plt.figure(figsize=(11, 8))
    plt.subplot(211)
    sns.pointplot(x=table_percentage.index, y=table_percentage.values)
    plt.xlabel('restaurants_categories', labelpad=7, fontsize=14)
    plt.ylabel('Percentage of positive reviews', fontsize=14)
    plt.title('Percentage of Positive Reviews', fontsize=15)
    plt.tick_params(labelsize=14)
    plt.xticks(rotation=40)
    for i, v in enumerate(table_percentage.round(2)):
        plt.text(i, v * 1.001, str(v), horizontalalignment='center', fontweight='bold', fontsize=14)

    plt.subplot(212)
    grouped = df.groupby('restaurants_categories')['stars'].mean().round(2).sort_values(ascending=False)
    sns.pointplot(grouped.index, grouped.values)
    plt.ylim(3)
    plt.xlabel('restaurants_categories', labelpad=10, fontsize=14)
    plt.ylabel('Average Rating', fontsize=14)
    plt.title('Average Rating of each restaurants_categories', fontsize=15)
    plt.tick_params(labelsize=14)
    plt.xticks(rotation=40)
    for i, v in enumerate(grouped):
        plt.text(i, v, str(v), horizontalalignment='center', fontweight='bold', fontsize=14)

    plt.subplots_adjust(hspace=1)

    # pause for x seconds as you display the histograms
    plt.pause(3.0)
    plt.savefig('Percentage of Positive Reviews')
    plt.show(block=False)


if __name__ == "__main__":
    business = sql.query_data('business', 'is_restaurant', '1')
    review = sql.query_data_by_sql('select * from review')
    print(business.head())
    print(review.head())
    restaurants_reviews = merge_business_review(business, review)
    columns_list = restaurants_reviews.columns.values.tolist()
    print(columns_list)
    print(restaurants_reviews.head())
    print(business.apply(lambda x: sum(x.isnull())))

    # count_of_restaurants_by_category(business)
    percentage_of_positive_reviews(restaurants_reviews)

