
from TtsModel import Tts_Model
import numpy as np


class InferencePreprocessing:
    def __init__(self,model:Tts_Model) -> None:
        self.model = model
    # get sentences and add period at the end of each one
    def __get_sentences(self,text, add_period = True):
        period = "." if add_period else ""
        sentences = [sent + period for sent in text.split(".")]
        # remove last period if it exsists and add_period flag is True
        if sentences[-1] == period : sentences = sentences[:-1]
        return sentences

    # divide large text into sentences chunks
    def __chunk_text(self,text, max_length = 400):
        sentences = self.__get_sentences(text)
        chunks = [[]]
        chunks_idx = 0
        curr_length = 0
        for sent in sentences:
            curr_length += len(sent)
            if (curr_length < max_length):
                chunks[chunks_idx].append(sent)
            else:
                chunks.append([sent])
                chunks_idx += 1
                curr_length = len(sent)
        return chunks

    def __prepare_sentences(self,sentences):
        sentences = self.model.normalizer.normalize_list(sentences)
        inputs = self.model.processor(text=sentences,is_split_into_words=True, return_tensors="pt")
        return inputs

    def __generate_single_speech(self,text):
        if type(text) == list :
            inputs = self.__prepare_sentences(text)
            speech_tensor = self.model.generate_speech(inputs["input_ids"],
                                                        self.model.speaker_embeddings, vocoder=self.model.vocoder)
        elif type(text) == str :
            sentences = self.__get_sentences(text)
            print(sentences)
            inputs = self.model.processor(text=self.model.normalizer.normalize(sentences[0]),
                                return_tensors="pt") if len(sentences) == 1 else self.__prepare_sentences(sentences)
        speech_tensor = self.model.generate_speech(inputs["input_ids"], self.model.speaker_embeddings,
                                              vocoder=self.model.vocoder)
        return speech_tensor.numpy()

    def generate_speech(self,text: str):
        transcripts = self.__chunk_text(text)
        speech_tensor_list = []
        for transcript in transcripts:
            print(transcript)
            speech_tensor_list.append(self.__generate_single_speech(transcript))
        return np.concatenate(speech_tensor_list)