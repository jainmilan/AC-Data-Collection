import web
import os
import MySQLdb,sys
import time,glob

# Connect to the Database
connection = MySQLdb.Connect(host='', user='root', passwd='password', db='ac_data_collection',local_infile = 1)
cursor = connection.cursor()

# File to be uploaded to the Database
PHASE = "3"
RPI_ID = "2"
APARTMENT_NO = "203"
f = "/home/milan/Data/Power_Converted/"+ APARTMENT_NO +"/Phase-" + Phase + "_" + RPI_ID + "/September/4_Power.csv"

try:
	# Uploading file to Database
	query = "LOAD DATA LOCAL INFILE " + "'" + f + "'" + " INTO TABLE room_meter_data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'(timestamp,power) SET phase = " + PHASE + ", apartment_no = " + APARTMENT_NO + ", rpi_id = " + RPI_ID + ";"	
	cursor.execute(query)
	connection.commit()

except Exception,e:
	print e

