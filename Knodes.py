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
                "Actions": ("STRING", {"default": None})}
            }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    FUNCTION = "Proc"

    OUTPUT_NODE = True

    CATEGORY = "Knodes"
    
    def Proc(self, images, Actions = ""):
        outs = []

        for single_image in images:
            img = np.asarray(single_image * 255., dtype=np.uint8)
            img = Image.fromarray(img)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            outs.append(img_str)

        PromptServer.instance.send_sync("knodes", {"images": outs, "Actions": Actions})

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

    RETURN_TYPES = ("IMAGE","MASK")
    CATEGORY = "Knodes"

    FUNCTION = "Proc"

    def Proc(self, strings):
        number_of_images = int(strings[:4].lstrip('0'), 16)
        print("Number Of Images: " + str(number_of_images))
        strings = strings[4:]

        images = list()
        
        for i in range(number_of_images):
            length = int(strings[:8].lstrip('0'), 16)
            print("Image #" + str(i) + " Length: " + str(length))
            strings = strings[8:]
            single_image = strings[:length]
            strings = strings[length:]
            images.append(single_image)

        tensors = list()
        masks = list()

        for single_image in images:
            imgdata = base64.b64decode(single_image)
            img = Image.open(BytesIO(imgdata))

            if "A" in img.getbands():
                mask = np.array(img.getchannel("A")).astype(np.float32) / 255.0
                mask = 1.0 - torch.from_numpy(mask)
                masks.append(mask)
            else:
                mask = torch.zeros((64, 64), dtype=torch.float32, device="cpu")
                masks.append(mask)

            img = img.convert("RGB")
            img = np.array(img).astype(np.float32) / 255.0
            img = torch.from_numpy(img)[None,]

            tensors.append(img)

        return (torch.cat(tensors), torch.cat(masks))
    
NODE_CLASS_MAPPINGS = {
    "Image(s) To Websocket (Base64)": ImageOutput,
    "Load Image (Base64)": LoadImageBase64,
    "Load Images (Base64)": LoadImagesBase64
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)",
    "LoadImageBase64": "Load Image (Base64)",
    "LoadImageBase64": "Load Images (Base64)"
}
