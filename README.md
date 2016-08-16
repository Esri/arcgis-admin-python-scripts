This repo will hold a set of Python scripts to facilitate performing various administrative tasks by an admin. More sctipts will be added in the near future, and everyone with access to this repo can contribute. Where possible I will try to include both Python 2 versions of the scripts using the ArcGIS rest api and fairly agnostic functions. And I will also provide Python 3 versions of the scripts leveraging our new [ArcGIS Python Beta API](https://developers.arcgis.com/python/).

####Required to run:
*Python 2

*Requests [link](http://docs.python-requests.org/en/master/)

*Python 3 for Python 3 scripts
*ArcGIS Beta API [link](https://developers.arcgis.com/python/guide/Install-and-set-up/)

##Scripts included

####[updateMetaPy2.py]
This script will look through all the files in a directory and if any valid metadata files are available, it will update the respective item in agol with that metadata file. When completed, it will produce 2 files. `report.csv` is a list of the items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 2 and aside from the `requests` package every library it uses is included in the python standard library.
#####Example
`python updateMetaPy2.py -o <username> -s <password> -u <portal>`



####[updateMetaPy3.py]
This script will look through all the files in a directory and if any valid metadata files are available, it will update the respective item in agol with that metadata file. When completed, it will produce 2 files. `report.csv` is a list of the items and times they were updated. `errors.csv` is a list of the files in the directory that were not updated and the error message. This is for python 3 and makes use of the ArcGIS Python Beta API

#####Example
`python3 updateMetaPy3.py -o <username> -s <password> -u <portal>`




###To test
1. Log in to portal and download the metadata of agol item in your content.
1. Save the file to the same directory as this script.
1. Execute the script.
