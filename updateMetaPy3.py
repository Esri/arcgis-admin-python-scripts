import argparse
import os
import arcgis
import json
from xml.etree import ElementTree
from arcgis.gis import GIS
import csv
import datetime

if __name__=='__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('-u', '--portal', help = ('url of the portal'))
	parser.add_argument('-o', '--username', required=True, help='username')
	parser.add_argument('-s', '--password')
	parser.add_argument('-p', '--path', help = 'path to metadata file')
	parser.add_argument('-i', '--itemId', help = 'id of the item to be updated')

	args = parser.parse_args()
	portal =  args.portal
	username = args.username
	password = args.password
	itemId = args.itemId
	path = args.path


	gis = GIS(url=portal, username=username, password=password)
	print (gis)

	#will only run if a valid connection to a portal was made
	if gis != None:
		#a list holding the files in the current directory
		folder = os.listdir(os.curdir)
		metaDataList = []
		badFiles = []
		badFilesDict = {}

		#Checks every file in the directory, and adds valid metadata files to a list
		for file in folder:
			fullFile = os.path.abspath(file)
			try:
				dom = ElementTree.parse(fullFile)
				itemId = dom.find('mdFileID').text
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
				if item['ownerFolder']:
					print("item id: ", item.id)
					print("title: ", item.title)
					print("\n")

				else:
					item['ownerFolder'] = ''
					print("item id: ", item.id)
					print("title: ", item.title)
					print("\n")

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
				print (b)
				pass

		for key, value in badFilesDict.items():
			errorReportExists = os.path.isfile('errors.csv')
			with open('errors.csv', 'a') as csvfile:
				fieldnames  = ['FILE', 'ERROR', 'DATE/TIME',]
				writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

				if errorReportExists == False:
					writer.writeheader()
				writer.writerow({'FILE': key,'ERROR': value, 'DATE/TIME':currentTime})


		print ("Updating complete")
	else:
		print("\nCould not generate a valid token. Check your credentials.")
