# read yelp data and insert them to Mysql
# Please don't run this script until you totally understand it.
import json
import pymysql

review_file = "/Users/jianfenglv/Desktop/yelp_dataset/review.json"
review_table_name = "review"
review_create_sql = """CREATE TABLE review (
       review_id VARCHAR(100) NOT NULL PRIMARY KEY,
       user_id VARCHAR(100),
       business_id VARCHAR(200),
       stars INT,
       date DATETIME,
       text VARCHAR(10000) NOT NULL,
       useful INT,
       funny INT,
       cool INT,
       INDEX (review_id))"""
review_columns_list = ['review_id', 'user_id', 'business_id', 'stars', 'date', 'text', 'useful', 'funny', 'cool']

business_file = "/Users/jianfenglv/Desktop/yelp_dataset/business.json"
business_table_name = "business"
business_create_sql = """CREATE TABLE business (
        business_id VARCHAR(100) NOT NULL PRIMARY KEY,
        name VARCHAR(200),
        address VARCHAR(200),
        city VARCHAR(100),
        state VARCHAR(50),
        postal_code VARCHAR(50),
        latitude DOUBLE,
        longitude DOUBLE,
        stars FLOAT,
        review_count INT,
        is_open INT,
        attributes VARCHAR(10000),
        categories VARCHAR(1000),
        hours VARCHAR(500),
        INDEX (business_id))"""
business_columns_list = ['business_id', 'name', 'address', 'city', 'state', 'postal_code', 'latitude', 'longitude',
                         'stars', 'review_count', 'is_open', 'attributes', 'categories', 'hours']


# Create table.
def create_table(db, table_name, sql):
    cursor = db.cursor()
    cursor.execute("SELECT VERSION()")
    data = cursor.fetchone()
    print("Database version : %s " % data)  # Result will show that connecting the database is successful.
    cursor.execute("DROP TABLE IF EXISTS " + table_name)  # drop old review
    cursor.execute(sql)


# insert data.
def data_insert(db, file, table_name, columns_list):
    column = ''
    argument = ''
    for c in columns_list:
        column += c + ','
        argument += '%s,'
    column = column[:-1]
    argument = argument[:-1]
    insert_re = "insert into " + table_name + "(" + column + ") values (" + argument + ")"
    result = []
    cursor = db.cursor()
    i = 0
    with open(file, encoding='utf-8') as f:
        while True:
            print(u'loading %sth line......' % i)
            try:
                result.clear()
                for index in range(10000):
                    i += 1
                    lines = f.readline()  # Read file line by line
                    review_text = json.loads(lines)  # run every line data
                    temp = []
                    for c in columns_list:
                        if c == 'date':
                            print(review_text[c])
                        temp.append(json.dumps(review_text[c]) if type(review_text[c])==dict else review_text[c])
                    result.append(tuple(temp))
                # print(insert_re)
                # print(result)
                cursor.executemany(insert_re, result)
                db.commit()
            except Exception as e:
                print(u'loading the %sth , the last one line......' % i)
                print(result)
                cursor.executemany(insert_re, result)
                print(result)
                db.commit()
                db.rollback()
                print(str(e))
                break


if __name__ == "__main__":
    db = pymysql.connect(host='192.168.64.2', user='yelp', password='yelp', db='yelp_data')
    # db = pymysql.connect(host='10.22.12.131', user='nonameteam', password='nonameteam', db='nonameteam')
    db.cursor()
    create_table(db, table_name=review_table_name, sql=review_create_sql)
    data_insert(db, file=review_file, table_name=review_table_name, columns_list=review_columns_list)
    # create_table(db, table_name=business_table_name, sql=business_create_sql)
    # data_insert(db, file=business_file, table_name=business_table_name, columns_list=business_columns_list)
    db.cursor().close()
