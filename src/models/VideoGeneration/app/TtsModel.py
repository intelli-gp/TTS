from datasets import Dataset
from transformers import SpeechT5Processor
from transformers import SpeechT5ForTextToSpeech
from datasets import load_dataset, load_from_disk
import torch
from nemo_text_processing.text_normalization.normalize import Normalizer
from transformers import SpeechT5HifiGan
import os
import pickle 

class Tts_Model():
    # constant sample rate
    SR = 16000
    data_path = 'app/data/processed/Tts model/'

    def __init__(self) -> None:
        self.__load_processor()
        self.__load_model()
        #self.__load_data()
        self.__load_speaker_embedding()
        self.__load_normalizer()
        self.__load_vocodor()
        if not os.path.exists(Tts_Model.data_path):
            print(f"The tts model data path: {Tts_Model.data_path} isn't valid")
        
    def __load_processor(self):
        checkpoint = "microsoft/speecht5_tts"
        self.processor = SpeechT5Processor.from_pretrained(checkpoint)
        
    def __load_model(self):
        # load model from huggingface or local if found
        audio_model_path = Tts_Model.data_path + 'audio_model'
        if os.path.exists(audio_model_path):
            print("Audio model found")
            self.model = SpeechT5ForTextToSpeech.from_pretrained(audio_model_path)
        else:
            print("Audio model not found, fetching from hugging face")
            self.model = SpeechT5ForTextToSpeech.from_pretrained("Nour17/speecht5_finetuned_Andrew_NG_complete")
            self.model.save_pretrained(audio_model_path)
    
    def __load_data(self):
            # load dataset from huggingface or local if found
        dataset_model_path = Tts_Model.data_path + 'audio_dataset'
        if os.path.exists(dataset_model_path):
            print("Audio dataset found")
            self.dataset = load_from_disk(dataset_model_path)
        else:
            print("Audio dataset not found, fetching from hugging face")
            self.dataset = load_dataset("Nour17/Andrew_NG_audio_dataset")
            self.dataset.save_to_disk(dataset_model_path)
    
    def __load_speaker_embedding(self):
        speaker_embeddings_path = Tts_Model.data_path + 'speaker_embeddings.pt'
        self.speaker_embeddings = torch.load(speaker_embeddings_path)

    def __load_normalizer(self):
        normalizer_path = Tts_Model.data_path +"normalizer.pkl"
        if os.path.exists(normalizer_path):
            print("normalizer found")   
            with open(normalizer_path, "rb") as f:
                #self.normalizer = Normalizer(input_case='cased', lang='en')
                self.normalizer = pickle.load(f)
        else:
            print("Normalizer not found")
            self.normalizer = Normalizer(input_case='cased', lang='en')
            with open(normalizer_path, "wb") as f:
                pickle.dump(self.normalizer,f)
    
    def __load_vocodor(self):
        # convert mel-spectogram to audio waveform model (reverse fft phase shift)
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")