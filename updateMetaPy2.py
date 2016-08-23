import argparse
import os
import requests
import json
from xml.etree import ElementTree
import csv
import datetime


def genToken(user, passw, portal):
	if portal:
		url = '{}/sharing/rest/generateToken'.format(portal)
		params ={'username': user, 'password': passw, 'client': 'referer', 'referer': portal, 'expiration': 60, 'f': 'json'}
		query = requests.post

		try:
			r = requests.post(url, data=params)
			return r.json()['token']
		except:
			return None
	else:
		print("Error: Must specify a portal")
		return

def updateMetaData(username, folderId, itemId, file, portal, token):

	parameters = {'token': token,'f': 'json'}
	endPoint = '{}/sharing/rest/content/users/{}/{}/items/{}/update'.format(portal, username, folderId, itemId)
	test = requests.post(endPoint, data = parameters)
	return test.json()


def getItemData(itemId, portal, token):
	'''Grabs the item's folder from agol, to construct the url'''
	parameters = {'token': token, 'f': 'json'}
	endPoint = '{}/sharing/rest/content/items/{}'.format(portal, itemId)
	resp = requests.get(endPoint, params=parameters)
	return resp.json()


if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--portal', help = ('url of the portal'))
	parser.add_argument('-u', '--username', required=True, help=('username'))
	parser.add_argument('-p', '--password', required=True, help=('password'))
	#parser.add_argument('-f', '--path', help=('path to directory holding metadata files to update'))

	args = parser.parse_args()
	portal =  args.portal
	username = args.username
	password = args.password
	# userPath = args.path


	userToken = genToken(username, password, portal)

	#will only run if a valid token was generated
	if userToken != None:
		#a list holding the files in the current directory
		folder = os.listdir(os.curdir)
		metaDataList = []
		badFiles = []
		badFilesDict = {}

		#Checks every file in the directory, and adds valid metadata files to a list
		for file in folder:
			itemId = None
			fullFile = os.path.abspath(file)
			try:
				dom = ElementTree.parse(fullFile)
				if dom.findtext('mdFileID'):
					itemId = dom.findtext('mdFileID')
			except Exception as e:
				badFilesDict[file] = e
				pass

			if file[-4:] == '.xml' and itemId != None:
				metaDataList.append(file)
		count = 0
		for file in metaDataList:
			fullFile = os.path.abspath(file)
			dom = ElementTree.parse(fullFile)
			itemId = dom.findtext('mdFileID')

			try:
				item = getItemData(itemId, portal, userToken)
			except Exception as e:
				pass

			if item['ownerFolder']:
				pass

			else:
				item['ownerFolder'] = ''

			try:
				count+=1
				update = updateMetaData(username, item['ownerFolder'], itemId, fullFile, portal, userToken)
				currentTime = datetime.datetime.now()

				print "#{}".format(count)
				print "title: {}".format(item['title'])
				print "item id: {}".format(itemId)
				print "updated: {}".format(update['success'])
				print "time: ", datetime.datetime.now(), "\n"

				reportExists = os.path.isfile('report.csv')

				with open('report.csv', 'a') as csvfile:
					fieldnames  = ['TITLE', 'ID', 'UPDATED', 'DATE/TIME', 'FILE']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

					if reportExists == False:
						writer.writeheader()
					writer.writerow({'TITLE':item['title'], 'ID':item['id'], 'UPDATED':update['success'], 'DATE/TIME':datetime.datetime.now(), 'FILE': file})

			except KeyError as b:
				print b
				pass

		for key, value in badFilesDict.items():
			errorReportExists = os.path.isfile('errors.csv')
			with open('errors.csv', 'a') as csvfile:
				fieldnames  = ['FILE', 'ERROR', 'DATE/TIME',]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

				if errorReportExists == False:
					writer.writeheader()
				writer.writerow({'FILE': key,'ERROR': value, 'DATE/TIME':currentTime})

		print ("Updating complete. {} items updated.".format(count))
	else:
		print "\nCould not generate a valid token. Check your credentials."
