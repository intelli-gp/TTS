from pytube import YouTube
from pytube import Playlist

import os, sys
sys.path.append(os.getcwd())

from src.data.Scrapper.Scrapper import Scrapper
from src.data.Storage.Tutor import Tutor
from src.data.Storage.Storage import DataStorage
from src.data.Storage.DataType import DataType
from src.data.Storage.Link import Link


class YouTubeScrapper(Scrapper):

    def __init__(self,tutor: Tutor, link: Link = None,data_types: [DataType] = []):
        super().__init__(tutor,link,data_types)
        
        self.tutor_path += "/raw"

    def printMsg(self,str,audio_only):
        msg = 'Downloading ' + str
        msg = msg + " Video" if audio_only is False else msg + " Audio"
        print(msg)
    
    def addPath(self,outputDir,title, audio_only):
        path = outputDir + "/" + title+ ".mp4"
        self.data_paths.append(path)
        self.printPath(path,audio_only)

    def printPath(self,path,audio_only):
        msg = f" Video downloaded to {path}" if audio_only is False else f" Audio downloaded to {path}"
        print(msg)

    def downloadVideo(self,url,output_path, audio_only = False):
        self.printMsg('Single',audio_only)
        yt = YouTube(url)
        if audio_only:
            audio_stream = yt.streams.filter(only_audio=True).first()
            audio_stream.download(output_path=output_path)
            self.addPath(output_path,audio_stream.title,audio_only)
        else:
            video_stream = yt.streams.get_highest_resolution()
            video_stream.download(output_path=output_path)
            self.addPath(output_path,video_stream.title,audio_only)

    def DownloadPlaylist(self, url, output_path, audio_only=False):
        self.printMsg('Playlist',audio_only)
        playlist = Playlist(url)
        
        for i,video in enumerate(playlist.videos):
            print(f'Downloading: {video.title}')
            if audio_only:
                audio_stream = video.streams.filter(only_audio=True).first()
                audio_stream.download(output_path=output_path)
                self.addPath(output_path,audio_stream.title,audio_only)
            else:
                video_stream = video.streams.get_highest_resolution()
                video_stream.download(output_path=output_path)
                self.addPath(output_path,video_stream.title,audio_only)
            print(f'{i}/{len(playlist.videos)} downloaded')

        print('Playlist Download completed!')

    def scrapeData(self):
        links = self.links if(len(self.links) > 0) else self.getNewLinks()
        print(len(links))
        for link in links:
            if(link.website_name == "Youtube"):
                if(DataType.Audio in self.data_types and not link.isDataTypeDone(DataType.Audio)):
                    output_dir = self.tutor_path + '/Audio'
                    if(link.info == "Single"):
                        self.downloadVideo(link.url,output_dir,audio_only=True)
                    elif(link.info == "Playlist") :
                        self.DownloadPlaylist(link.url,output_dir,audio_only=True)
                    link.addDataType(DataType.Audio)
                    self.storage.updateLink(self.tutor,link)
                if(DataType.Video in self.data_types and not link.isDataTypeDone(DataType.Video)):
                    output_dir = self.tutor_path + '/Video'
                    if(link.info == "Single"):
                        self.downloadVideo(link.url,output_dir,audio_only=False)
                    elif(link.info == "Playlist") :
                        self.DownloadPlaylist(link.url,output_dir,audio_only=False)
                    link.addDataType(DataType.Video)
                    self.storage.updateLink(self.tutor,link)

