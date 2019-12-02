#!/usr/bin/python3
# Author:Xiaoyu Wang
# data:12/1/2019

import SampleGetData as sql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import getopt


def stars_by_time_show(df, x_index):
    grouped = df.groupby(x_index)['stars'].mean().round(2)
    plt.figure(figsize=(11, 7))
    sns.pointplot(grouped.index, grouped.values)
    plt.xlabel(x_index, fontsize=14)
    plt.ylabel('stars', fontsize=14)
    title = 'stars by ' + x_index
    plt.title(title, fontsize=15)
    plt.tick_params(labelsize=14)
    for i, v in enumerate(grouped):
        plt.text(i, v, str(v), fontweight='bold', fontsize=14)
    # pause for 3 seconds as you display the histograms
    plt.pause(3.0)
    plt.savefig(title)
    plt.show(block=True)


def starts_by_hour(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['hour'] = df.date.dt.hour
    print(df.head())
    stars_by_time_show(df, 'hour')


def stars_by_day(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['day'] = df.date.dt.day
    print(df.head())
    stars_by_time_show(df, 'day')


def stars_by_month(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['month'] = df.date.dt.month
    print(df.head())
    stars_by_time_show(df, 'month')

def stars_by_year(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['year'] = df.date.dt.year
    print(df.head())
    stars_by_time_show(df, 'year')


# get parameter from the command line and analysis the data that users input
def main(argv):
    name = ''
    time = ''
    try:
        opts, args = getopt.getopt(argv, "n:t:", ["name=", "time="])
    except getopt.GetoptError:
        print('test.py -n <name> -t <time>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-n", "--name"):
            name = arg
        elif opt in ("-t", "--time"):
            time = arg
    print('RESTAURANT : ', name, ' by ', time)

    sql_command = 'select stars, date from review where business_id = (select business_id from business where name = "' + name + '")'
    review = sql.query_data_by_sql(sql_command)
    print(review.head())
    if time == 'year':
        stars_by_year(review)
    elif time == 'month':
        stars_by_month(review)
    elif time == 'day':
        stars_by_day(review)
    elif time == 'hour':
        starts_by_hour(review)


if __name__ == "__main__":
    main(sys.argv[1:])

    