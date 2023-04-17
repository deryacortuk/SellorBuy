from django.core.files import File
from io import BytesIO
from PIL import Image

def thumnail(image):
    img = Image.open(image)
    img = img.convert("RGB")
    thumbnail_size = (45, 55)
    data_img = BytesIO()
    img.thumbnail(thumbnail_size,Image.ANTIALIAS)
    img.save(data_img, 'JPEG', quality=100, optimize=True) 

    new_image = File(data_img, name=image.name)

    return new_image

def compress(image):
    img = Image.open(image)
    img = img.convert("RGB")

   
    new_size = (900, 1024)  
    img = img.resize(new_size, Image.ANTIALIAS)
    
    
    im_io = BytesIO() 
    img.save(im_io, 'JPEG', quality=100, optimize=True) 

    new_image = File(im_io, name=image.name)

    return new_image
  
def midcompress(image):
    img = Image.open(image)
    img = img.convert("RGB")

   
    new_size = (250, 300)  
    img = img.resize(new_size, Image.ANTIALIAS)
    
    
    im_io = BytesIO() 
    img.save(im_io, 'JPEG', quality=100, optimize=True) 

    new_image = File(im_io, name=image.name)

    return new_image
