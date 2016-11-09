#imports the required libraries and resources to run this script
import argparse
import os
import json
import xml.etree.ElementTree as xml
from lxml import etree
from arcgis.gis import GIS
import csv
import datetime
from time import strftime
from shutil import copyfile
import pdb


def generateSeedXml(agoItem):
    '''
    This function takes in an arcgis online item passed in to it, and generates some basic
    metadata for that item and copies that file to the child directory with the other metadata files.
    '''
    try:
        root = etree.Element("metadata")
        dataIdInfo = etree.SubElement(root, "dataIdInfo")
        idCitation = etree.SubElement(dataIdInfo, "idCitation")
        
        resTitle = etree.SubElement(idCitation, "resTitle")
        resTitle.text = agoItem.title
        
        #might need to remove nesting on line below
        if agoItem.description:
            idAbs = etree.SubElement(dataIdInfo, "idAbs")
            idAbs.text = agoItem.description

    
        searchKeys = etree.SubElement(idCitation, "searchKeys")
        if agoItem.tags:
            if type(agoItem.tags) == list:
                for tag in agoItem.tags:
                    keyword = etree.SubElement(searchKeys, "keyword")
                    keyword.text = tag
            else:
                keyword = etree.SubElement(searchKeys, "keyword")
                keyword.text = agoItem.tags


        resConst = etree.SubElement(idCitation, "resConst")
        Consts = etree.SubElement(resConst, "Consts")
        useLimit = etree.SubElement(Consts, "useLimit")
        if agoItem.licenseInfo:
            useLimit.text = agoItem.licenseInfo

        #ESRI 
        Esri = etree.SubElement(root, "Esri")
        ArcGISFormat = etree.SubElement(Esri, "ArcGISFormat")
        ArcGISFormat.text = "1.0"
        ArcGISProfile = etree.SubElement(Esri, "ArcGISProfile")
        mdDateSt = etree.SubElement(root, "mdDateSt")
        mdFileID = etree.SubElement(root, "mdFileID")
        mdFileID.text = agoItem.itemid        
        mdContact = etree.SubElement(root, "mdContact")
        rpOrgName = etree.SubElement(root, "rpOrgName")

        tree = etree.tostring(root, pretty_print=True)

        #writes the formatted xml to a file
        with open("{}_metadata.xml".format(agoItem.title), "wb") as fh:
            fh.write(tree)
            fh.close()

        metaDataFile = os.path.abspath('{}_metadata.xml'.format(agoItem.title))

        '''renames and copies the metadata file to the downloaded directory and optionally
           removes the original file
        '''
   
        copyfile(metaDataFile, 'downloaded/{}_{}_SEED_metadata.xml'.format(agoItem.title, agoItem.id))

        #removes the metadata file once it's copied to another directory
        # os.remove(metaDataFile)

    except Exception as B:
        pass
    else:
        return metaDataFile


def updateXml(seedFile, row):
    '''
    this function accepts the path to an xml metadata file to upload to AGOL.
    this is necessarry to gain the ability to pull download metadata for that
    item for the first time
    '''

    dom = etree.parse(seedFile)
    root = dom.getroot()
    itemId = dom.findtext('mdFileID')

    if row:
        item_properties = {'title':row['resTitle'], 'tags':row['keyword'], 
                        'description':row['idAbs'], 'licenseInfo':row['useLimit']}
        try:
            item = gis.content.get(itemId)
        except Exception as e:
            pass
        update = item.update(item_properties, metadata=seedFile)
    else:
        try:
            item = gis.content.get(itemId)
        except Exception as e:
            pass
        update = item.update(metadata=seedFile)

    return


def bulkMdWriter():
    '''
    this function reads in the csv and produces valid AGOL metadata in the form 
    of xml files for every row in it
    '''
    count = 0
    with open ('metaDataTable.csv') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            try:
                root = etree.Element("metadata")
                dataIdInfo = etree.SubElement(root, "dataIdInfo")
                idCitation = etree.SubElement(dataIdInfo, "idCitation")
                idPoc = etree.SubElement(dataIdInfo, "idPoc")
                
                # update frequency metadata
                resMaint = etree.SubElement(dataIdInfo, "resMaint")
                maintFreq = etree.SubElement(resMaint, "maintFreq")
                MaintFreqCd = etree.SubElement(maintFreq, "MaintFreqCd")
                MaintFreqCd.set("value", row['MaintFreqCd'])

                #update title
                resTitle = etree.SubElement(idCitation, "resTitle")
                resTitle.text = row['resTitle']

                #update revision data
                reviseDate = etree.SubElement(idCitation, "reviseDate")
                reviseDate.text = row['reviseDate']

                #update published date
                date = etree.SubElement(idCitation, "date")
                pubDate = etree.SubElement(date, "pubDate")


                rpIndName = etree.SubElement(idPoc, "rpIndName")
                rpIndName.text = row['rpIndName']
                
        
                # if row['idAbs']:
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
                # ArcGISstyle = etree.SubElement(Esri, "ArcGISstyle")
                # ArcGISstyle.text = row['ArcGISstyle']

                CreaDate = etree.SubElement(Esri, "CreaDate")
                CreaDate.text = row['CreaDate']



                ModDate = etree.SubElement(Esri, "ModDate")
                ModDate.text = row['ModDate']


                ArcGISFormat = etree.SubElement(Esri, "ArcGISFormat")
                ArcGISFormat.text = "1.0"



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
                #uploads the more robust metadata as read from the csv
                updateXml(metaDataFile, row)

                #removes the metadata file once it's copied to another directory
                os.remove(metaDataFile)
                count += 1
                print('{}. {} {} updated'.format(count, row['resTitle'], row['mdFileID']))

            except Exception as B:
                print(B)
                pass
    return



