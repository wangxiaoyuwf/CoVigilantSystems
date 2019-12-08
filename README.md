Co-Vigilant System
================================

A System that can discover, evaluate, understand, and prevent adverse effects or any other problems for restaurant.

**Team Member :** Jianfeng Lyu, Xiaoyu Wang, Kaiqing Wang, Zixuan Zeng,
Joshua Kiss

Python
================================

**Note:**The requirement.txt can help us to install all the dependency
package. the commend is : 

    pip3 install -r requirements.txt

Database
================================
I put the data what we need on the database of VM that professor give
us.(url: [http://dmdb1.cs.hofstra.edu/](http://dmdb1.cs.hofstra.edu/) ).

    Note: You should connect the vpn of our school, before connecting the
    database. 

And I create a new database and a new account for our team
`database:nonameteam. username:nonameteam. userpassword:nonameteam.` For
every thing makes sense, I also write a new sample code showing how to
connect the database .(
[SampleGetData.py](./CoVigilantSystems/SampleGetData.py) ).

[The Github url of pymysql](https://github.com/PyMySQL/PyMySQL/)

DataClean
------------
The file format of Yelp Reviews is Json or SQL, but this kind of file
isn't easy to be use.(We think CSV is better). There is an open source project dedicated to parsing the JSON file:

> https://github.com/Yelp/dataset-examples

The installation of this project is very simple, you can install it directly after the project is completed.

	git clone https://github.com/Yelp/dataset-examples
	python setup.py install

Convert review.json to CSV format with the following command:

	python json_to_csv_converter.py /dataset/yelp/dataset/review.json

After the command is executed, the corresponding CSV file review.csv will be generated in the same directory as review.json.

Convert all json file to sql file with the following command:

	./json_to_sql_converter.sh
	
After the command is executed, the 6 sql file : business.sql, checkin.sql, photo.sql, review.sql, tip.sql and user.sql will be generated with the same name as json file.

Data Analysis
------------
AnalysisFromeTimeLine.py is used to analysis the Stars of one RESTAURANT users input from the time line. You can get the mean of stars of a Restaurant by year, month, day or hour(according to what time you input by -t). The executed command is : 

	python3 AnalysisFromeTimeLine.py -n 'SpinalWorks Chiropractic' -t year (|month|day|hour) 

KeywordsAnalysis.py is used to analysis the key words for positive and negative and get the polarity of them. Then return the json data to the front side.The executed command is : 

	python3 KeywordsAnalysis.py -n 'SpinalWorks Chiropractic'

