# This is a sample how to get data from database and convert data to a dataframe of pandas
import numpy as np
import pymysql
import atexit
import pandas as pd
from sqlalchemy import create_engine

display = pd.options.display
display.max_columns = 50
display.max_rows = 10
display.max_colwidth = 10
display.width = None
display.float_format = lambda x: '%.4f' % x

# Connect the database.
db = pymysql.connect(host='10.22.12.131', user='nonameteam', password='nonameteam', db='nonameteam',
                     cursorclass=pymysql.cursors.DictCursor)
engine = create_engine('mysql+pymysql://nonameteam:nonameteam@10.22.12.131:3306/nonameteam').connect()


# This function is registered, and it will be called when the application complete.
def on_exit():
    # Close database.
    db.close()
    # print('ApplicationExit! Close database.')


# Register the function as one that is called when the application stop.
atexit.register(on_exit)


def insert_dataframe_to_sql(df: pd.DataFrame, table_name):
    df.to_sql(table_name, engine, if_exists='replace')


# Function to query data.Return the pandas.DataFrame. Table name and column can be checked in the database.
def query_data(table_name, column_name, value) -> pd.DataFrame:
    sql_command = 'Select * from ' + table_name + ' where ' + column_name + '=%s'
    cursor = db.cursor()
    cursor.execute(sql_command, value)
    query_result = cursor.fetchall()
    result = pd.DataFrame(list(query_result))
    return result


def query_data_by_sql(sql) -> pd.DataFrame:
    sql_command = sql
    cursor = db.cursor()
    cursor.execute(sql_command)
    query_result = cursor.fetchall()
    result = pd.DataFrame(list(query_result))
    return result


def get_cursor():
    cursor = db.cursor()
    return cursor


def commit_sql():
    db.commit()


# This is main function,and this is called only as main script.That means this part would be executed,
# when this script is called by other script as library.
if __name__ == "__main__":
    result = query_data('business', 'state', 'AZ')
    print(result)
