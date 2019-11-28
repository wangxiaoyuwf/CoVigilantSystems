#！/bin/bash
echo "Convert Yelp Dataset data from json to sql"
echo "Begin..."
python3 json_to_sql_converter.py ./yelp_dataset/business.json
python3 json_to_sql_converter.py ./yelp_dataset/checkin.json
python3 json_to_sql_converter.py ./yelp_dataset/photo.json
python3 json_to_sql_converter.py ./yelp_dataset/review.json
python3 json_to_sql_converter.py ./yelp_dataset/tip.json
python3 json_to_sql_converter.py ./yelp_dataset/user.json
echo "Done!"