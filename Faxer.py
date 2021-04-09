#!c:\python36\python.exe
import requests
import base64
from Logger import Logger
import time
from http.client import *

#set static variables
coverPage='https://faxfinder.mattar.local/ffws/v1/data/cover_pages/wkm_template.pdf'
ourOrg='William Mattar, P.C.'
ourPhonenum='716-444-4444'
ourFaxnum='716-630-6518'
emailAddr='matthewn@williammattar.com'
sendReceipt="always"

webAddr='https://faxfinder.mattar.local/ffws/v1/ofax/'
user=""
password=""
comments="Attached please find our firm's medical records request along with authorization.\nKindly process.\nThank you." 
emailAddr='matthewn@williammattar.com'

maxRetries=3
tryInterval=180

def getContent(filename):
    i=0
    while(True):
        #for some reason, there are rare issues getting read locks on freshly converted PDFs.
        try:
            myfile=open(filename, 'rb')
            break
        except: 
            Logger.writeAndPrintLine("Couldn't grab read lock on "+filename+". ",2)  
            time.sleep(2)
        i+=1
        if(i>5): 
            raise Exception("Could not get read lock on "+filename+" in a reasonable period of time, aborting.")
    data=myfile.read()
    enc=base64.b64encode(data)
    myfile.close()
    return enc

def getContentTheHardWay(filename):
    myfile=open(filename, 'rb')
    superString=''
    for line in myfile:
        superString+=base64.b64encode(line).decode('ascii')
    return superString

def getContentTheEasyWay(filename):
    myfile=open(filename, 'rb')
    superString=base64.b64encode(myfile.read()).decode('ascii')
    return superString

def prepXMLString(instring):
    outstring=instring.replace('&',"&amp;").replace('<','&lt;').replace('>','&gt;')
    return outstring

def sendFax(destOrg, destFax, cliName, casenum, attachments, errEAddr, comment, destName):
    creds=requests.auth.HTTPBasicAuth(user,password)
    
    #== OVERRIDE OUTBOUND FAX NUMBER FOR TESTING ==
    #destFax='716-631-9804'
    #print("faxes will be sent to "+destFax)
    #return
    #==============================================

    #Fax parameters from hidden fields stored in the allData variable.

    allData=''
    allData+='<schedule_fax>\n'
    
    allData+='<cover_page>\n'
    allData+='<url>'+prepXMLString(coverPage)+'</url>\n'
    allData+='<enabled>true</enabled>\n'
    allData+='<subject>'+prepXMLString(cliName)+' - case # '+str(casenum)+'</subject>\n'
    allData+='<comments>'+prepXMLString(comment)+'</comments>\n'
    allData+='</cover_page>\n'
    
    allData+='<sender>\n'
    allData+='<name>'+prepXMLString(webAddr)+'</name>\n'
    allData+='<organization>'+prepXMLString(ourOrg)+'</organization>\n'
    allData+='<phone_number>'+prepXMLString(ourPhonenum)+'</phone_number>\n'
    allData+='<fax_number>'+prepXMLString(ourFaxnum)+'</fax_number>\n'
    allData+='<email_address>'+prepXMLString(errEAddr)+'</email_address>\n'
    allData+='</sender>\n'
    
    allData+='<recipient>\n'
    allData+='<name>'+prepXMLString(destName)+'</name>\n'
    allData+='<organization>'+prepXMLString(destOrg)+'</organization>\n'
    allData+='<fax_number>'+prepXMLString(destFax)+'</fax_number>\n'
    allData+='</recipient>\n'
    
    for attachment in attachments:
        allData+='<attachment>\n'
        allData+='<location>inline</location>\n'
        allData+='<name>'+prepXMLString(attachment.split('\\')[-1])+'</name>\n'
        #allData+='<content_type>text/plain</content_type>\n'
        allData+='<content_type>application/pdf</content_type>\n'
        allData+='<content_transfer_encoding>base64</content_transfer_encoding>\n'
        allData+='<content>'+getContentTheEasyWay(attachment)+'</content>\n'
        allData+='</attachment>\n'
    
    
    allData+='<max_tries>'+str(maxRetries)+'</max_tries>\n'
    allData+='<try_interval>'+str(tryInterval)+'</try_interval>\n'
    allData+='<receipt>'+sendReceipt+'</receipt>\n'
    allData+='<receipt_attachment>none</receipt_attachment>\n'
    #allData+='<schedule_all_at>none</schedule_all_at>\n'  
    allData+='</schedule_fax>\n'
    

    #Open connection and Pass allData variable to the FF appliance.
    print("sending fax to faxfinder...")
    #input()
    response=requests.post(webAddr,data=allData,auth=creds)
    
    Logger.writeAndPrintLineFile('RESPONSE:',"responses.txt",5) 
    Logger.writeAndPrintLineFile(response.text,"responses.txt",5) 
    #print('RESPONSE:')
    #print(response.text)