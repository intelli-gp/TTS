
from AzureStorageSas import AzureStorageSas
from fastapi import FastAPI
from TtsModel import Tts_Model
from VideoGeneration import ListSlidesPydantic, generate_video
import nest_asyncio
import uvicorn
import os
from dotenv import load_dotenv
load_dotenv()
if __name__ == "__main__":
    acc_name = os.getenv("ACC_NAME")
    acc_key = os.getenv("ACC_KEY")
    container_name = os.getenv("CONTAINER_NAME")
    azure_storage_sas = AzureStorageSas(acc_name, acc_key, container_name)
    app_name = os.getenv("APP_NAME")
    app = FastAPI(title=app_name)
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