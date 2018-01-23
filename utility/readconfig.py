#-*-coding=utf-8-*-
import json
def config():

	with open('config.cfg','r') as f:
		conf=json.load(f)

	return conf
		

if __name__=='__main__':
	config()