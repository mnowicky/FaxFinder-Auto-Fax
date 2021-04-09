'''
Created on Dec 12, 2018

@author: treusch
'''
import time
import traceback
import os
import re
from Logger import Logger
from faxJob import faxJob
from threading import Thread
import threading

class FolderWatcher(object):
    running=True
    idle=10
    watchFile=""
    faxableFiles=['DOC','DOCX','PDF','PNG','JPG','BMP','JPEG','TIF','TIFF','TXT']
    addLock=threading.Lock()

    def __init__(self, idle,  watchFile):
        self.idle=idle
        self.watchFile = watchFile
    
    def run(self):
        print("FolderWatcher run")
        try:
            while(self.running):
                self.scanFiles()
                time.sleep(self.idle)
        except:
            Logger.writeAndPrintLine("An unexpected error occurred in FolderWatcher, halting: "+traceback.format_exc(),3)  
            
    def scanFiles(self):
        try:
            files = [f for f in os.listdir(self.watchFile) if os.path.isfile(os.path.join(self.watchFile, f))]
        except:
            Logger.writeAndPrintLine("Could not get directory listing for "+self.watchFile+". Sleeping for 5 minutes. "+traceback.format_exc(),3)  
            time.sleep(300)
            return
        filteredFiles=[f for f in files if(f.split('.')[-1].upper() in self.faxableFiles)]
        files=filteredFiles
        for file in files:
            try:
                identifier=re.search('(.+?)[_|\\.]',file,0).group(1)
            except: 
                continue#file name format not valid (no file extension)
            self.addLock.acquire()
            if(not self.isDuplicate(identifier)):
                try:
                    newJob=faxJob(identifier)
                    faxJob.faxJobs.append(newJob)
                    Thread(target=self.waitForMatches, args=(identifier, newJob)).start()
                except:
                    None
            self.addLock.release()
                    
    def isDuplicate(self, identifier):
        isDuplicate=False
        for job in faxJob.faxJobs:
            if(job.uid==identifier):
                isDuplicate=True
                break
        return isDuplicate
            
    def waitForMatches(self, identifier, newJob):
        #give time for accompanying files to appear. 
        time.sleep(20)
        try:
            files = [f for f in os.listdir(self.watchFile) if os.path.isfile(os.path.join(self.watchFile, f))]
        except:
            Logger.writeAndPrintLine("Could not get directory listing for "+self.watchFile,3)  
            return   
        filteredFiles=[f for f in files if(f.split('.')[-1].upper() in self.faxableFiles)]
        matchedFiles=[]
        for file in filteredFiles:
            fullPath=self.watchFile+'\\'+file
            if(re.search('(.+?)[_|\\.]',file,0).group(1)==identifier):
                matchedFiles.append(fullPath)
        
        if(len(matchedFiles)==0):
            return
        newJob.files=matchedFiles
        newJob.status="MATCHED"
        Logger.writeAndPrintLine("Matched files for job "+newJob.uid, 1)
        

                
            
