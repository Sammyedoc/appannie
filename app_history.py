import requests
import json
import os.path
import pandas as pd
import datetime

# input
parameter_set = dict(
countries='WW',          # country list as reference
feeds='downloads',       # downloads|revenue
device='all',            # all|iphone|ipad|android
granularity='monthly',   # monthly|weekly|daily
start_date='2016-01-01', # yyyy-mm-dd
end_date='2016-12-01',   # yyyy-mm-dd
)

appid_list = [
'1047246341',
'791532221',
] #sample app id

#read header
f = open("header.txt",'r')
key=f.read()
f.close()
HEADER={'Authorization':key}

# parameters
parameter_list=[
'countries',
'feeds',
'device',
'granularity',
'start_date',
'end_date']

url_base= "https://api.appannie.com/v1.2/intelligence/apps/ios/app"

# store intelligence app history
def get_response(app_id):

	# use parameter to form later part of url
	url_latter = 'history?'	
	for item in parameter_list:
		url_latter = url_latter + item +"="+ parameter_set[item]+'&'
	url_latter = url_latter[:-1]
	
	# form url
	url = os.path.join(url_base, app_id, url_latter)
	
	while True:
		try:
		# get response
			response= requests.get(url, headers=HEADER)
			response= json.loads(response.text)
			
			return response
		
		except Exception as e:
			print "there is error!:( ", e


# return app data
result=pd.DataFrame()

for appid in appid_list:
	
	response = get_response(appid) #return data from API
	
	if response['code'] == 200: #if respond successfully
		app_data = pd.DataFrame(response['list']) # estimate numbers
		# add variables to keep information such as product name
		var_list = response.keys()
		del var_list[0] # del code
		del var_list[7] # del list
		for item in var_list:
			app_data[item]=response[item] 
		
		result=pd.concat([app_data,result])
		
	else: # unsuccessful response
		print response['error']

print result

time = str(datetime.datetime.now())

result.to_csv(time+"result.csv", encoding='UTF-8')
	



