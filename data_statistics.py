#-----Task Description-----------------------------------------------#
#
#  DATA STATISTICS
#
#  In this task you will use a Python program to construct and
#  interrogate an SQL database to produce statistics for
#  a large amount of textual data.
#
#  You are required to write the following four functions:
#
#  1) populate_table
#  This function reads data from a file specified by the parameter
#  and enters the data into a table which has the same name as the
#  file, and then returns the number of rows inserted.
#
#  2) best_and_worst
#  Given the name of a make of car, this function prints the make and
#  the minimum and maximum overall rating given to cars of this make
#  by the owners.  If no such make of car exists the function must
#  print an appropriate message.
#
#  3) most_expensive
#  This function prints the make, model, price and overall rating of
#  the most expensive cars in the database, one car per line.
#  Its parameter is a number specifying how many lines to print.
#
#  4) average_ratings
#  Given a make of car, this function prints the average overall
#  rating awarded to each model of this make.  If no such make of
#  car exists the function must print an appropriate message.
#
#  In each case use the unit tests below to determine the layout of
#  the result to be printed.  Take particular note of the sequence
#  in which the results must be printed as this may influence the
#  ordering you specify in your SQL query.
#
#--------------------------------------------------------------------#


#-----Acceptance Tests-----------------------------------------------#
#
#  This section contains the unit tests that your program must
#  pass.  You may not change anything in this section.  NB: When
#  your program is marked the following tests will be used as
#  well as some additional tests (not provided) to ensure your
#  solution works for other cases.
#
"""
---------- Populating the database tables

>>> int(populate_table("car_details")) # Test 1 (updated)
3119

>>> int(populate_table("car_ratings")) # Test 2 (updated)
5504

---------- Best and worst overall ratings 

>>> best_and_worst('TOYOTA') # Test 3
TOYOTA (1-5)

>>> best_and_worst('VOLVO') # Test 4
VOLVO (2-5)

>>> best_and_worst('LEXUS') # Test 5
LEXUS (4-5)

>>> best_and_worst('CADILLAC') # Test 6
CADILLAC (4-4)

>>> best_and_worst('LIGHTBURN') # Test 7
No such make of car!

---------- Most expensive cars

>>> most_expensive(1) # Test 8
FERRARI 575M: $551000, Overall rating 4

>>> most_expensive(4) # Test 9
FERRARI 575M: $551000, Overall rating 4
FERRARI 599: $551000, Overall rating 5
MERCEDES-BENZ E55: $225600, Overall rating 5
JAGUAR XJR: $178000, Overall rating 5

>>> most_expensive(15) # Test 10
FERRARI 575M: $551000, Overall rating 4
FERRARI 599: $551000, Overall rating 5
MERCEDES-BENZ E55: $225600, Overall rating 5
JAGUAR XJR: $178000, Overall rating 5
MERCEDES-BENZ E500: $153900, Overall rating 1
BMW 7: $145900, Overall rating 4
BMW 7: $136500, Overall rating 4
JAGUAR XJ8: $126500, Overall rating 3
JAGUAR S TYPE: $124500, Overall rating 5
MERCEDES-BENZ 300: $124500, Overall rating 4
LEXUS LX470: $119100, Overall rating 4
MERCEDES-BENZ CLK230: $112200, Overall rating 5
MERCEDES-BENZ CLK320: $112200, Overall rating 4
MERCEDES-BENZ E280: $112200, Overall rating 5
MERCEDES-BENZ E280: $112200, Overall rating 3
 
>>> most_expensive(0) # Test 11 (produces no output)

---------- Average ratings of the cars

>>> average_ratings('HOLDEN') # Test 12 (updated)
MONARO 4.8
TORANA 4.6
VIVA 4.4
PREMIER 4.4
COMBO 4.3
CRUZE 4.3
CALAIS 4.3
KINGSWOOD 4.3
BERLINA 4.2
JACKAROO 4.2
NOVA 4.1
ASTRA 4.1
BARINA 4.0
COMMODORE 4.0
VECTRA V6 4.0
ADVENTRA 3.9
CAPTIVA 3.9
VECTRA 3.8
CREWMAN 3.8
CAMIRA 3.7
EPICA 3.7
FRONTERA 3.6
RODEO 3.6
CALIBRA 3.6

>>> average_ratings('KIA') # Test 13 (updated)
OPTIMA 5.0
PREGIO 5.0
GRAND CARNIVAL 4.9
MAGENTIS 4.4
SORENTO 4.3
CERATO 4.3
K2700 4.0
RIO 3.8
SPORTAGE 3.6
CARNIVAL 3.5
SPECTRA 3.3
MENTOR 3.0

>>> average_ratings('DAIHATSU') # Test 14
COPEN 5.0
MIRA 5.0
APPLAUSE 4.4
TERIOS 4.2
CHARADE 4.0
SIRION 4.0
FEROZA 3.8
PYZAR 3.7

>>> average_ratings('LIGHTBURN') # Test 15
No such make of car!

""" 
#
#--------------------------------------------------------------------#