#script starting
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

    
    #counters
    totalCount = 0
    failCount = 0
    successCount = 0
    
    #checks the flags entered by the user and only runs if -c is used
    if args.c and not args.m:
        try:
            admin = gis.users.get(username)
            print('\nGathering items for {}. This can take several minutes depending on the number of items in your org...'.format(username))
        except Exception as e:
            pass
        
        
        reportExists = os.path.isfile('metaDataTable.csv')

        #removes the old csv if it exists and the user wants to generate a new one
        if reportExists == True:
            os.remove('metaDataTable.csv')


        # gathers all items in the root directory
        allItems = admin.items()

        #loops through every folder in the root directory and adds the valid items to the list of items gathered from the root directory
        for folder in admin.folders:
            x = folder['title']
            folderItems = admin.items(folder=x, max_items=5000)
            allItems.extend(folderItems)

            
        for item in allItems:
            if item.access == 'public':
                totalCount+=1

                try:
                    metaDataFile = item.download_metadata(save_folder=os.getcwd())
                    metaDataFile = os.path.abspath(metaDataFile)
                    
                    #this block checks for items that need to have metadata generated for them 
                    with open (metaDataFile) as metaCheck:
                        try:
                            for line in metaCheck:
                                jsonCheck = json.loads(line)
                                if jsonCheck['error']['message'] == 'Metadata for item not found':
                                    print(">>>>got here", item.title)
                                    
                                    #generates seed metadata if the script is unable to access the current metadata
                                    if generateSeedXml(item) != None:
                                        metaDataFile = generateSeedXml(item)
                                        print (">>>>> {}. {} had to be generated.".format(totalCount, item.title))
                                        updateXml(metaDataFile, row=False)
                    
                                else:
                                    print("Error encountered")
                        except:
                            pass

                    #checks if downloaded folder exists, and creates if it does not
                    if not os.path.exists('downloaded'):
                        os.makedirs('downloaded')
    
                    newFile = copyfile(metaDataFile, 'downloaded/{}_{}metadata.xml'.format(item.title, item.id))
                    
                    #parses the xml file and assigns the root element
                    try:
                        creationDate = datetime.datetime.fromtimestamp(item.created/1000)
                        creationDate = creationDate.strftime('%Y%m%d')

                        dom = etree.parse(newFile) 
                        root = dom.getroot()


                        print ("{}. {} - {} downloaded successfully".format(totalCount, item.id, item.title))
                        successCount+=1

                        #a dictionary holding the fieldnames for the csv
                        fieldnames = [  'resTitle',
                                        'mdFileID',
                                        'useLimit',
                                        'keyword',
                                        'CreaDate',
                                        'idAbs',
                                        'ModDate',
                                        'CharSetCd',
                                        'RoleCd', 
                                        'TopicCatCd',
                                        'reviseDate',
                                        'rpIndName', 
                                        'EmailAdd',
                                        'MaintFreqCd']


                        fields = {  'TopicCatCd':'None', 
                                    'rpIndName':'None',
                                    'reviseDate':'None',
                                    'CreaDate':creationDate,
                                    'mdDateSt':'None',
                                    'MaintFreqCd':'None',
                                    'useLimit':'None', 
                                    'resTitle':item.title, 
                                    'mdFileID':item.id, 
                                    'keyword':[], 
                                    'ModDate': strftime("%x"), 
                                    'RoleCd':'None', 
                                    'CharSetCd':'None', 
                                    'idAbs': 'None'}
                        

                        for f in fieldnames:
                            for xmlFld in root.iter():
                                if xmlFld.tag == f and xmlFld.text != 'None':
                                    try:
                                        fields[f] = xmlFld.text
                                    except:
                                        pass
                                if type(xmlFld.tag) == list:
                                    for tags in xmlFld.tag:
                                        fields['keyword'].append(tags) 

            
                    except:
                        totalCount-=1
                        print(item.title)
            
                    #checks that the csvfile currently exists, to decide if a header row needs to be printed        
                    reportExists = os.path.isfile('metaDataTable.csv')
                    try:
                        with open('metaDataTable.csv', 'a') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval='None', extrasaction='ignore', dialect='excel')
                            if reportExists == False:
                                writer.writeheader()
                                writer.writerow(fields)
                            else:
                                writer.writerow(fields)
                                pass
                    except:
                        print("an error occured while creating the csv")
                        pass

                except (AttributeError):
                    failCount += 1
                    pass
                    

        #removes the file metadata.xml that essentially just a temportary staging file
        os.remove('metadata.xml')
        
        print ("\n{} / {} downloaded successfully.".format(successCount, totalCount))
        if failCount > 0:
            print("{} had to be generated. Run the script with the -c flag to access an up-to-date csv of your items, including any that were just generated.".format(failCount))

    #if the -m flag is set and valid, the function to create valid xml files from the csv is called
    elif args.m and not args.c:
        try:
            bulkMdWriter()
        except Exception as fail:
            print ('Error creating xml from csv: {}'.format(fail))
            pass

    #error message if user tries to use -c and -m together
    elif args.c and args.m:
        print("Invalid entry. You can't use -c and -m at the same time.")

    else:
        print ("Missing parameter. You must choose to use -c to create a csv or -m to create metadata")
























