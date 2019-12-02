# This is a sample how to get data from database and convert data to a dataframe of pandas
import pymysql
import atexit
import pandas as pd

# Connect the database.
db = pymysql.connect(host='10.22.12.131', user='nonameteam', password='nonameteam', db='nonameteam')


# This function is registered, and it will be called when the application complete.
def on_exit():
    # Close database.
    db.close()
    print('ApplicationExit! Close database.')


# Register the function as one that is called when the application stop.
atexit.register(on_exit)


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
