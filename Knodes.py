from server import PromptServer
from io import BytesIO
from PIL import Image
import numpy as np
import base64
import torch
import json

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
        return {"required": {"image": ("STRING", {"multiline": False})}}

    RETURN_TYPES = ("IMAGE", "MASK")
    CATEGORY = "Knodes"

    FUNCTION = "Proc"

    def Proc(self, image):
        imgdata = base64.b64decode(image)
        img = Image.open(BytesIO(imgdata))

        if "A" in img.getbands():
            mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
            mask = 1.0 - torch.from_numpy(mask)
        else:
            mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")

        img = img.convert("RGB")
        img = np.array(img).astype(np.float32) / 255.0
        img = torch.from_numpy(img)[None,]

        return (img, mask)

class LoadImagesBase64:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"strings": ("STRING", {"multiline": False})}}

    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "Knodes"

    FUNCTION = "Proc"

    def Proc(self, strings):
        
        # Pop the number of images from the string
        number_of_images = int(strings[:4].lstrip('0'), 16)
        print("Number Of Images: " + str(number_of_images))
        strings = strings[4:]

        images = []
        
        # Structure of the rest of the string: 0xXXXXXXXX (int64) Base64 (string) with 0xXXXXXXXX being the length of the string... repeat number_of_images times
        for i in range(number_of_images):
            length = int(strings[:8].lstrip('0'), 16)
            print("Image #" + str(i) + " Length: " + str(length))
            strings = strings[8:]
            single_image = strings[:length]
            strings = strings[length:]
            images.append(single_image)

        tensors = []

        for single_image in images:
            imgdata = base64.b64decode(single_image)
            img = Image.open(BytesIO(imgdata))

            img = img.convert("RGB")
            img = np.array(img).astype(np.float32) / 255.0
            img = torch.from_numpy(img)[None,]

            # shape is [5, 1, 640, 640, 3] = [n, ?, h, w, c] ... n = number of images, h = height, w = width, c = channels.
            
            tensors.append(img)

        tensors = [img.squeeze(0) for img in tensors]

        return (tensors,)
        
NODE_CLASS_MAPPINGS = {
    "Image(s) To Websocket (Base64)": ImageOutput,
    "Load Image From Websocket (Base64)": LoadImageBase64,
    "Load Images From Websocket (Base64)": LoadImagesBase64
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)",
    "LoadImageBase64": "Load Image From Websocket (Base64)",
    "LoadImageBase64": "Load Images From Websocket (Base64)"
}
