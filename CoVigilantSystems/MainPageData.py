import numpy as np
import pandas as pd
import seaborn as sns
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
    count_categories = []
    for c in restaurant_categories:
        count_categories.append(
            sql.query_data_by_sql(sql="select count(*) from business where restaurants_categories = '" + c + "'").at[
                0, 'count(*)'])
    dict_categories = dict(zip(restaurant_categories, count_categories))
    df_categories = pd.DataFrame(sorted(dict_categories.items(), key=lambda item: item[1], reverse=False),
                                 columns=['categories', 'count'])
    print(df_categories)
    plt.barh(np.arange(len(df_categories['categories'])), df_categories['count'], align='center', alpha=0.4)
    plt.yticks(np.arange(len(df_categories['categories'])), df_categories['categories'])
    for a, b in zip(df_categories['count'], np.arange(len(df_categories['categories']))):
        plt.text(a, b, '%d' % a, ha='left', va='center', fontsize=11, color="blue")
    plt.xlabel('Number of restaurants')
    plt.title('Count of Restaurants by Category', fontsize=15)
    plt.show()
    0


def show_count_of_restaurants_by_city():
    count_city = sql.query_data_by_sql(
        sql="select city,count(*) as count from business where state in "
            + str(states).replace('[', '(').replace(']', ')')
            + " group by city")
    top_10_count_city = count_city.sort_values(by='count', ascending=False)[:10]
    print(top_10_count_city)
    plt.figure(figsize=(11, 6))
    sns.barplot(x=np.arange(len(top_10_count_city['city'])), y=top_10_count_city['count'],
                palette=sns.color_palette("BuGn_r", len(top_10_count_city['city'])))
    plt.xlabel('City', labelpad=10, fontsize=14)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(np.arange(len(top_10_count_city['city'])), top_10_count_city['city'])
    plt.title('Count of Restaurants by City (Top 10)', fontsize=15)
    plt.tick_params(labelsize=14)
    plt.xticks(rotation=15)
    for a, b in zip(np.arange(len(top_10_count_city['city'])), top_10_count_city['count']):
        plt.text(a, b * 1.02, str(b), horizontalalignment='center', fontweight='bold', fontsize=14)
    plt.show()
    0


def main():
    # # ------------only run one time-----------------
    # insert_column_isrestaurant()
    # insert_column_restaurants_categories()
    # print(sql.query_data_by_sql("select * from business where restaurants_categories='Canadian'"))
    # # ------------only run one time-----------------

    # show_count_of_restaurants_by_category()
    show_count_of_restaurants_by_city()
    0


if __name__ == "__main__":
    main()
