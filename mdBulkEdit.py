#imports the required libraries and resources to run this script
import argparse
import os
import json
import xml.etree.ElementTree as xml
from lxml import etree
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
        root = etree.Element("metadata")
        dataIdInfo = etree.SubElement(root, "dataIdInfo")
        idCitation = etree.SubElement(dataIdInfo, "idCitation")
        
        resTitle = etree.SubElement(idCitation, "resTitle")
        resTitle.text = x.title
        
        if x.description:
            idAbs = etree.SubElement(dataIdInfo, "idAbs")
            idAbs.text = x.description

    
        searchKeys = etree.SubElement(idCitation, "searchKeys")
        if x.tags:
            if type(x.tags) == list:
                for tag in x.tags:
                    keyword = etree.SubElement(searchKeys, "keyword")
                    keyword.text = tag
            else:
                keyword = etree.SubElement(searchKeys, "keyword")
                keyword.text = x.tags

        
        resConst = etree.SubElement(idCitation, "resConst")
        Consts = etree.SubElement(resConst, "Consts")
        useLimit = etree.SubElement(Consts, "useLimit")
        if x.licenseInfo:
            useLimit.text = x.licenseInfo

        #ESRI 
        Esri = etree.SubElement(root, "Esri")
        ArcGISstyle = etree.SubElement(Esri, "ArcGISstyle")
        ArcGISstyle.text = "ISO 19139 Metadata Implementation Specification" #needs to go in the dictionary

       
        ArcGISFormat = etree.SubElement(Esri, "ArcGISFormat")
        ArcGISFormat.text = "1.0"
        ArcGISProfile = etree.SubElement(Esri, "ArcGISProfile")


        mdDateSt = etree.SubElement(root, "mdDateSt")
        mdFileID = etree.SubElement(root, "mdFileID")
        mdFileID.text = x.itemid

        
        mdContact = etree.SubElement(root, "mdContact")
        rpOrgName = etree.SubElement(root, "rpOrgName")

        tree = etree.tostring(root, pretty_print=True)

        #writes the formatted xml to a file
        with open("{}_metadata.xml".format(x.title), "wb") as fh:
            fh.write(tree)
            fh.close()

        metaDataFile = os.path.abspath('{}_metadata.xml'.format(x.title))

        '''renames and copies the metadata file to the downloaded directory and optionally
           removes the original file
        '''
        copyfile(metaDataFile, 'downloaded/{}_{}_SEED_metadata.xml'.format(x.title, x.id))

        #removes the metadata file once it's copied to another directory
        # os.remove(metaDataFile)

    except Exception as B:
        print (B)
        print('>>>3.', type(metaDataFile))
        pass
    return metaDataFile


def uploadSeedXml(seedFile):
    '''
    this function accepts the path to an xml metadata file to upload to AGOL.
    this is necessarry to gain the ability to pull download metadata for that
    item for the first time
    '''

    dom = etree.parse(seedFile)
    root = dom.getroot()

    itemId = dom.findtext('mdFileID')
    
    try:
        item = gis.content.get(itemId)
    except Exception as e:
        pass
    update = item.update(metadata=seedFile)

    return


