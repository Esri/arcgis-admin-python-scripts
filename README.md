
##Introduction
This repo will hold a set of Python 3 scripts leveraging our new [ArcGIS Python Beta API](https://developers.arcgis.com/python/) to perform various administrative tasks by an admin. More scripts will be added in the near future, and everyone with access to this repo is encouraged to contribute to it.

##Requirements and Installation

To run the script you'll need to install the following dependencies.

* Python 3 [Install instructions](https://www.continuum.io/downloads)
* Conda and ArcGIS package [Install instructions](https://developers.arcgis.com/python/guide/Install-and-set-up/)
* Clone the repo - ```git clone git@github.com:Esri/arcgis-admin-python-scripts.git```

Note: There is no universal installation of Python 3 currently so you will have to be sure that you're calling the exact same version of python 3 where you installed the ArcGIS Beta API. Using the command `which python3` will return the path to your current default python 3, and is a useful tool for verifying. The python 3 version you want to use for this script should be in your ```/anaconda/bin``` directory, similar to below.

```
bash-3.2$ which python3
/Users/<user_name>/anaconda/bin/python3
```

##Preparing your MetaData for update
1. Log in to your ArcGIS site.
	e.g. http://www.arcgis.com
1. Click on the username dropdown in the upper right corner.
1. Click on your username to be taken to your user profile page.
1. Click on 'My Content' at the top of the page and you will be shown a view of all your items similar to the example photo below.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/2.png "My Content")
1. Click on an item to view a detailed page for that item.
1. On the right hand side of the page you should see see a set of buttons, some with dropdown funtionality.
 ![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/3.png "detailed page")
1. Click the Metadata dropdown, and then choose "edit"
1. Click the "Save Local Copy" button to download the metadata in the form of an xml file for that item.
1. Copy the metadata xml file(s) to the same directory as the `UpdateMetaPy3.py` file.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/4.png "save local copy example")
1. Open the metadata in your editor of choice, being careful not to edit the `<mdFileID>` field at all.
  *  In the screenshot below I've changed the title of the metadata by removing the '2015' from the yellow circled field.
  *  The field in the red circle should not be changed as it's the canonical id for the item in ArcGIS online, and is what the script uses to find the item online.
    ![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/5.png "editing the metadata")



##Run the update script

####[updateMetaPy3.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy3.py)
This script will look through all files in a directory and if any valid metadata files are available, it will update that respective item in ArcGIS Online with the local metadata file. When completed it will produce 2 files. `report.csv` is a list of the ArcGIS Online items and times they were updated. `errors.csv` is a list of the files in the directory that were not valid metadata and the error message. This is for python 3 and makes use of the ArcGIS Python Beta API

flags scripts accepts:  
  * `-a` this flag specifies sets the GIS you want to administer __[required]__    
  * `-u` this flag sets the username to log in with __[required]__    
  * `-p` this flag sets the password associated with the username __[required]__    

##Example
* `python3 updateMetaPy3.py -u <username> -p <password> -a https://www.arcgis.com`

Once the script is completed. Refer to step 7 above but instead of clicking edit, this time click view to observe your changes. Below are two screenshots of the metadata pre and post edit.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/6_7.jpg "before editing and after editing")

####[mdBulkEdit.py](https://github.com/Esri/arcgis-admin-python-scripts/blob/metaDataBulkEdit/mdBulkEdit.py)
This script performs multiple functions, based on the flag an admin passes to it. If you're running this script for the first time, you have to use the optional `-c` flag to generate the file `metaDataTable.csv` which is the csv of the metadata for the items you want to edit. If the script is unable access the metadata for any item, it will post a message to the screen that this is the case, generate its own basic metadata and then upload that to AGOL, to seed in ability to access and edit more robust metadata for that item. IF this is the case, you will then have to run the script again, with the same `-c` flag so that it can now incorporate the AGOL items you couldn't access before. Once you've run the script to generate the csv necessary, you can then edit the fields of the csv as desired. When you're ready to push those changes to online, run the script again, but this time with the `-m` flag.

flags script accepts:
  * `-a` this flag specifies sets the GIS you want to administer __[required]__    
  * `-u` this flag sets the username to log in with __[required]__    
  * `-p` this flag sets the password associated with the username __[required]__ 
  * `-c` is the optional flag used have the script generate a csv of all your public, open data items.__[optional]__
  * `-m` is the optional flag used to have the script build valid xml metadata files from the csv you generated with the `-c` flag.__[optional]__

##Examples
 * `python3 mdBulkEdit.py -u <username> -p <password> -a http://www.arcgis.com -c`

 * `python3 mdBulkEdit.py -u <username> -p <password> -a http://www.arcgis.com -m`



####Python 2 support
Where possible I will try to include Python 2 versions of the scripts using the ArcGIS rest api and fairly generic functions, but support for Python 2 is not guaranteed moving forward, and using our new Python 3 API is highly encouraged.

####[updateMetaPy2.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy2.py)
This script will look through all the files in a directory and if any valid metadata files are available, it will update the respective item in agol with that metadata file. When completed, it will produce 2 files. `report.csv` is a list of the items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 2 and aside from the `requests` package every library it uses is included in the python standard library.

####Required to run:
* Python 2

  * Requests [link](http://docs.python-requests.org/en/master/)

  ##Example
  * `python updateMetaPy2.py -u <username> -p <password> -a https://www.arcgis.com`


##Contributing

Contributing to Esri Open Source Projects

Esri welcomes contributions to our [open source projects on Github](http://esri.github.io/).

##Issues

Feel free to submit issues and enhancement requests.

Please refer to each project's style guidelines and guidelines for submitting patches and additions. In general, we follow the "fork-and-pull" Git workflow.

 1. **Fork** the repo on GitHub
 2. **Clone** the project to your own machine
 3. **Commit** changes to your own branch
 4. **Push** your work back up to your fork
 5. Submit a **Pull request** so that we can review your changes

NOTE: Be sure to merge the latest from "upstream" before making a pull request!


##Licensing
Copyright 2016 Esri

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

A copy of the license is available in the repository's [license](https://github.com/ArcGIS/python-admin/blob/master/LICENSE) file.

[](Esri Tags: Python ArcGIS API XML Metadata Administration)
[](Esri Language: Python)
