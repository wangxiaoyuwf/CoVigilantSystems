import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import CoVigilantSystems.SampleGetData as sql
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.svm import LinearSVC


def clean_review(s: str):
    result = s.lower()
    result = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%…&*]+".encode('utf-8').decode('utf-8'),
                    " ".encode('utf-8').decode('utf-8'), result)
    return result


def insert_clean_text_for_review():
    cursor = sql.get_cursor()
    # cursor.execute("alter table review "
    #                "add clean_text varchar(5000)")
    count_result = sql.query_data_by_sql("select count(*) from review").at[0, 'count(*)']
    print(count_result)
    print("-------------Start updating---------------")
    query_index = 1432
    query_limit = 4000
    while count_result > query_index * query_limit:
        query_result = sql.query_data_by_sql(
            "select review_id,text from review limit %d, %d;" % (query_index * query_limit, query_limit))
        # print(query_result)
        for i in query_result.iterrows():
            clean_text = clean_review(i[1]['text'])
            try:
                sql.query_data_by_sql("update review "
                                      "set clean_text= '%s' where review_id = '%s'" % (clean_text, i[1]['review_id']))
            except Exception as e:
                print("-----------Error!!!!!!")
                print("The " + str(i[0] + query_index * query_limit) + "/" + str(
                    count_result) + " line:update review set clean_text= '%s' where review_id = '%s'" % (
                          clean_text, i[1]['review_id']))
        sql.commit_sql()
        query_index += 1
        print("The " + str(i[0] + query_index * query_limit) + "/" + str(
            count_result) + " line")


def main():
    insert_clean_text_for_review()
    0


if __name__ == "__main__":
    main()
