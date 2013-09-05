import os
import web
import time,glob
import MySQLdb,sys

# Input directory
RPI_ID = "1"
APARTMENT_NO = "1102"
MONTH = "9"
DATE = "2"
filedir = "/home/milan/Data/Temperature/" + APARTMENT_NO + "/" + RPI_ID + "/" + MONTH + "/"+ DATE +"/"

# Connect to the database
connection = MySQLdb.Connect(host='', user='root', passwd='password', db='ac_data_collection',local_infile = 1)
cursor = connection.cursor()

### In case we want to iterate through multiple folders ###

#folders=os.listdir(filedir)
#print folders
#for folder in folders:
	#list_of_files=glob.glob(str(filedir)+str(folder)+str("/*.csv"))

# List of all files
list_of_files = glob.glob(str(filedir)+str("/*.csv"))

# Iterate through each file in the folder
for f in list_of_files:
	
	try:
		# Upload to the Database
		query = "LOAD DATA LOCAL INFILE " + "'" + f + "'" + " INTO TABLE room_temperature_data FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n'(timestamp,temperature) SET rpi_id = " + RPI_ID + ", apartment_no = " + APARTMENT_NO + ";"	
		cursor.execute(query)
		connection.commit()

	except Exception,e:
			print e

