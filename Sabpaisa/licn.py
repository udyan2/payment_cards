import sys
def checkp(inp):
    fobj=open("passw.txt","r")
    if inp==fobj.readline():
        "Access Granted"
        return 
    else:
        print("Access Denied: ")
        sys.exit()