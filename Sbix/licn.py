import sys
import getpass
usern=getpass.getuser()

def checkp(inp):
    fobj=open("passw.txt","r")
    if inp==fobj.readline():
        "Access Granted"
        return 
    else:
        print("Access Denied: ")
        sys.exit()
