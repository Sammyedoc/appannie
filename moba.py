import requests
import json
import pandas as pd
import numpy as np
import datetime

f = open("header.txt",'r')
key=f.read()
f.close()

HEADER={'Authorization':key}

MONTHS=[
'2015-01-01',
'2015-02-01',
'2015-03-01',
'2015-04-01',
'2015-05-01',
'2015-06-01',
'2015-07-01',
'2015-08-01',
'2015-09-01',
'2015-10-01',
'2015-11-01',
'2015-12-01',
'2016-01-01',
'2016-02-01',
'2016-03-01',
'2016-04-01',
'2016-05-01',
'2016-06-01',
'2016-07-01',
'2016-08-01',
'2016-09-01',
'2016-10-01',
'2016-11-01',
'2016-12-01']

def get_gamedata(url):
	
	res= requests.get(url, headers=HEADER)
	res= json.loads(res.text)

	return res
	
def get_rank(response):
	
	rank = pd.DataFrame(response['list'])
	
	rank['date'] = response['start_date']
	
	return rank
	
def get_description(game):

	while True:
	
	 	try:
			url = "https://api.appannie.com/v1.2/apps/ios/app/"+game+"/details"	
			response = requests.get(url, headers=HEADER)
			response = json.loads(response.text)
			
			return response
			
		except Exception as e:
		
			print "there is error!:( ", e

def find_MOBA(game_list):

	for item in game_list:
		if game_list[item]['description'].find('MOBA') == -1:
			continue
		else:
			MOBA_list[item]= game_list[item]
			
			print MOBA_list[item]['product_name']
			
	return MOBA_list

# get gamelist

def get_gamelist(months):
	
	result=pd.DataFrame()
	
	for month in months:

		url = "https://api.appannie.com/v1.2/intelligence/apps/ios/ranking?countries=WW&categories=Overall > Games&feeds=free&ranks=1000&granularity=monthly&device=ios&start_date="+month+"&end_date="+month

		response = get_gamedata(url)
	
		ranks = get_rank(response)
	
		result = result.append(ranks)
	
		print month

	#unique games for retrieving description data
	gamelist = result['product_id'].unique()

	gamelist = gamelist.tolist()
	gamelist = map(str, gamelist)
	
	return gamelist



gamelist = get_gamelist(MONTHS[:2])

#retrive game description
result_app = dict()
MOBA_list = dict()
trouble_list = []

count = 0

for game in gamelist[:10]:
	
	response = get_description(game)
	
	count = count +1
	
	if response['code'] == 200 :
	
		result_app[game]=response['product']
			
		print count, response['product']['product_name']
		
	else:
		print count, response['error']
		trouble_list.append(game)

time = str(datetime.datetime.now())

df = pd.DataFrame(result_app)
df_t = df.transpose()
df_t.to_csv(time+"MOBA_raw.csv",encoding = 'utf-8')

# find item with "MOBA" word

find_MOBA(result_app)

df_MOBA = pd.DataFrame(MOBA_list)
df_MOBA = df_MOBA.transpose()
df_MOBA.to_csv(time+"MOBA.csv",encoding = 'utf-8')

	
