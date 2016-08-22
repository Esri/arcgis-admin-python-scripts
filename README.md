This repo will hold a set of Python 3 scripts leveraging our new [ArcGIS Python Beta API](https://developers.arcgis.com/python/) to perform various administrative tasks by an admin. More scripts will be added in the near future, and everyone with access to this repo is encouraged to contribute to it. Where possible I will try to include Python 2 versions of the scripts using the ArcGIS rest api and fairly generic functions.

####Required to run:
* Python 2

  * Requests [link](http://docs.python-requests.org/en/master/)


* Python 3 for Python 3 scripts

  * ArcGIS Beta API [link](https://developers.arcgis.com/python/guide/Install-and-set-up/)

##Scripts included

####[updateMetaPy3.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy3.py)
This script will look through all the files in a directory and if any valid metadata files are available, it will update that respective item in agol with the local metadata file. When completed it will produce 2 files. `report.csv` is a list of the Agol items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 3 and makes use of the ArcGIS Python Beta API

#####Example
`python3 updateMetaPy3.py -u <username> -p <password> -a https://opendata.arcgis.com`

Note: There is no universal installation of Python 3 currently so you will have to be sure that you're calling the exact same version of python 3 where you installed the ArcGIS Beta API. Using the command `which python3` will return the path to your current default python 3, and is a useful tool for verifying. The python 3 version you want to use for this script should be in your /anaconda/bin directory.

![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/1.png "which python3 example")



####[updateMetaPy2.py](https://github.com/ArcGIS/python-admin/blob/master/updateMetaPy2.py)
This script will look through all the files in a directory and if any valid metadata files are available, it will update the respective item in agol with that metadata file. When completed, it will produce 2 files. `report.csv` is a list of the items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 2 and aside from the `requests` package every library it uses is included in the python standard library.




flags scripts accepts:  
  * `-a` this flag specifies which ArcGIS portal you want to administer __[required]__    
  * `-u` this flag sets the username to log in with __[required]__    
  * `-p` this flag sets the password associated with the username __[required]__    


#####Example 
`python updateMetaPy2.py -u <username> -p <password> -a https://opendata.arcgis.com`




###Accessing Your Metadata
1. Log in to your opendata portal.
	e.g. http://opendata.arcgis.com

1. Click on the username dropdown in the upper right corner.
1. Click on your username to be taken to your user profile page.
1. Click on 'My Content' at the top of the page and you will be shown a view of all your items similar to the example photo below.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/2.png "My Content")
1. Click on an item to view a detailed page for that item. 
1. On the right hand side of the page you should see see a set of buttons, some with dropdown funtionality. 
 ![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/3.png "detailed page")
1. Click the Metadata dropdown, and then choose "edit"
1. Click the "Save Local Copy" button to download the metadata in the form of an xml file for that item.
![alt text](https://github.com/ArcGIS/python-admin/blob/master/images/4.png "save local copy example")
1. Edit the metadata as you like, being careful not to edit the `<mdFileID>` field at all.
1. Run the script from the same directory as the xml file you downloaded and edited.
1. When completed, verify that the changes you made to your local file are reflected in the corresponding item online.

