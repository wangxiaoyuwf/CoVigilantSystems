#!/usr/bin/python3
# Author:Xiaoyu Wang
# This file is used to convert the .json data to .sql data
# data:11/12/2019

import json
import codecs
import argparse
import os


# read json file and write the context to the sql file
def read_and_write_file(json_file_path, sql_file_path):
    json_f = open(json_file_path,"r",encoding='utf-8')
    sql_f = open(sql_file_path,"a",encoding='utf-8')
    (sqlfilepath, tempfilename) = os.path.split(sql_file_path)
    (sql_table_name, extension) = os.path.splitext(tempfilename)
    print("table name:", sql_table_name)
    for line in json_f:
        json2sql(sql_f, sql_table_name,line)


def json2sql(sql_f, table_name,json_str):
    result_jstr = json.loads(json_str)
    # table name is same as json file name
    sql = 'insert into ' + table_name + '('
    key_jstr = ''
    value_jstr = '"'
    for j in result_jstr.keys():
        key_jstr = key_jstr+j+','
    for i in result_jstr.values():
        value_jstr = value_jstr+str(i)+'","'
    # print(sql+key_jstr[:-1]+') values('+value_jstr[:-2]+');')
    sql_f.write(sql+key_jstr[:-1]+') values('+value_jstr[:-2]+');\n')


# python json_to_sql_converter.py jsonfilename, then it will create a sql file
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Convert Yelp Dataset data from json to sql'
    )
    parser.add_argument(
            'json_file',
            type=str,
            help='The json file to convert.',
    )
    args = parser.parse_args()
    json_file = args.json_file
    sql_file = '{0}.sql'.format(json_file.split('.json')[0])
    read_and_write_file(json_file, sql_file)