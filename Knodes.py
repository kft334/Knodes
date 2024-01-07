from server import PromptServer
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import torch

class ImageOutput:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"default": None, "forceInput": True}),
                "tag": ("STRING", {"default": None})}
            }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    FUNCTION = "Proc"

    OUTPUT_NODE = True

    CATEGORY = "Knodes"
    
    def Proc(self, images, tag = ""):
        outs = []

        for single_image in images:
            img = np.asarray(single_image * 255., dtype=np.uint8)
            img = Image.fromarray(img)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            outs.append(img_str)

        PromptServer.instance.send_sync("knodes", {"images": outs, "text": tag})

        return (images,)
    
class LoadImageBase64:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
            "image": ("STRING", {"multiline": False})}
            }

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Knodes"
    FUNCTION = "Proc"

    def Proc(self, image):

        # image is a base64 encoded JObject.

        jObject = base64.b64decode(image)

        # jObject is a JObject with the following structure: [image, image, ...]
        # where each image is a base64 encoded string.

        images = []

        for single_image in jObject:
            imgdata = base64.b64decode(single_image)
            img = Image.open(BytesIO(imgdata))

            img = img.convert("RGB")
            img = np.array(img).astype(np.float32) / 255.0
            img = torch.from_numpy(img)[None,]

            images.append(img)

        return (images,)
        
NODE_CLASS_MAPPINGS = {
    "Image(s) To Websocket (Base64)": ImageOutput,
    "Load Image(s) From Websocket (Base64)": LoadImageBase64
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)",
    "LoadImageBase64": "Load Image(s) From Websocket (Base64)"
}
