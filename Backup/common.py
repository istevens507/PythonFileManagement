#######################################################################################
### Purpose: This file contains a class JsonManagement which is used to load, parse, convert and convert list to json.
###  
### Usage: import Common
###
import json

class JsonManagement:
    
    
    def LoadJsonFile(filePath):
        with open(filePath, "r") as f:
            data = json.load(f)
            f.close()
        return data
    
    def ParseJson(data):
        return json.loads(data)
    
    def ConvertToJson(data):
        return json.dumps(data)
    
    def ConvertListToJson(itemList):
        itemDictionary = {index: value.__dict__ for index, value in enumerate(itemList)}
        return json.dumps(itemDictionary)
       

