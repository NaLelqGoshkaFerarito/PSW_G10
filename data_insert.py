"""
Project Software Engineering
Group 10

Description code:
Update SQL database with data from a CSV file.
"""
# TODO LIST:
# - Database:   Humidity is currently HARDCODED set to 0, because sensor doesnt provide it. Will need to specify where to grab the NULL from [line 48]

import MySQLdb
import csv
import sys


def create_database():
    """
    Creates a database if it doesnt exist.
    """
    cursor.execute("CREATE DATABASE IF NOT EXISTS mydatabase")


def create_tables():
    """
    Creates tables if they do not exist.
    """
    cursor.execute("CREATE TABLE IF NOT EXISTS device("
                   "name VARCHAR(255) NOT NULL,"
                   "longitude VARCHAR(255),"
                   "latitude VARCHAR(255),"
                   "altitude VARCHAR(255),"
                   "PRIMARY KEY (name))")

    cursor.execute("CREATE TABLE IF NOT EXISTS status("
                   "status_id INTEGER AUTO_INCREMENT,"
                   "device_id VARCHAR(255) ,"
                   "temperature INTEGER NOT NULL,"
                   "pressure INTEGER NOT NULL,"
                   "humidity INTEGER NOT NULL,"
                   "light INTEGER NOT NULL,"
                   "time DATETIME,"
                   "PRIMARY KEY (status_id),"
                   "FOREIGN KEY (device_id) REFERENCES device(name))")


def insert_data():
    """
    For each row in the csv file, values will be extracted and inserted into the database in their respective tables
    :return:
    """
    for row in csv_data:
        if (len(row) != 0):
            print(row)
            cursor.execute(
                "INSERT IGNORE INTO device(name, longitude, latitude,  altitude) VALUES (%s, %s, %s, %s)",
                (row[0], row[2], row[1], row[3]))
            cursor.execute(
                "INSERT INTO status(device_id, temperature, pressure, humidity, light, time) VALUES (%s, %s, %s, %s, %s,%s)",
                (row[0], row[5], row[6], 0, row[4], row[8]))


def drop_table():
    """
    Drops all tables in the database
    """
    cursor.execute(
        "DROP TABLE status"
    )
    cursor.execute(
        "DROP TABLE device"
    )


# LOCAL TESTING:
#conn = MySQLdb.connect(host="localhost", user="root", password="kaas", database="mydatabase")

conn = MySQLdb.connect(host="139.144.177.81", user="jesse", password="Kaas@1234", database="mydatabase")
cursor = conn.cursor()

csv_data = csv.reader(open('log_12_2022(1).csv'))
print('Importing the CSV Files')

create_database()
create_tables()
insert_data()
conn.commit()
cursor.close()
print('Done')
