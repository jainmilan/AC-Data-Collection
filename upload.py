import csv
import time
import glob
import os
import sys
import requests
import json
import math

S_API_KEY = "3773bd8cf9594ca7a2a6c0074f73ace7"
D_Loc = "A-Home"
D_NAME = "Node-AH"
BASEPATH = [Path of CSV Folder]
URL_S = "http://sensoract.iiitd.edu.in:9000/upload/wavesegment"
while(True):
	list_of_files = glob.glob(BASEPATH+str("*.csv"))
	print list_of_files
	for f in list_of_files:
		if int(time.time())-int(os.stat(f).st_mtime)>900:
			with open(f) as filein:
				reader = csv.reader(filein, quoting=csv.QUOTE_NONNUMERIC, skipinitialspace = True)
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
						r2 = requests.post(URL_S, data=json.dumps(payload2), headers=headers)
						r3 = requests.post(URL_S, data=json.dumps(payload3), headers=headers)
#						lo=open(BASEPATH+"LOG_UPLOAD.txt","a")
#						lo.write("\n"+str(time.time())+":  "+"Values Uploaded "+str(f))
#						lo.close()
						
					except Exception as f2:
						lo=open(BASEPATH+"LOG_UPLOAD.txt","a")
						lo.write("\n"+str(time.time())+"  "+"filename: "+f +"  Error: "+f2.__str__())
						lo.close()
				lo=open(BASEPATH+"LOG_UPLOAD.txt","a")
				lo.write("\n"+str(time.time())+"  "+"Upload Success. \n Now removing file: "+str(f))
				lo.close()
				os.remove(f)
	
		else:
			lo=open(BASEPATH+"LOG_UPLOAD.txt","a")
			lo.write("\n"+str(time.time())+": File in Use \n"+f)
			lo.close()
	time.sleep(900)
