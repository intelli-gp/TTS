from datasets import Dataset
from transformers import SpeechT5Processor
from transformers import SpeechT5ForTextToSpeech
from datasets import load_dataset, load_from_disk
import torch
from nemo_text_processing.text_normalization.normalize import Normalizer
from transformers import SpeechT5HifiGan
import os

class Tts_Model():
    # constant sample rate
    SR = 16000
    def __init__(self) -> None:
        self.__load_processor()
        self.__load_model()
        self.__load_data()
        self.__load_speaker_embedding()
        self.__load_normalizer()
        self.__load_vocodor()
        
    def __load_processor(self):
        checkpoint = "microsoft/speecht5_tts"
        self.processor = SpeechT5Processor.from_pretrained(checkpoint)
        
    def __load_model(self):
        # load model from huggingface or local if found
        audio_model_path = 'audio_model'
        if os.path.exists(audio_model_path):
            print("Audio model found")
            self.loaded_model = SpeechT5ForTextToSpeech.from_pretrained('audio_model')
        else:
            print("Audio model not found, fetching from hugging face")
            self.model = SpeechT5ForTextToSpeech.from_pretrained("Nour17/speecht5_finetuned_Andrew_NG_complete")
            self.model.save_pretrained('audio_model')
    
    def __load_data(self):
            # load dataset from huggingface or local if found
        dataset_model_path = 'audio_dataset'
        if os.path.exists(dataset_model_path):
            print("Audio dataset found")
            self.dataset = load_from_disk('audio_dataset')
        else:
            print("Audio dataset not found, fetching from hugging face")
            self.dataset = load_dataset("Nour17/Andrew_NG_audio_dataset")
            self.dataset.save_to_disk('audio_dataset')
    
    def __load_speaker_embedding(self):
            # default speaker embeddings
        example = self.dataset["test"][0]
        self.speaker_embeddings = torch.tensor(example["speaker_embeddings"]).unsqueeze(0)

    def __load_normalizer(self):
        # normalize input text 
        self.normalizer = Normalizer(input_case='cased', lang='en')
    
    def __load_vocodor(self):
        # convert mel-spectogram to audio waveform model (reverse fft phase shift)
        self.vocoder = SpeechT5HifiGan.from_pretrained("microsoft/speecht5_hifigan")