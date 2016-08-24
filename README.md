
##Introduction
This repo will hold a set of Python 3 scripts leveraging our new [ArcGIS Python Beta API](https://developers.arcgis.com/python/) to perform various administrative tasks by an admin. More scripts will be added in the near future, and everyone with access to this repo is encouraged to contribute to it.

##Requirements and Installation

To run the script you'll need to install the following dependencies.

* Python 3 [Install instructions](https://www.continuum.io/downloads)
* Conda and ArcGIS package [Install instructions](https://developers.arcgis.com/python/guide/Install-and-set-up/)
* Clone the repo - ```git clone git@github.com:ArcGIS/python-admin.git```

Note: There is no universal installation of Python 3 currently so you will have to be sure that you're calling the exact same version of python 3 where you installed the ArcGIS Beta API. Using the command `which python3` will return the path to your current default python 3, and is a useful tool for verifying. The python 3 version you want to use for this script should be in your ```/anaconda/bin``` directory, similar to below.

```
bash-3.2$ which python3
/Users/<user_name>/anaconda/bin/python3
```

##Preparing your MetaData for update
1. Log in to your open data site.
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

##[updateMetaPy3.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy3.py)
This script will look through all files in a directory and if any valid metadata files are available, it will update that respective item in ArcGIS Online with the local metadata file. When completed it will produce 2 files. `report.csv` is a list of the ArcGIS Online items and times they were updated. `errors.csv` is a list of the files in the directory that were not valid metadata and the error message. This is for python 3 and makes use of the ArcGIS Python Beta API

flags scripts accepts:  
  * `-a` this flag specifies which open data site you want to administer __[required]__    
  * `-u` this flag sets the username to log in with __[required]__    
  * `-p` this flag sets the password associated with the username __[required]__    

##Example
`python3 updateMetaPy3.py -u <username> -p <password> -a https://www.arcgis.com`

Once the script is completed. Refer to step 7 above but instead of clicking edit, this time click view to observe your changes. Below are two screenshots of the metadata pre and post edit.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/6_7.jpg "before editing and after editing")


###Python 2 support
Where possible I will try to include Python 2 versions of the scripts using the ArcGIS rest api and fairly generic functions, but support for Python 2 is not guaranteed moving forward, and using our new Python 3 API is highly encouraged.

###[updateMetaPy2.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy2.py)
This script will look through all the files in a directory and if any valid metadata files are available, it will update the respective item in agol with that metadata file. When completed, it will produce 2 files. `report.csv` is a list of the items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 2 and aside from the `requests` package every library it uses is included in the python standard library.

###Required to run:
* Python 2

  * Requests [link](http://docs.python-requests.org/en/master/)

  #####Example
  `python updateMetaPy2.py -u <username> -p <password> -a https://www.arcgis.com`


##Contributing

Anyone and everyone is welcome to contribute. Please see our [guidelines for contributing](https://github.com/esri/contributing).

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

A copy of the license is available in the repository's [license.txt](https://github.com/ArcGIS/python-admin/blob/master/license.txt) file.

[](Esri Tags: Python ArcGIS API XML Metadata Administration)
[](Esri Language: Python)
