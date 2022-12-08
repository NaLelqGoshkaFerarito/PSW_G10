"""
Project Software Engineering
Group 10
Description code:
Update SQL database with data from a CSV file.
"""

import pymysql
import pandas as pd
import sys

"""
Before importing the file, you need to prepare the following:
- A database table to which the data from the file will be imported.
- A CSV file with data that matches with the number of columns of the table and the type of data in each column.
- The account, which connects to the MySQL database server, has FILE and INSERT privileges.
"""

# For this code we assume the database has already been made.
# Guide to load CSV -> SQL: https://www.mysqltutorial.org/import-csv-file-mysql-table/

import MySQLdb
import csv
import sys

conn = MySQLdb.connect(host="localhost", user="root", password="kaas", database="mydatabase")

cursor = conn.cursor()
# cursor.execute("CREATE DATABASE mydatabase")
csv_data = csv.reader(open('loggers/logs_csv/log_12_2022.csv'))
header = next(csv_data)

print('Importing the CSV Files')
for row in csv_data:
    print(row)
    cursor.execute(
        "INSERT INTO employee (device_id, light, temperature, pressure, latitude, longitude, altitude, datetime, "
        "datenow, datelast) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", row)

conn.commit()
cursor.close()
print('Done')
