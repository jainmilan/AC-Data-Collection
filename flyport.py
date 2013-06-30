import web
import json
import csv
import datetime
import time
from pytz import timezone
import math


global init_time
init_time = time.time()
global init_time_t
init_time_t = datetime.datetime.now(timezone('Asia/Kolkata'))

BASEPATH = [Path of CSV Folder]

urls = (
    '/', 'flyport'
)
app = web.application(urls, globals())

GLOBAL_DATA = BASEPATH + "data.csv"
class flyport:        
        
	def POST(self):
		# Data from the Request Received
		data = web.data()
		packet = json.loads(data)
		
		# Unpacking the Values
		temperature = packet['Temperature']
		PIR = packet['PIR']
		light = packet['Light']
		timestamp = packet['timestamp']
		
		# Current Time
		current_time = time.time()
		global init_time
		global init_time_t
		
		# Collect 15 Minutes of Data
		end_time = init_time + 900
		if current_time > end_time:
			init_time = current_time
			init_time_t = init_time_t = datetime.datetime.now(timezone('Asia/Kolkata'))
			
		# File to be Uploaded	
		FILENAME = BASEPATH+str(init_time_t.day)+"_"+str(init_time_t.month)+"_"+str(init_time_t.hour)+"_"+str(init_time_t.minute)+".csv"
		file = open(FILENAME,"a")
		upload_time = time.time()
		
		# Create CSV
		file.write(str(upload_time)+","+str(temperature)+","+str(PIR)+","+str(light)+"\n")
		file.close()
		
		# File Won't be deleted, Local Data Storage
		file_global = open(GLOBAL_DATA,"a")
		upload_time = time.time()
		file_global.write(str(upload_time)+","+str(temperature)+","+str(PIR)+","+str(light)+"\n")
		file_global.close()
		print(data)
		
if __name__ == "__main__":
    app.run()
