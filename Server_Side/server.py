import os
import web
import time
import json
import pytz
import random
import datetime
import matplotlib
matplotlib.use('Agg')
import MySQLdb,sys
from threading import Lock
import matplotlib.dates as md
import matplotlib.pyplot as plt

# Threading 
lock = Lock()

# URLS
urls = ('/','home',
		'/upload', 'Upload',
		'/query','query',
		'/csvupload', 'CSVUpload')

APARTMENT_NO = "203"
filedir = "/home/milan/Data/Temperature/" + APARTMENT_NO

# HTML Page
render = web.template.render('templates')

TIMEZONE='Asia/Kolkata'

# Connect to database
db = web.database(dbn='mysql', db='ac_data_collection', user='root', pw='password')

# By Default
class home:
	def GET(self):
		return render.index()

# Receive files from RPi
class Upload:
   def POST(self):
		x = web.input(myfile={})
		if 'myfile' in x: # to check if the file-object is created
			filepath = x.myfile.filename	#.replace('\\','/') # replaces the windows-style slashes with linux ones.
			filename = filepath.split('/')[-1] # splits the and chooses the last part (the filename with extension)
			file_date = filename.split('_')
			print filename
			path = filedir + "/" + file_date[0] + "/" + file_date[2] + "/" + file_date[1] + "/"	
			if not os.path.exists(path):
				os.makedirs(path)
			fout = open(path + filename,'w') # creates the file where the uploaded file should be stored
			fout.write(x.myfile.file.read()) # writes the uploaded file to the newly created file.
			fout.close() # closes the file, upload complete.

# Plot using CSV Files
class CSVUpload:
	def POST(self):

		# Read uploaded temperature CSV 
		temperature_file = web.input(temperaturefile={})
		temperature = []
		temperature_timestamp = []
		
		# If any file exist
		if 'temperaturefile' in temperature_file:
			# Get Complete File
			temperature_file_data = temperature_file.temperaturefile.value
			# Seprate both the Readings
			temperature_data = temperature_file_data.split('\n')
			
			# Iterate through each reading
			for element in temperature_data:
				split_temperature_data = element.split(',')
				if len(split_temperature_data[0]) > 1:
					# Errorneous Readings
					if float(split_temperature_data[2]) > 40:
						continue
					# Timestamp Array
					temperature_timestamp.append(int(split_temperature_data[0]))
					# Array of temperature Readings
					temperature.append(float(split_temperature_data[2]))

		else:
			return json.dumps({"status":"Temperature CSV not uploaded"})
		
		power_file = web.input(powerfile={})
		power = []
		power_timestamp = []
		if 'powerfile' in power_file:
			power_file_data = power_file.powerfile.value
			power_data = power_file_data.split('\n')
			for element in power_data:
				split_power_data = element.split(',')
				if len(split_power_data) > 1:
					power_datetime = split_power_data[0].split("+")
					format_time = '%Y-%m-%dT%H:%M:%S'
					split_datetime = datetime.datetime.strptime(power_datetime[0],format_time)
					power_timestamp.append(int(time.mktime(split_datetime.timetuple())))
					power.append(float(split_power_data[1]))
		else:
			return json.dumps({"status":"Power CSV not uploaded"})
		
		temperature_dates = [datetime.datetime.fromtimestamp(ts1) for ts1 in temperature_timestamp]
		power_dates = [datetime.datetime.fromtimestamp(ts2) for ts2 in power_timestamp]

		with lock:
			figure = plt.gcf() # get current figure
			plt.axes().relim()
			ax1 = figure.add_subplot(111)											
			plt.title("Power vs Time")
			ax1.set_xlabel('Time')										
			ax1.set_ylabel('Temperature(C)', color='b')
			ax1.plot(temperature_dates,temperature,'b-')	
			plt.axes().autoscale_view(True,True,True)
			ax2 = ax1.twinx()
			ax2.plot(power_dates,power,'r-')
			ax2.set_ylabel('Power(Watts)', color='r')
			figure.autofmt_xdate()
			ax = plt.gca()
			xfmt = md.DateFormatter('%Y\n%b-%d\n%H:%M')
			ax.xaxis.set_major_formatter(xfmt)
			ax.set
			plt.grid()
			plt.xticks( rotation=25 )
			filename = "hello.jpg"
			plt.savefig("/home/milan/Projects/3.Summer_Semester/AC_Data_Collection/Scripts/Server_Side/static/images/"+filename, bbox_inches=0,dpi=100)
			plt.close()
			web.header('Content-Type', 'application/json')
			return json.dumps({"status":"Plotting Done","filename":filename})
		
		

