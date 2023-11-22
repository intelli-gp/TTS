import sys,os
sys.path.append(os.getcwd())
from src.data.Storage.DataType import DataType

class Link(object):
    def __init__(self, url, website_name= None,info = None,done = False,
                 data_types_done : [DataType] = []):
        self.url = url
        self.website_name = website_name
        self.info = info
        self.data_types_done = data_types_done
    
    def isDataTypeDone(self,data_type:DataType)-> bool:
        return data_type in self.data_types_done
    
    def addDataType(self,data_type:DataType):
        if(data_type not in self.data_types_done):
            self.data_types_done.append(data_type)



