#imports the required libraries and resources to run this script
import argparse
import os
import json
from xml.etree import ElementTree
from arcgis.gis import GIS
import csv
import datetime
import pdb

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-a', '--portal', required=True, help=('url of the portal'))
	parser.add_argument('-u', '--username', required=True, help=('username'))
	parser.add_argument('-p', '--password', required=True, help=('password'))
	parser.add_argument('-f', '--path', help=('path to directory holding metadata files to update'))

	args = parser.parse_args()
	portal =  args.portal
	username = args.username
	password = args.password
	path = args.path
	badKey = None

	gis = GIS(url=portal, username=username, password=password)

	try:
		if gis.properties['user']:
			gis = GIS(url=portal, username=username, password=password)

	except KeyError as e:
		badKey = e
		pass

	#will only run if a valid connection to a portal was made
	if badKey == None:

		#a list holding the files in the current directory
		folder = os.listdir(os.curdir)
		metaDataList = []
		badFiles = []
		badFilesDict = {}
		# itemId = ''

		#Checks every file in the directory, and adds valid metadata files to a list
		for file in folder:
			fullFile = os.path.abspath(file)
			try:
				dom = ElementTree.parse(fullFile)
				itemId = dom.findtext('mdFileID')
			except Exception as e:
				badFilesDict[file] = e
				pass

			if file[-4:] == '.xml' and itemId:
				metaDataList.append(file)

		for file in metaDataList:
			fullFile = os.path.abspath(file)
			dom = ElementTree.parse(fullFile)
			itemId = dom.find('mdFileID').text

			try:
				item = gis.content.get(itemId)
			except Exception as e:
				pass

			try:
				update = item.update(metadata=file)
				currentTime = datetime.datetime.now()

				print("Status: ", update)
				print("Updated: ", itemId)

				reportExists = os.path.isfile('report.csv')

				with open('report.csv', 'a') as csvfile:
					fieldnames  = ['TITLE', 'ID', 'UPDATED', 'DATE/TIME', 'FILE']
					writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

					if reportExists == False:
						writer.writeheader()
					writer.writerow({'TITLE':item.title, 'ID':item.id, 'UPDATED':update, 'DATE/TIME':currentTime, 'FILE': file})

			except KeyError as b:
				pass

		for key, value in badFilesDict.items():
			errorReportExists = os.path.isfile('errors.csv')
			with open('errors.csv', 'a') as csvfile:
				fieldnames  = ['FILE', 'ERROR', 'DATE/TIME',]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

				if errorReportExists == False:
					writer.writeheader()
				writer.writerow({'FILE': key,'ERROR': value, 'DATE/TIME':datetime.datetime.now()})


		print ("Updating complete")
	else:
		pass
		# print("\nInvalid log in attempt. Check your credentials.")
