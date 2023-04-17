from django.core.files import File
from io import BytesIO
from PIL import Image



def image_resize(image, tgt_width):
    img = Image.open(image)
    width, height = img.size
    ratio = width / height
    tgt_height = int(tgt_width / ratio)
    img = img.resize((tgt_width, tgt_height), Image.ANTIALIAS)
    if tgt_height > tgt_width:        
        top = 0
        bottom = tgt_width
        img = img.crop((0, top, tgt_width, bottom))
    img = img.convert('RGB')
    return img