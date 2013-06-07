import csv
import time
import glob
import os
import sys
import requests
import json
import math
import time
import datetime
from pytz import timezone

S_API_KEY = "3773bd8cf9594ca7a2a6c0074f73ace7"
D_Loc = "A-Home"
D_NAME = "Node-AH"
BASEPATH = 	"/home/milan/Projects/AC/CSVs/"					# [Path of CSV files]
URL_S = "http://sensoract.iiitd.edu.in:9000/upload/wavesegment"
now = datetime.datetime.now(timezone('Asia/Kolkata'))
while(True):
	loop_lock = 0
	Log_Filename = "Log_" + str(now.day) + "_" + str(now.month) + "_" + str(now.hour) + "_" + str(now.minute) + ".txt"
	Log_File = BASEPATH + Log_Filename
	list_of_files = glob.glob(BASEPATH+str("*.csv"))
	print list_of_files
	for f in list_of_files:
		if int(time.time())-int(os.stat(f).st_mtime)>900:
			with open(f) as filein:
				reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
				lo=open(Log_File,"a")
				lo.write("\n"+str(time.time())+"  "+"Starting Upload for File: -"+str(f))
				lo.close()

				for row in reader:
					timestamp = math.fabs(row[0])
					temperature = row[1]
					pir = row[2]
					light = row[3]
					
					headers = { 'Content-Type': 'application/json; charset=UTF-8'}
					payload1 = { 'secretkey' : S_API_KEY, "data" : { "loc" : D_Loc, "dname" : str(D_NAME), "sname" :"PIRSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [pir] } ] } }
					payload2 = { 'secretkey' : S_API_KEY, "data" : { "loc" : D_Loc, "dname" : str(D_NAME), "sname" :"TemperatureSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [temperature] } ] } }
					payload3 = { 'secretkey' : S_API_KEY, "data" : { "loc" : D_Loc, "dname" : str(D_NAME), "sname" :"LightSensor", "sid" : "1", "timestamp" : timestamp, "channels" : [ { "cname" : "channel1", "unit" : "none","readings" : [light] } ] } }

					try:
						r1 = requests.post(URL_S, data=json.dumps(payload1), headers=headers)
						time.sleep(1)
						r2 = requests.post(URL_S, data=json.dumps(payload2), headers=headers)
						time.sleep(1)
						r3 = requests.post(URL_S, data=json.dumps(payload3), headers=headers)

					except Exception as f2:
						lo=open(Log_File,"a")
						lo.write("\n"+str(time.time())+"  "+"filename: "+f +"  Error: "+f2.__str__())
						lo.close()
						loop_lock = 1
						break
					time.sleep(2)
		else:
			lo=open(Log_File,"a")
			lo.write("\n"+str(time.time())+": File in Use \n"+f)
			lo.close()
		time.sleep(1)
		if loop_lock == 0:
			lo=open(Log_File,"a")
			lo.write("\n"+str(time.time())+"  "+"Upload Success. \n Now removing file: "+str(f))
			lo.close()
			os.remove(f)
		else:
			lo=open(Log_File,"a")
			lo.write("\n"+str(time.time())+"  "+"Connectivity Issue, Going to sleep ")
			lo.close()
			
	time.sleep(900)
