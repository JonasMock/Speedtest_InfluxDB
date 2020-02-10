# Runs speedtest via speedtest.net, extracts data and saves to InfluxDB

import subprocess
import pandas as pd
import datetime
from influxdb import InfluxDBClient
import dateutil.parser as dp

Home_SSID = ""
user = ''
password = ''
dbname = ''
protocol = 'json'
host=''
port=
home = False
csvOutputPath = ""
measurement = "speedtest"
hostTag = "JonasMacBook"

#Connection to InfluxDB
def main(host, port):
	"""Instantiate the connection to the InfluxDB client."""
	client = InfluxDBClient(host, port, user, password, dbname)

	print("Create database: " + dbname)
	client.create_database(dbname)

	print("Get DB")
	client.get_list_database()

	print("Write points: {0}".format(json_body))
	client.write_points(json_body)

	print("Read DataFrame")
	client.query("select * from speedtest")

	#print("Delete database: " + dbname)
	#client.drop_database(dbname)

import subprocess

#Check if connected WiFi is at Home
try:

	result = subprocess.run(['/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport', '-I'], stdout=subprocess.PIPE)

	result = str(result).split()

	ssid = result[result.index("SSID:") + 1]

	if Home_SSID in ssid:
		home = True

except ValueError:
        print("Probably not connected to WiFi!")

# Only if you're at home
if home:

	#Capture Console output from Speedtest CLI
	result = subprocess.run(['/usr/local/bin/speedtest-cli', '--csv'], stdout=subprocess.PIPE)

	#Export Speedtest CLi Output to CSV
	with open(csvOutputPath, mode = "a") as the_file:
		the_file.write(result.stdout.decode("utf-8"))
		the_file.newlines
	the_file.close()

	#Open and edit .csv output from Speedtest CLI
	df = pd.read_csv(csvOutputPath)
	df['Download'] = df['Download'].apply(lambda x: x / 1000000)
	df['Upload'] = df['Upload'].apply(lambda x: x / 1000000)

	for index in df.index:
		json_body = [
			{
				"measurement": measurement,
				"tags": {
					"host": hostTag 
				},
					"time": df[(df.index == index)]['Timestamp'].values[0],
				"fields":{
					"Server_ID": df[(df.index == index)]['Server ID'].values[0],
					"Sponsor": df[(df.index == index)]['Sponsor'].values[0],
					"Server Name": df[(df.index == index)]['Server Name'].values[0],
					"Distance": df[(df.index == index)]['Distance'].values[0],
					"Ping": df[(df.index == index)]['Ping'].values[0],
					"Download": df[(df.index == index)]['Download'].values[0],
					"Upload": df[(df.index == index)]['Upload'].values[0],
					"IP Address": df[(df.index == index)]['IP Address'].values[0]
					 }
				}
			]
	main(host, port)
else:
	print("Nicht Zuhause")
