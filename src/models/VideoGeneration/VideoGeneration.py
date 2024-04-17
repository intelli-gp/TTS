from pydantic import BaseModel
from scipy.io.wavfile import write
from datetime import datetime, timedelta
from fastapi import FastAPI
from inferencePreprocessing import InferencePreprocessing
from Slide import Slide
from TtsModel import Tts_Model
from AzureStorageSas import AzureStorageSas
import os
import uvicorn
import nest_asyncio

generated_data_path = "data/generated/VideoGeneration/"
if not os.path.exists(generated_data_path):
    os.makedirs(generated_data_path)

class SlidePydantic(BaseModel):
    title: str
    points: list[str]
    text: str

class ListSlidesPydantic (BaseModel):
    slides: list[SlidePydantic]
    def __iter__(self):
        return iter(self.slides)

    def __getitem__(self, item):
        return self.slides[item]

def generate_video(slides:ListSlidesPydantic,azure_storage_sas,model):
    curr_time = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") 
    curr_generated_data_path =  generated_data_path + curr_time + "/"
    os.makedirs(curr_generated_data_path)
    inference_preprocessing = InferencePreprocessing(model)
    generated_slides = []
    i = 1
    for slide in slides:
        #generate speech
        speech = inference_preprocessing.generate_speech(slide.text)
        filepath = curr_generated_data_path+f'slide {i}.wav'
        i = i +1
        write(filepath, Tts_Model.SR, speech)
        # generate slides
        slide = Slide(slide.title,slide.points,speech,filepath)
        generated_slides.append(slide)
    video_path = curr_generated_data_path + "output_video.mp4"
    Slide.generate_video_from_slides(generated_slides,video_path)
    # create blob and store it on azure
    blob_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + video_path
    azure_storage_sas.store(azure_storage_sas.container_name,blob_name,video_path)
    # get sas for blob for public access
    blob = azure_storage_sas.get_blob_sas(azure_storage_sas.container_name, blob_name)
    url = 'https://'+azure_storage_sas.account_name+'.blob.core.windows.net/'+azure_storage_sas.container_name+'/'+blob_name+'?'+blob
    # Return file url
    return url


class EndPoints():
    app = FastAPI(title='TTS_model')
    def __init__(self,azure_storage_sas: AzureStorageSas):
        self.azure_storage_sas = azure_storage_sas
        self.model = Tts_Model()
    @app.get("/")
    def root():
        return {"message": "Hello World"}
    # post tts model endpoint
    @app.post("/tts") 
    def generate_video(self,slides:ListSlidesPydantic):
        generate_video(slides,self.azure_storage_sas,self.model)

def spin_server(endpoints):
    nest_asyncio.apply()
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"
    uvicorn.run(endpoints.app , host=host, port=8000)

if __name__ == "__main__":
    acc_name = "graduationproject19024"
    acc_key = "l6cWAFptkSjT9EI033DehgiVbVXojBFF89mAN+JN8ibNGk3jhB/TComT+FEf+w3YvuQoWSu7TGbT+AStQWWNZg=="
    container_name = "videos"
    azure_storage_sas = AzureStorageSas(acc_name, acc_key, container_name)
    slide1 = SlidePydantic(title="Introduction", points=["Point 1", "Point 2"], text="This is the introduction slide.")
    slides_list = ListSlidesPydantic(slides=[slide1])
    print(generate_video(slides_list,azure_storage_sas,Tts_Model()))


