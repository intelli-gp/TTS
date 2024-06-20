from pydantic import BaseModel
from scipy.io.wavfile import write
from datetime import datetime, timedelta
from fastapi import FastAPI
from inferencePreprocessing import InferencePreprocessing
from Slide import Slide
from TtsModel import Tts_Model
from AzureStorageSas import AzureStorageSas
import os
from dotenv import load_dotenv

generated_data_path = "app/data/generated/VideoGeneration/"
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
    print(f"Generated Link: {url}")
    # Return file url
    return url

def generate_video_link(slides:list[dict]):
    slides_list = ListSlidesPydantic(slides=[SlidePydantic(title=s['title'],points =s['points'],text =s['text']) for s in slides])
    acc_name = os.getenv("ACC_NAME")
    acc_key = os.getenv("ACC_KEY")
    container_name = os.getenv("CONTAINER_NAME")
    azure_storage_sas = AzureStorageSas(acc_name, acc_key, container_name)
    model = Tts_Model()
    return generate_video(slides_list,azure_storage_sas,model)


if __name__ == "__main__":
    load_dotenv()
    slide1 = {"title":"Introduction", "points":["Point 1", "Point 2"], "text":"This is the introduction slide."}
    slide2 = {"title":"Introduction2", "points":["Point 3", "Point 4"], "text":"This is the introduction slide two."}
    print(generate_video_link([slide1,slide2]))


