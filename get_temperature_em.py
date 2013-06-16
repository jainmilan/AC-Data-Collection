APPKEY = [APP-KEY]
CITY = "New Delhi"
FORMAT = "json"
BASE_URL_1 = "http://api.worldweatheronline.com/free/v1/weather.ashx"
REQUEST_URL_1 = BASE_URL_1+"?q=%s&format=%s&key=%s" %(CITY,FORMAT,APPKEY)

CITY_ID = 1273294
BASE_URL_2 = "http://api.openweathermap.org/data/2.5/weather"
REQUEST_URL_2 = BASE_URL_2+"?id=%d" %(CITY_ID)

import requests
import datetime
import time

while True:
	json_data_1=requests.get(REQUEST_URL_1).json()
	data_1 = json_data_1['data']['current_condition']
	date_1 = json_data_1['data']['weather'][0]["date"]
	time_1 = data_1[0]['observation_time']
	date_time = str(date_1)+" "+str(time_1)
	timestamp_1 = int(datetime.datetime.strptime(date_time, '%Y-%m-%d %I:%M %p').strftime("%s")) + 19800
	date_up = datetime.datetime.fromtimestamp(timestamp_1).strftime('%Y-%m-%d %H:%M:%S')
	temperature_1 = data_1[0]['temp_C']
	humidity_1 = data_1[0]['humidity']
	Data_file = open("/home/milan/Projects/Summer_Project/Scripts/data_1.csv","a")
	Data_file.write(str(timestamp_1)+","+str(date_up)+","+str(temperature_1)+","+str(humidity_1)+"\n")
	
	json_data_2 = requests.get(REQUEST_URL_2).json()
	temperature_2 = (json_data_2["main"]['temp'])-273.15
	humidity_2 = json_data_2["main"]['humidity']
	time_2 = json_data_2["dt"]
	date_2 = datetime.datetime.fromtimestamp(time_2).strftime('%Y-%m-%d %H:%M:%S')
	Data_file = open("/home/milan/Projects/Summer_Project/Scripts/data_2.csv","a")
	Data_file.write(str(time_2)+","+str(date_2)+","+str(temperature_2)+","+str(humidity_2)+"\n")
	
	time.sleep(600)
	
	
