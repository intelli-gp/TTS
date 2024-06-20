from duckduckgo_search import AsyncDDGS,DDGS
import numpy as np
from PIL import Image
import requests
from io import BytesIO
from transformers import CLIPProcessor, CLIPModel

import torch
from sklearn.metrics.pairwise import cosine_similarity

class ImageMatcher:
    def __init__(self):
        self.model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32')
        self.processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32')
        
    def __fetch_image_urls(self,query, max_results = 10):
        query = query
        results = DDGS().images(
            keywords=query,
            region="wt-wt",
            safesearch="on",
            size=None,
            color=None,
            type_image=None,
            layout=None,
            license_image=None,
            max_results=max_results,
        )
        return [img['image'] for img in results]

    def __download_images(self,image_urls):
        images = []
        for url in image_urls:
            try:
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                images.append(img)
            except Exception as e:
                print(f"Failed to download image from {url}: {e}")
        return images

    def __generate_text_embeddings(self,texts):
        inputs = self.processor(text=texts, return_tensors="pt", padding=True, truncation=True)
        text_embeddings = self.model.get_text_features(**inputs)
        return text_embeddings

    def __generate_image_embeddings(self,images):
        inputs = self.processor(images=images, return_tensors="pt")
        image_embeddings = self.model.get_image_features(**inputs)
        return image_embeddings

    def match_best_image(self,query):
        image_urls = self.__fetch_image_urls(query)
        images = self.__download_images(image_urls)
        # Generate embeddings
        text_embeddings = self.__generate_text_embeddings([query])
        print(f"Successfully created text embeddings for: {query}")
        image_embeddings = self.__generate_image_embeddings(images)
        print(f"Successfully created image embeddings for all images")
        # Calculate similarities
        similarities = cosine_similarity(text_embeddings.detach().numpy(), image_embeddings.detach().numpy())
        print(similarities)
        # Find the most similar image
        top_index = similarities.argmax()
        most_relevant_image_conf  = similarities[0][top_index]
        most_relevant_image = images[top_index]
        return most_relevant_image_conf,most_relevant_image