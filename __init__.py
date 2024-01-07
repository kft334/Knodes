from .Knodes import ImageOutput
from .Knodes import LoadImageBase64

NODE_CLASS_MAPPINGS = {
    "ImageOutput": ImageOutput,
    "Load Image(s) From Websocket (Base64)": LoadImageBase64
    }

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageOutput": "Image(s) To Websocket (Base64)",
    "LoadImageBase64": "Load Image(s) From Websocket (Base64)"
    }

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
