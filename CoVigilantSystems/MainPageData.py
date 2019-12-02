
import pandas as pd
import matplotlib.pyplot as plt
import CoVigilantSystems.SampleGetData as sql

display = pd.options.display
display.max_columns = 50
display.max_rows = 10
display.max_colwidth = 10
display.width = None

# filter restaurants of US
states = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

restaurant_categories = ['American', 'Mexican', 'Italian', 'Japanese', 'Chinese', 'Thai', 'Mediterranean', 'French',
                             'Vietnamese', 'Greek', 'Indian', 'Korean', 'Hawaiian', 'African', 'Spanish',
                             'Middle_eastern', 'Canadian']

# Add the new column is_restaurant for business to show whether this business is restaurant.
def insert_column_isrestaurant():
    cursor = sql.get_cursor()
    cursor.execute("alter table business "
                   "add is_restaurant int not null ")
    cursor.execute("update business "
                   "set is_restaurant=1 "
                   "where categories like '%Restaurant%'")
    sql.commit_sql()


# Add the new column categories(food type) for restaurant.
def insert_column_restaurants_categories():
    cursor = sql.get_cursor()
    cursor.execute("alter table business "
                   "add restaurants_categories varchar(20)")
    for c in restaurant_categories:
        cursor.execute("update business "
                       "set restaurants_categories='" + c + "' where categories like '%" + c + "%'")
    sql.commit_sql()


def show_count_of_restaurants_by_category():
    result = sql.query_data_by_sql(sql="select * from business where restaurants_categories = '"+restaurant_categories[0]+"'")
    print(result)
    0


def main():
    # insert_column_isrestaurant()
    # insert_column_restaurants_categories()
    # print(sql.query_data_by_sql("select * from business where restaurants_categories='Canadian'"))
    show_count_of_restaurants_by_category()
    0


if __name__ == "__main__":
    main()
