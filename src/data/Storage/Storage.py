import os, sys, sqlite3
from enum import Enum
sys.path.append(os.getcwd())
from src.data.Storage.Tutor import Tutor
from src.data.Storage.Link import Link
from src.utils.azure_utils import AzureStorage
from src.data.Storage.DataType import DataType

class DataStorage(AzureStorage):
    account_name = "graduationwork3664469496"
    acc_key  = "secret key"
    container_str = "tutors"
    tutors_path = "data\Tutors.db"
    str_to_type_dict = {
        'Video': DataType.Video,
        'Audio': DataType.Audio,
        'Text': DataType.Text,
        'Image': DataType.Image
    }
    type_to_str_dict = {
    DataType.Video: 'Video',
    DataType.Audio: 'Audio',
    DataType.Text: 'Text',
    DataType.Image: 'Image'
}
    def __init__(self):
        super().__init__(DataStorage.account_name,DataStorage.acc_key)
        #self.tutors_db = self.retrieve(DataStorage.container_str,DataStorage.tutors_path)
            
    def getTutorDBCursor(self):
        self.tutor_db_conn = sqlite3.connect(DataStorage.tutors_path)
        return self.tutor_db_conn.cursor()
    
    def getTutor(self,name):
        cursor = self.getTutorDBCursor()
        cursor.execute("SELECT Name FROM Tutor WHERE Name = ?", (name,))
        tutor_data = cursor.fetchone()
        self.tutor_db_conn.close()
        if tutor_data is not None:
            tutor_name = tutor_data[0]
            return Tutor(tutor_name)
        else:
            return None

    def insertTutor(self,tutor: Tutor):
        cursor = self.getTutorDBCursor()
        cursor.execute("INSERT INTO Tutor (Name) VALUES (?)",(tutor.name,))
        self.tutor_db_conn.commit()
        self.tutor_db_conn.close()

    def deleteTutor(self,tutor: Tutor):
        cursor = self.getTutorDBCursor()
        cursor.execute("DELETE FROM Tutor WHERE Name = ?", (tutor.name,))
        self.tutor_db_conn.commit()
        self.tutor_db_conn.close()

    def getLinkDataTypes(self,tutor:Tutor, link :Link):
        cursor = self.getTutorDBCursor()
        cursor.execute("SELECT Type FROM DataType WHERE Tutor_Name = ? AND URL =?",
                        (tutor.name,link.url))
        link_data_types :[DataType] = []
        link_data_types_data = cursor.fetchall()
        for link_data_type_data in link_data_types_data:
             if link_data_type_data is not None:
                 data_type_str = link_data_type_data
                 link_data_types.append(DataStorage.str_to_type_dict[data_type_str[0]])
        self.tutor_db_conn.close()
        return link_data_types

    def getTutorLinks(self,tutor:Tutor):
        cursor = self.getTutorDBCursor()
        cursor.execute("SELECT URL,Website_Name,Info FROM Link WHERE Tutor_Name = ?",
                        (tutor.name,))
        tutor_original_links : [Link] = []
        tutor_original_links_data = cursor.fetchall()
        # getting all original links urls data
        for tutor_link_data in tutor_original_links_data:
            if tutor_link_data is not None:
                url,website_name,info = tutor_link_data
                link = Link(url,website_name,info)
                tutor_original_links.append(link)
        self.tutor_db_conn.close()
        for tutor_original_link in tutor_original_links:
            data_types = self.getLinkDataTypes(tutor,tutor_original_link)
            tutor_original_link.data_types_done = data_types
        return tutor_original_links
    
    def updateLink(self,tutor:Tutor, link :Link):
        tutor_original_links = self.getTutorLinks(tutor)
        orignal_urls = [original_link.url for original_link in tutor_original_links ]
        if (link.url not in orignal_urls):
            self.addLink(tutor,link,tutor_original_links,orignal_urls)
        else :
            cursor = self.getTutorDBCursor()
            for link_data_type in link.data_types_done:
                cursor.execute("INSERT OR IGNORE INTO DataType (URL, Tutor_Name,Type, Done) VALUES (?,?, ?, ?)",
                   (link.url, tutor.name,
                    DataStorage.type_to_str_dict[link_data_type], True))
            self.tutor_db_conn.commit()
            self.tutor_db_conn.close()

    def addLinks(self,tutor:Tutor, links : [Link]):
        tutor_original_links = self.getTutorLinks(tutor)
        orignal_urls = [original_link.url for original_link in tutor_original_links ]
        new_links = [link for link in links if link.url not in orignal_urls]
        # insert new links
        for new_link in new_links:
            self.addLink(tutor,new_link,tutor_original_links,orignal_urls)
        
    def addLink(self,tutor:Tutor, new_link : Link,
                tutor_original_links = [], orignal_urls =[]):
        
        if(tutor_original_links == []):
            tutor_original_links = self.getTutorLinks(tutor)    
        if(orignal_urls == []):
            orignal_urls = [original_link.url for original_link in tutor_original_links]

        if (new_link.url not in orignal_urls):
            cursor = self.getTutorDBCursor()
            cursor.execute("INSERT INTO Link (URL, Tutor_Name,Website_Name,Info) VALUES (?,?, ?, ?)",
                   (new_link.url, tutor.name,new_link.website_name,new_link.info))
            for link_data_type in new_link.data_types_done:
                cursor.execute("INSERT INTO DataType (URL, Tutor_Name,Type, Done) VALUES (?,?, ?, ?)",
                   (new_link.url, tutor.name,
                    DataStorage.type_to_str_dict[link_data_type], True))
            self.tutor_db_conn.commit()
            self.tutor_db_conn.close()
"""
tutor = Tutor("andrewh")
print(tutor.name)
data_storage = DataStorage()
#data_storage.insertTutor(andrew)
link = Link("Test.com/tests","test.com","testing")
#data_storage.addLink(andrew,link)
andrew_test = data_storage.getTutor("andrewh")
print(andrew_test.name)
link.done = True
data_storage.updatelink(tutor,link)
link_test = data_storage.getTutorLinks(andrew_test)[0]
print(link_test.url,link_test.website_name,link_test.info,link_test.done)
"""





        