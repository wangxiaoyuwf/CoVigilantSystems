#!/usr/bin/python3
# Author:Xiaoyu Wang
# data:12/1/2019
# This file is used to analysis the Stars of one RESTAURANT users input from the time line
# The executed command is : python3 AnalysisFromeTimeLine.py -n 'SpinalWorks Chiropractic' -t year (|month|day|hour)


import SampleGetData as sql
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
import getopt


def stars_by_time_show(df, x_index):
    grouped = df.groupby(x_index)['stars'].mean().round(2)
    json_data = grouped.to_json()
    print(json_data)
    # return json_data

    # plt.figure(figsize=(11, 7))
    # sns.pointplot(grouped.index, grouped.values)
    # plt.xlabel(x_index, fontsize=14)
    # plt.ylabel('stars', fontsize=14)
    # title = 'stars by ' + x_index
    # plt.title(title, fontsize=15)
    # plt.tick_params(labelsize=14)
    # for i, v in enumerate(grouped):
    #     plt.text(i, v, str(v), fontweight='bold', fontsize=14)
    # # pause for 3 seconds as you display the histograms
    # plt.pause(3.0)
    # plt.savefig(title)
    # plt.show(block=True)


def starts_by_hour(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['hour'] = df.date.dt.hour
    # print(df.head())
    stars_by_time_show(df, 'hour')


def stars_by_day(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['day'] = df.date.dt.day
    # print(df.head())
    stars_by_time_show(df, 'day')


def stars_by_month(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['month'] = df.date.dt.month
    # print(df.head())
    stars_by_time_show(df, 'month')


def stars_by_year(df):
    df['date'] = pd.to_datetime(df.date, format='%m/%d/%Y %I:%M:%S %p')
    df['year'] = df.date.dt.year
    # print(df.head())
    stars_by_time_show(df, 'year')


# get parameter from the command line and analysis the data that users input
def main(argv):
    business_id = ''
    time = ''
    try:
        opts, args = getopt.getopt(argv, "i:t:", ["id=", "time="])
    except getopt.GetoptError:
        # print('test.py -i <id> -t <time>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-i", "--id"):
            business_id = arg
        elif opt in ("-t", "--time"):
            time = arg
    # print('RESTAURANT : ', id, ' by ', time)

    sql_command = 'select stars, date from review where business_id = "' + business_id + '";'
    # print(sql_command)
    review = sql.query_data_by_sql(sql_command)
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

