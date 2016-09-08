#imports the required libraries and resources to run this script
import argparse
import os
import json
from xml.etree import ElementTree
import xml.etree.ElementTree as xml
from arcgis.gis import GIS
import csv
import datetime
import time
from shutil import copyfile

import pdb


def generateSeedXml(x):
    '''
    This function takes in an arcgis online item passed in to it, and generates some basic
    metadata for that item and copies that file to the child directory with the other metadata files.
    '''

    try:
        root = xml.Element("metadata")

        mdFileID = xml.SubElement(root, "mdFileID")
        mdFileID.text = x.itemid


        resTitle = xml.SubElement(root, "resTitle")
        resTitle.text = x.title


        if x.tags:
            if type(x.tags) == list:
                for tag in x.tags:
                    keyword = xml.SubElement(root, "keyword")
                    keyword.text = tag
            else:
                keyword = xml.SubElement(root, "keyword")
                keyword.text = x.tags




        if x.description:
            idAbs = xml.SubElement(root, "idAbs")
            idAbs.text = x.description

        if x.licenseInfo:
            useLimit = xml.SubElement(root, "useLimit")
            useLimit.text = x.licenseInfo

        if x.url:
            linkage = xml.SubElement(root, "linkage")
            linkage.text = x.url

        # pdb.set_trace()

        tree = xml.ElementTree(root)
        with open("{}_metadata.xml".format(x.title), "wb") as fh:
            newFile = tree.write(fh)

        metaDataFile = os.path.abspath('{}_metadata.xml'.format(x.title))
        copyfile(metaDataFile, 'downloaded/{}_{}metadata.xml'.format(x.title, x.id))

        #removes the metadata file once it's copied to another directory
        # os.remove(metaDataFile)
    except Exception as B:
        print (B)

    return



if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--portal', required=True, help=('url of the portal'))
    parser.add_argument('-u', '--username', required=True, help=('username'))
    parser.add_argument('-p', '--password', required=True, help=('password'))

    args = parser.parse_args()
    portal = args.portal
    username = args.username
    password = args.password
    badKey = None

    gis = GIS(url=portal, username=username, password=password)

    try:
        admin = gis.users.get(username)
        allItems = admin.content()
    except Exception as e:
        pass

    # an empty list to hold items with no license
    noLicense = []

    #counters
    totalCount = 0
    failCount = 0
    successCount = 0

    #loops through every folder and every item in those folders
    for folder in allItems:
        for item in allItems[folder]:
            if item.licenseInfo and item.access == 'public':
                totalCount+=1
                try:
                    metaDataFile = item.download_metadata(dir=os.getcwd())
                    metaDataFile = os.path.abspath(metaDataFile)

                    newFile = copyfile(metaDataFile, 'downloaded/{}_{}metadata.xml'.format(item.title, item.id))

                    #parses the xml file and assigns the root element
                    dom = ElementTree.parse(newFile)
                    root = dom.getroot()
                    print ("{}. {} downloaded successfully".format(totalCount, item.title))
                    successCount+=1

                    # a dictionary holidng the fieldnames for the csv
                    fieldnames = {'ArcGISProfile':'None', 'ArcGISstyle':'None', 'ArcGISFormat':'None',
                                'CreaDate':'None', 'linkage':'None', 'mdDateSt':'None', 'CreaTime':'None',
                                'useLimit':'None', 'resTitle':'None', 'metadata':'None', 'ModTime':'None',
                                'mdFileID':'None', 'keyword':'None', 'ModDate':'None', 'mdChar':'None',
                                'PublishStatus':'None', 'RoleCd':'None', 'CharSetCd':'None'}

                    # creates a hash of all the xml fields in the current metadata
                    tempDict = {}
                    for xmlFld in root.iter():
                        try:
                            if xmlFld.text.isspace() != True:
                                tempDict[xmlFld.tag] = xmlFld.text
                            else:
                                tempDict[xmlFld.tag] = 'None'
                        except:
                            pass

                    for key, value in fieldnames.items():
                        if key in tempDict:
                            fieldnames[key] = tempDict[key]
                        else:
                            pass

                    reportExists = os.path.isfile('metaDataTable.csv')
                    try:
                        with open('metaDataTable.csv', 'a') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='None', dialect='excel')
                            if reportExists == False:
                                writer.writeheader()
                                writer.writerow(fieldnames)
                            else:
                                # writer.writeheader()
                                writer.writerow(fieldnames)
                                pass
                    except:
                        pass

                except Exception as E:
                    failCount += 1
                    generateSeedXml(item)

                    print (">>>>> {}. {} had to be generated.".format(totalCount, item.title))
                    pass
            else:
                pass

    #removes the file file metadata.xml that essentially just a temportary staging file
    # os.remove('metadata.xml')
    print ("\n{} / {} downloaded successfully. {} had to be generated ".format(successCount, totalCount, failCount))