def bulkMdWriter():
    '''
    this function takes a csv as a variable, and produces valid AGOL meta data in the form 
    of xml files for every entry 
    '''
    with open ('metaDataTable.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                root = etree.Element("metadata")
                dataIdInfo = etree.SubElement(root, "dataIdInfo")
                idCitation = etree.SubElement(dataIdInfo, "idCitation")
                
                resTitle = etree.SubElement(idCitation, "resTitle")
                resTitle.text = row['resTitle']

                date = etree.SubElement(idCitation, "date")
                pubDate = etree.SubElement(date, "pubDate")

                
                if row['idAbs']:
                    idAbs = etree.SubElement(dataIdInfo, "idAbs")
                    idAbs.text = row['idAbs']

                    dataLang = etree.SubElement(idCitation, "dataLang")
                    languageCode = etree.SubElement(dataLang, "languageCode")
                    languageCode.set("value", "eng")


                    dataChar = etree.SubElement(idCitation, "dataChar")
                    CharSetCd = etree.SubElement(dataChar, "CharSetCd")
                    CharSetCd.set("value","004" )

                    tpCat = etree.SubElement(idCitation, "tpCat")
                    TopicCatCd = etree.SubElement(tpCat, "TopicCatCd")

                    searchKeys = etree.SubElement(idCitation, "searchKeys")
                    if row['keyword']:
                        if type(row['keyword']) == list:
                            for tag in row['keyword']:
                                keyword = etree.SubElement(searchKeys, "keyword")
                                keyword.text = tag
                        else:
                            keyword = etree.SubElement(searchKeys, "keyword")
                            keyword.text = row['keyword']

                    
                    resConst = etree.SubElement(idCitation, "resConst")
                    Consts = etree.SubElement(resConst, "Consts")
                    useLimit = etree.SubElement(Consts, "useLimit")
                    if row['useLimit']:
                        useLimit.text = row['useLimit']

                    #ESRI 
                    Esri = etree.SubElement(root, "Esri")
                    ArcGISstyle = etree.SubElement(Esri, "ArcGISstyle")
                    ArcGISstyle.text = row['ArcGISstyle']

                    CreaDate = etree.SubElement(Esri, "CreaDate")
                    CreaDate.text = row['CreaDate']

                    CreaTime = etree.SubElement(Esri, "CreaTime")
                    CreaTime.text = row['CreaTime']

                    ModDate = etree.SubElement(Esri, "ModDate")
                    ModDate.text = row['ModDate']

                    ModTime = etree.SubElement(Esri, "ModTime")
                    ModTime.text = row['ModTime']

                    ArcGISFormat = etree.SubElement(Esri, "ArcGISFormat")
                    ArcGISFormat.text = "1.0"

                    ArcGISProfile = etree.SubElement(Esri, "ArcGISProfile")
                    ArcGISProfile.text = row['ArcGISProfile']

                    mdDateSt = etree.SubElement(root, "mdDateSt")

                    mdFileID = etree.SubElement(root, "mdFileID")
                    mdFileID.text = row['mdFileID']

                    mdChar = etree.SubElement(root, "mdChar")
                    CharSetCd = etree.SubElement(mdChar, "CharSetCd")
                    CharSetCd.set("value", "004")

                    mdContact = etree.SubElement(root, "mdContact")
                    rpOrgName = etree.SubElement(root, "rpOrgName")

                    role = etree.SubElement(root, "role")
                    RoleCd = etree.SubElement(role, "RoleCd")
                    RoleCd.set("value", "007")

                    tree = etree.tostring(root, pretty_print=True)
                    
                    #writes the formatted xml to a file
                    with open("{}_metadata.xml".format(row['resTitle']), "wb") as fh:
                        fh.write(tree)
                        fh.close()

                    metaDataFile = os.path.abspath('{}_metadata.xml'.format(row['resTitle']))

                    '''renames and copies the metadata file to the downloaded directory and optionally
                       removes the original file
                    '''
                    
                    uploadSeedXml(metaDataFile)

                    #removes the metadata file once it's copied to another directory
                    os.remove(metaDataFile)

            except Exception as B:
                print(B)
                pass
    return



#Script Starting
if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--portal', required=True, help=('url of the portal'))
    parser.add_argument('-u', '--username', required=True, help=('username'))
    parser.add_argument('-p', '--password', required=True, help=('password'))
    parser.add_argument('-c', help=('flag to generate csv of public open data items'), action='store_true')
    parser.add_argument('-m', help=('flag to produce and upload metadata'), action='store_true')

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
    
    
    if args.c and not args.m:
        #counters
        totalCount = 0
        failCount = 0
        successCount = 0
        reportExists = os.path.isfile('metaDataTable.csv')

        if reportExists == True:
            os.remove('metaDataTable.csv')

        '''loops through every folder and every item in those folders in search of public
            open data items'''
        for folder in allItems:
            for item in allItems[folder]:
                if item.licenseInfo and item.access == 'public':
                    totalCount+=1

                    try:
                        metaDataFile = item.download_metadata(dir=os.getcwd())
                        metaDataFile = os.path.abspath(metaDataFile)
                        newFile = copyfile(metaDataFile, 'downloaded/{}_{}metadata.xml'.format(item.title, item.id))
                        
                        #parses the xml file and assigns the root element
                        dom = etree.parse(newFile)
                        root = dom.getroot()
                        
                        print ("{}. {} downloaded successfully".format(totalCount, item.title))
                        successCount+=1

                        # a dictionary holidng the fieldnames for the csv
                        fieldnames = {'ArcGISProfile':'None', 'ArcGISstyle':'None', 'ArcGISFormat':'1.0',
                                    'CreaDate':'None', 'mdDateSt':'None', 'CreaTime':'None',
                                    'useLimit':'None', 'resTitle':'None', 'metadata':'None', 'ModTime':'None',
                                    'mdFileID':'None', 'keyword':'None', 'ModDate':'None', 'PublishStatus':'None', 
                                    'RoleCd':'None', 'CharSetCd':'None', 'idAbs': 'None'}

                        # to store a hash of all the xml fields in the current metadata
                        tempDict = {}

                        for xmlFld in root.iter(): 
                            try:
                                if xmlFld.tag in fieldnames and xmlFld.text.isspace() != True:
                                    fieldnames[xmlFld.tag] = xmlFld.text
                                else:
                                    pass
                
                            except:
                                pass

                        reportExists = os.path.isfile('metaDataTable.csv')
                        try:
                            with open('metaDataTable.csv', 'a') as csvfile:
                                writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='None', extrasaction='ignore', dialect='excel')
                                if reportExists == False:
                                    writer.writeheader()
                                    writer.writerow(fieldnames)
                                else:
                                    writer.writerow(fieldnames)
                                    pass
                        except:
                            pass

                    except Exception as E:
                        failCount += 1

                        metaDataFile = generateSeedXml(item)
                        print (">>>>> {}. {} had to be generated.".format(totalCount, item.title))
                        # uploadSeedXml(metaDataFile)
                        pass


        #removes the file file metadata.xml that essentially just a temportary staging file
        os.remove('metadata.xml')
        print ("\n{} / {} downloaded successfully. {} had to be generated. ".format(successCount, totalCount, failCount))
        if failCount > 0:
            print("Run the script with the -c flag again.")

    elif args.m and not args.c:
        bulkMdWriter()
        pass

    elif args.c and args.m:
        print("Invalid entry. You can't use -c and -m at the same time.")

    else:
        print ("Missing parameter. You must choose to use -c to create a csv or -m to create metadata")





























