ComfyUI Nodes

3 Nodes:

- Image(s) to Websocket (Base64)
-- Accepts images and returns base64 images using the websocket. Optionally returns a tag for routing.

- Load Image (Base64)
-- Accepts a base64 encoded image and returns a tensor.

- Load Images (Base64)
-- Accepts a string with the following structure:
--- 0xffff (Image count)
--- 0xffffffff (Image1 length)
--- Image1 (base64)
--- ...
--- ...
--- 0xffffffff (ImageN length)
--- ImageN (base64)
-- Returns tensors for all the images.