class query:
	def POST(self):
		data = web.data()
		query_data = json.loads(data)
		start_time = query_data["start_time"]
		end_time = query_data["end_time"]
		rpiid = query_data["rpiid"]
		temperature_t = query_data["temperature"]
		power_t = query_data["power"]
		
		start_datetime = datetime.datetime.fromtimestamp(start_time,pytz.timezone(TIMEZONE))
		end_datetime = datetime.datetime.fromtimestamp(end_time,pytz.timezone(TIMEZONE))
		
		query_temperature = "SELECT temperature,timestamp FROM room_temperature_data WHERE rpi_id = " + rpiid + " AND timestamp BETWEEN " + str(start_time) + " AND " + str(end_time) + ";"
		retrieved_data_temperature = list(db.query(query_temperature))
		LEN_temperature = len(retrieved_data_temperature)
		temperature_timestamp = [0]*LEN_temperature
		temperature = [0]*LEN_temperature
		temperature_datetime = [None]*LEN_temperature
		for i in range(0,LEN_temperature):
			temperature_timestamp[i] = retrieved_data_temperature[i]["timestamp"]
			temperature[i] = retrieved_data_temperature[i]["temperature"]
			temperature_datetime[i] = datetime.datetime.fromtimestamp(temperature_timestamp[i])#,pytz.timezone(TIMEZONE))
		
		query_power = "SELECT power,timestamp FROM room_meter_data WHERE rpi_id = " + rpiid + " AND timestamp BETWEEN " + str(start_time) + " AND " + str(end_time) + ";"
		retrieved_data_power = list(db.query(query_power))
		LEN_power = len(retrieved_data_power)
		power_timestamp = [0]*LEN_power
		power = [0]*LEN_power
		power_datetime = [None]*LEN_power
		for i in range(0,LEN_power):
			power_timestamp[i] = retrieved_data_power[i]["timestamp"]
			power[i] = retrieved_data_power[i]["power"]
			power_datetime[i] = datetime.datetime.fromtimestamp(power_timestamp[i])#,pytz.timezone(TIMEZONE))
		
		with lock:
		
			filename = ""
			# Only Temperature
			if temperature_t and power_t!=True:
				figure = plt.gcf() # get current figure
				plt.axes().relim()
				plt.title("Temperature vs Time")
				plt.xlabel("Time")
				plt.ylabel("Temperature")
				plt.axes().autoscale_view(True,True,True)
				figure.autofmt_xdate()
				ax = plt.gca()
				xfmt = md.DateFormatter('%H:%M\n%Y,%b-%d')
				ax.xaxis.set_major_formatter(xfmt)
				plt.plot(temperature_datetime,temperature,'b-')
				filename = str(start_datetime.day)+"_"+str(start_datetime.month)+"_"+str(start_datetime.hour)+"_"+str(start_datetime.minute)+"-"+str(end_datetime.day)+"_"+str(end_datetime.month)+"_"+str(end_datetime.hour)+"_"+str(end_datetime.minute)+"_Temperature.png"
				plt.savefig("/home/milan/Server/static/images/"+filename, bbox_inches=0,dpi=100)
				plt.close()
		
			# Only Power
			elif power_t and temperature_t!=True:
				figure = plt.gcf() # get current figure
				plt.axes().relim()
				plt.title("Power vs Time")
				plt.xlabel("Time")
				plt.ylabel("Power")
				plt.axes().autoscale_view(True,True,True)
				figure.autofmt_xdate()
				ax = plt.gca()
				xfmt = md.DateFormatter('%Y\n%b-%d\n%H:%M')
				ax.xaxis.set_major_formatter(xfmt)
				plt.plot(power_datetime,power,'r-')
				filename = str(start_datetime.day)+"_"+str(start_datetime.month)+"_"+str(start_datetime.hour)+"_"+str(start_datetime.minute)+"-"+str(end_datetime.day)+"_"+str(end_datetime.month)+"_"+str(end_datetime.hour)+"_"+str(end_datetime.minute)+"_Power.png"
				plt.savefig("/home/milan/Server/static/images/"+filename, bbox_inches=0,dpi=100)
				plt.close()
		
			# Default Plot
			else:
				figure = plt.gcf() # get current figure
				plt.axes().relim()
				ax1 = figure.add_subplot(111)											
				plt.title("Power vs Time")
				ax1.set_xlabel('Time')										
				ax1.set_ylabel('Temperature(C)', color='b')
				ax1.plot(temperature_datetime,temperature,'b-')	
				plt.axes().autoscale_view(True,True,True)
				ax2 = ax1.twinx()
				ax2.plot(power_datetime,power,'r-')
				ax2.set_ylabel('Power(Watts)', color='r')
				figure.autofmt_xdate()
				ax = plt.gca()
				xfmt = md.DateFormatter('%Y\n%b-%d\n%H:%M')
				ax.xaxis.set_major_formatter(xfmt)
				#ax.set
				plt.grid()
				plt.xticks( rotation=25 )
				filename = str(start_datetime.day)+"_"+str(start_datetime.month)+"_"+str(start_datetime.hour)+"_"+str(start_datetime.minute)+"-"+str(end_datetime.day)+"_"+str(end_datetime.month)+"_"+str(end_datetime.hour)+"_"+str(end_datetime.minute)+"_Both.png"
				plt.savefig("/home/milan/Server/static/images/"+filename, bbox_inches=0,dpi=100)
				plt.close()
			
			web.header('Content-Type', 'application/json')
			return json.dumps({"status":"Plotting Done","filename":filename})
		web.header('Content-Type', 'application/json')
		return json.dumps({"temperature":y,"power":X})
        
if __name__ == "__main__":
   app = web.application(urls, globals())
   app.run()