# Get the MySQL-Python functions:
import MySQLdb

##    # Alternative for Mac users:
##    import mysql.connector
##    MySQLdb = mysql.connector


#Connect to our database and assign our cursor.
connection = MySQLdb.connect(host = "127.0.0.1", user = "root", 
                       passwd = "", db = "car_reviews")
cursor = connection.cursor()


#Function to read a text file, process the line and output to a database. Returns row count.
def populate_table(filename):
     text_file =  file(filename + '.txt')
     rows_inserted = 0

     #remove existing db information before inserting more.
     sqlquery_truncate = "TRUNCATE TABLE " + filename 
     cursor.execute(sqlquery_truncate) 

     #processes each row of text into a string ready to be used by our SQL query. Then INSERT into db.
     for line in text_file:
          wordlist = line.strip().split('\t')
          query_string = ""
          for word in wordlist:
               if word == wordlist[-1]:
                    query_string = query_string + "'" + word + "'"
               else:
                    query_string = query_string + "'" + word + "'" + ", "
          sqlquery_insert = "INSERT INTO " + filename + " VALUES(" + query_string + ")"
          cursor.execute(sqlquery_insert)
     connection.commit()

     #Count how many rows we have in our db and return the row count.
     sqlquery_count_rows = "SELECT COUNT(*) FROM " + filename
     cursor.execute(sqlquery_count_rows)
     row_count = cursor.fetchall()
     row_count = int(row_count[0][0])
     return row_count


# Function to query the db and print the minimum and
# maximum overall score for the reqested make of car.
# Prints an appropriate message if no result found.
def best_and_worst(car_make):
     sqlquery_select_ratings = "SELECT MIN(overallRating), MAX(overallRating) \
     FROM car_details INNER JOIN car_ratings ON car_details.carId=car_ratings.carId\
     WHERE make = '" + car_make + "'"
     cursor.execute(sqlquery_select_ratings)
     min_max_ratings = cursor.fetchall()
     min_rating = min_max_ratings[0][0]
     max_rating = min_max_ratings[0][1]

     if min_rating == None:
          print "No such make of car!"
     else:
          print car_make + " (" + str(min_rating) + "-" + str(max_rating) + ")"


# This function prints the most expensive cars in our db.
# Displays the number of rows based on the function paramater. 
def most_expensive(number_of_rows_to_display):
     sqlquery_most_expensive = 'SELECT make, model, price, overallRating\
     FROM car_details INNER JOIN car_ratings ON car_details.carId=car_ratings.carId ORDER \
     BY price DESC, make ASC, model ASC, overallRating DESC LIMIT 0,' + str(number_of_rows_to_display)
     cursor.execute(sqlquery_most_expensive)
     most_expensive_list = cursor.fetchall()
     
     for cars in most_expensive_list:
          car_make = cars[0]
          car_model = cars[1]
          car_price = cars[2]
          overall_rating = cars[3]
          print car_make + " " + car_model + ": $" + str(car_price) + ", Overall rating " + str(overall_rating)


# This function prints the average overall rating for every model of a
# particular make of car, as defined by the paramater.
# Prints an appropriate message if no result found.
def average_ratings(make_of_car):
     sqlquery_average_ratings = "SELECT model, AVG(overallRating) AS AverageRating \
     FROM car_details INNER JOIN car_ratings ON car_details.carId=car_ratings.carId \
     WHERE make = '" + make_of_car + "' GROUP BY model ORDER BY AverageRating DESC, model ASC"
     cursor.execute(sqlquery_average_ratings)
     average_ratings_list = cursor.fetchall()
     
     if average_ratings_list == () or len(average_ratings_list) == 0:
          print "No such make of car!"
     else:     
          for car_rating in average_ratings_list:
               car_model = car_rating[0]
               average_rating = car_rating[1]
               rounded_average_rating = str(round(average_rating, 1))
               print car_model + " " + rounded_average_rating


#--------------------------------------------------------------------#



#-----Automatic Testing----------------------------------------------#
#
#  The following code will automatically run the acceptance tests
#  when the program is "run".  Do not change anything in this
#  section.  If you want to prevent the tests from running, comment
#  out the code below, but ensure that the code is uncommented when
#  you submit your program.
#
if __name__ == "__main__":
     from doctest import testmod
     testmod(verbose=True)   
#
#--------------------------------------------------------------------#

