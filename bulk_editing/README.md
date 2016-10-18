####[mdBulkEdit.py](https://github.com/Esri/arcgis-admin-python-scripts/blob/metaDataBulkEdit/bulk_editing/mdBulkEdit.py)
This script performs multiple functions, based on the flag an admin passes to it. If you're running this script for the first time, you have to use the optional `-c` flag to generate the file `metaDataTable.csv` which is the csv of the metadata for the items you want to edit. If the script is unable access the metadata for any item, it will post a message to the screen that this is the case, generate its own basic metadata and then upload that to AGOL, to seed in ability to access and edit more robust metadata for that item. IF this is the case, you will then have to run the script again, with the same `-c` flag so that it can now incorporate the AGOL items you couldn't access before. Once you've run the script to generate the necessary csv, you can then edit the fields of that csv as needed. When you're ready to push those changes to online, run the script again, but this time with the `-m` flag.

### __Currently this script only works with the ISO 19139 Metadata Implementation Specification__

flags script accepts:
  * `-a` this flag specifies sets the GIS you want to administer __[required]__    
  * `-u` this flag sets the username to log in with __[required]__    
  * `-p` this flag sets the password associated with the username __[required]__ 
  * `-c` is the optional flag used have the script generate a csv of all your public, open data items.__[optional]__
  * `-m` is the optional flag used to have the script build valid xml metadata files from the csv you generated with the `-c` flag.__[optional]__

##Examples
 * `python3 mdBulkEdit.py -u <username> -p <password> -a http://www.arcgis.com -c`

 * `python3 mdBulkEdit.py -u <username> -p <password> -a http://www.arcgis.com -m`


 1. Clone the repo or copy the code from the script and save it to a `.py` file on your local system.

 1. Run the script with the `-c` as shown above, to have the script generate a csv of your public items. 
 		* Depending on what the script finds, it may instruct you to run it again with the `-c` flag a second time.
 		* This will also generate other files that the script needs to run properly. This is inludes a directory named 'downloaded' and metadata files for each item in the csv file. These  are essentially temporary files and can be deleted once the script has finished generating the csv.
 1. Edit the fields in the csv as needed, being careful to never manually edit the mdFileID field ever.
 	* resTitle = Title
 	* useLimit = License
 	* key word = tags
 	* idAbs = description
 1. Save your edited csv in the same directory as the script.
 1. When you're ready to push your edits to your online account, run the script again, but this time with the `-m` flag.
 1. Once the script is finished, confirm that the changes you made are reflected in your online items.


| __Category__ | __Value__ | __Role__ | __Value__ | __Update Frequency__| __Value__|                                   
|----------  |---------|-----------|-------------|---------|-----------|                    
|Farming     | 001     |Resource Provider| 001|Daily    | 001|
|Biota       | 002     |Custodian| 002     |Weekly      | 002     |
|Boundaries  | 003     |Owner    | 003     |Fortnightly | 003     |
|Atmospheric Sciences| 004|User  | 004     |Monthly     | 004     |
|Economy     | 005     |Distributor| 005   |Quarterly   | 005     |
|Elevation   | 006     |Originator | 006   |Biannually  | 006     |
|Environment | 007     |Point of Contact| 007|Annually  | 007     |
|Geoscientific| 008    |Principal Investigator| 008   |As Needed  | 008|
|Health      | 009     |Processor  |009    |Irregular   | 009     |
|Imagery and Basemaps| 010|Publisher  | 010   |Not Planned | 010|
|Military Intelligence| 011|Author    | 011   |Unknown  | 011|
|Inland Waters| 012    |
|Locations   | 013     |
|Oceans      | 014     |
|Planning & Cadastral| 015|
|Society     | 016     |
|Structure   | 017     |
|Transportation| 018   |
|Utilities and Communications| 019|

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
