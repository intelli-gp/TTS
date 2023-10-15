import os, sys

sys.path.append(os.getcwd())

from src.data.Storage.Tutor import Tutor
from src.data.Storage.Link import Link
from src.data.Storage.Storage import DataStorage
from src.data.Storage.DataType import DataType
from abc import ABC, abstractmethod


class Scrapper(ABC):
    data_type_dict = [{DataType.Video: 'Video'}, {DataType.Audio: 'Audio'},
                      {DataType.Text: 'Text'}, {DataType.Image: 'Image'}]

    def __init__(self, tutor: Tutor, link: Link = None, data_types: [DataType] = []):
        self.tutor = tutor
        self.data_types = data_types if len(data_types) > 0 else [DataType.Video,
                                                                  DataType.Audio, DataType.Text, DataType.Image]
        self.tutor_path = "data/" + tutor.name
        self.data_paths = []
        self.data_path_file = self.tutor_path + "/data_path.txt"
        self.links = [link] if (link != None) else []
        self.storage = DataStorage()
        return

    def getNewLinks(self):
        all_links = self.storage.getTutorLinks(self.tutor)
        return all_links
        # return [new_link for new_link in all_links if new_link is False]

    @abstractmethod
    def scrapeData(self):
        pass

    def saveFilePaths(self):
        with open(self.data_path_file, 'w') as file:
            for line in self.data_paths:
                file.write(line + '\n')
