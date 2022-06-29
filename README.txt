To use with your own FaxFinder appliance:

1) Modify launcher.bat
2) Modify Faxer.py static variables to point to your own appliance and creds.
3) Set watchfolder in Loader.py, change fax template vars to match your company/personal info.
4) Needles.py is optional; uses pyodbc to connect to Needles 5.x (and older) version CMS for notification of successful send.
5) Emailer.py sends email notifications of successful sent faxes- currently setup to work with O365/Hosted Exchange, but easily modifyable to work with your email provider. 

Understand that this tool was built for in-house use in a specific proprietary environment. It has not been tested outside of this environment, so additional 
modifications may be required. If nothing else, I share this code as an example of how an automatic-faxing utility can be built to interoperate with a physical faxing appliance (FaxFinder). 
