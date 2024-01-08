from .Knodes import ImageOutput
from .Knodes import LoadImageBase64
from .Knodes import LoadImagesBase64

NODE_CLASS_MAPPINGS = {
    "ImageOutput": ImageOutput,
    "Load Image From Websocket (Base64)": LoadImageBase64,
    "Load Images From Websocket (Base64)": LoadImagesBase64
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)",
    "LoadImageBase64": "Load Image From Websocket (Base64)",
    "LoadImagesBase64": "Load Images From Websocket (Base64)"
    }

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
