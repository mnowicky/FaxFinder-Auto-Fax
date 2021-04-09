'''
Created on Dec 4, 2018

@author: treusch
'''
import configparser
from Logger import Logger
import Faxer
from FolderWatcher import FolderWatcher
from threading import Thread
from JobHandler import JobHandler
import os

class Loader(object):
    
    #config obj
    config = None
    configFileName="AutoFaxer.config"
    
    #global
    runOnce=False
    idle=10
    errorStaff=''
    delOrMoveCompleted=''
    moveFolder="sent"
    storeToDW=True
    libreEXE=""
    
    #watchfolder
    watchfolder=""
    failedFolder="failed"
    
    #fax finder
    webAddr=""
    username=""
    password=""
    maxRetries=3
    tryInterval=60
    sendReceipt="always"
    
    #fax template
    coverPage=""
    faxOrg="William Mattar, P.C."
    faxOrgPhone="716-444-4444"
    faxPhone="716-631-9804"
    emailAddr="trevor@williammattar.com"
    
    #operational
    folderWatcher=None
    folderWatcherThread=None
    jobHandler=None
    jobHandlerThread=None

    def __init__(self):
        self.config = configparser.ConfigParser()
        
    def loadConfig(self):
        self.config.read(self.configFileName)
        
        #global configuration
        self.runOnce = bool(self.config['DEFAULT']['runOnce'])
        self.idle = int(self.config['DEFAULT']['idle'])
        
        #other configuration
        self.errorStaff = self.config['OTHER']['errorStaff']
        self.delOrMoveCompleted = self.config['OTHER']['delOrMoveCompleted']
        self.moveFolder = self.config['OTHER']['moveFolder']
        self.storeToDW = bool(self.config['OTHER']['storeToDW'])
        self.libreEXE = self.config['OTHER']['libreEXE']
        
        #watchfolder configuration
        self.watchfolder=self.config['WATCHFOLDER']['watchfolder']
        self.failedFolder=self.config['WATCHFOLDER']['failedFolder']
        
        #faxfinder configuration
        self.ffWebaddr = self.config['FAXFINDER']['ffWebaddr']
        self.ffUser = self.config['FAXFINDER']['ffUser']
        self.ffPass = self.config['FAXFINDER']['ffPass']
        self.maxRetries = int(self.config['FAXFINDER']['maxRetries'])
        self.tryInterval = int(self.config['FAXFINDER']['tryInterval'])
        self.sendReceipt = self.config['FAXFINDER']['sendReceipt']
        
        #fax configuration
        self.coverPage = self.config['FAXFINDER']['coverPage']
        self.faxOrg = self.config['FAXFINDER']['faxOrg']
        self.faxOrgPhone = self.config['FAXFINDER']['faxOrgPhone']
        self.faxPhone = self.config['FAXFINDER']['faxPhone']
        self.emailAddr = self.config['FAXFINDER']['emailAddr']
        
    def printConfig(self):
        print("DEFAULT: ")
        print("runOnce: "+str(self.runOnce))
        print("idle: "+str(self.idle))
        print("errorStaff: "+str(self.errorStaff))
        print("")
        print("OTHER: ")
        print("errorStaff: "+str(self.errorStaff))
        print("delOrMoveCompleted: "+str(self.delOrMoveCompleted))
        print("moveFolder: "+str(self.moveFolder))
        print("storeToDW: "+str(self.storeToDW))
        print("libreEXE: "+str(self.libreEXE))
        print("")
        print("WATCHFOLDER: ")
        print("watchfolder: "+self.watchfolder)
        print("failedFolder: "+self.failedFolder)
        print("")
        print("FAXFINDER: ")
        print("ffWebAddr: "+self.ffWebaddr)
        print("ffUser: "+self.ffUser)
        print("ffPass: "+self.ffPass)
        print("maxRetries: "+str(self.maxRetries))
        print("tryInterval: "+str(self.tryInterval))
        print("sendReceipt: "+str(self.sendReceipt))
        print("coverPage: "+self.coverPage)
        print("faxOrg: "+self.faxOrg)
        print("faxOrgPhone: "+self.faxOrgPhone)
        print("faxPhone: "+self.faxPhone)
        print("emailAddr: "+self.emailAddr)
        print("")
        
    def launch(self):
        Logger.writeAndPrintLine("Program started.", 0)
        self.loadConfig()
        print("Launching AutoFaxer with the following parameters! :")
        self.printConfig()
        
        self.initFaxer()
        
        if(self.delOrMoveCompleted=="MOVE" and not os.path.exists(self.moveFolder)):
            os.mkdir(self.moveFolder)
        
        self.folderWatcher=FolderWatcher(self.idle, self.watchfolder)
        self.folderWatcherThread=Thread(target = self.folderWatcher.run)
        self.folderWatcherThread.start()
        
        self.jobHandler=JobHandler(self.idle, self.watchfolder, self.delOrMoveCompleted, 
                                   self.moveFolder, self.storeToDW, self.libreEXE, self.failedFolder)
        self.jobHandlerThread=Thread(target = self.jobHandler.run)
        self.jobHandlerThread.start()
        
        
    def initFaxer(self):
        Faxer.coverPage=self.coverPage
        Faxer.ourOrg=self.faxOrg
        Faxer.ourPhonenum=self.faxOrgPhone
        Faxer.ourFaxnum=self.faxPhone
        Faxer.emailAddr=self.emailAddr
        Faxer.webAddr=self.ffWebaddr
        Faxer.user=self.ffUser
        Faxer.password=self.ffPass
        Faxer.maxRetries=self.maxRetries
        Faxer.tryInterval=self.tryInterval
        Faxer.sendReceipt=self.sendReceipt
        
        
        
        