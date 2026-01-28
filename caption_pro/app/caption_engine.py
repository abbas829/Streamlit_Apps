from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import torch

class CaptionEngine:
    def __init__(self, model_name="Salesforce/blip-image-captioning-large"):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name).to(self.device)

    def generate(self, image: Image.Image, prompt: str = None, max_len: int = 50, beams: int = 5):
        if prompt:
            inputs = self.processor(image, prompt, return_tensors="pt").to(self.device)
        else:
            inputs = self.processor(image, return_tensors="pt").to(self.device)
        out = self.model.generate(**inputs, max_length=max_len, num_beams=beams)
        return self.processor.decode(out[0], skip_special_tokens=True)