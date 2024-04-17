
from AzureStorageSas import AzureStorageSas
from fastapi import FastAPI
from TtsModel import Tts_Model
from VideoGeneration import ListSlidesPydantic, generate_video
import nest_asyncio
import uvicorn
import os
if __name__ == "__main__":
    acc_name = "graduationproject19024"
    acc_key = "l6cWAFptkSjT9EI033DehgiVbVXojBFF89mAN+JN8ibNGk3jhB/TComT+FEf+w3YvuQoWSu7TGbT+AStQWWNZg=="
    container_name = "videos"
    azure_storage_sas = AzureStorageSas(acc_name, acc_key, container_name)
    app = FastAPI(title='TTS_model')
    model = Tts_Model()
    @app.get("/")
    def root():
        return {"message": "TTs Model default page"}
    # post tts model endpoint
    @app.post("/tts") 
    def tts_generate_video(slides:ListSlidesPydantic):
        return generate_video(slides,azure_storage_sas,model)
    nest_asyncio.apply()
    host = "0.0.0.0" if os.getenv("DOCKER-SETUP") else "127.0.0.1"
    uvicorn.run(app , host=host, port=8000)