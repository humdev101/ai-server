 
import os
 
# get current directory
def getPath():
    path = os.getcwd()
    print("Current Directory", path)
    return path


 
# prints parent directory
# print(os.path.abspath(os.path.join(path, os.pardir)))