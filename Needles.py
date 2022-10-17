from Logger import Logger
import pyodbc

dbUser="" #enter db username
dbPassword="" # enter db pw
dbHost="" #hostname where db lives
dbPort= #port (as numeral)
dbConnection=None

def connectDB():
    try:
        return pyodbc.connect('UID='+dbUser+';PWD='+dbPassword+';DSN='+dbHost)
    except: 
        Logger.writeAndPrintLine("Could not connect specified database.", 3)    
        return False
    return True

def disconnectDB(connection):
    connection.close()
    
def sendMessage(staffcode, recipients, body, casenum, party_id, phonenum):
    dbConnection=connectDB()
    if(dbConnection!=None):
        if(casenum==None):
            casenum="null"
        else:
            casenum="'"+str(casenum)+"'"
        if(party_id==None or party_id=="0" or party_id==0):
            party_id="null"
        else:
            party_id="'"+str(party_id)+"'"
        if(phonenum==None):
            phonenum=""

        sql=("exec WKM_InsertMessage '"+staffcode+"','"+recipients+"','"+body+"',"
                    +str(casenum)+","+str(party_id)+",'"+str(phonenum)+"' commit")
        Logger.writeAndPrintLine("Sending message: "+sql, 1)
        #try:
        cursor=dbConnection.cursor()
        cursor.execute(sql)
        cursor.close()
        disconnectDB(dbConnection)
        return True
        #except:
        #    disconnectDB(dbConnection)
        #    return False
        
        
    
