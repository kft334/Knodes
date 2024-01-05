from server import PromptServer
from io import BytesIO
from PIL import Image
import numpy as np
import base64

class ImageOutput:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "images": ("IMAGE", {"default": None, "forceInput": True}),
                "text": ("STRING", {"default": None})}
            }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("IMAGE",)

    FUNCTION = "Proc"

    OUTPUT_NODE = True

    CATEGORY = "Knodes"
    
    def Proc(self, images, text = ""):
        outs = []
        for single_image in images:
            img = np.asarray(single_image * 255., dtype=np.uint8)
            img = Image.fromarray(img)
            buffered = BytesIO()
            img.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            outs.append(img_str)

        PromptServer.instance.send_sync("knodes", {"images": outs, "text": text})
        return images

NODE_CLASS_MAPPINGS = {
    "Image(s) To Websocket (Base64)": ImageOutput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)"
}
