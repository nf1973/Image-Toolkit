from PIL import Image, ImageOps

def resize_image(image, max_size):
    width, height = image.size
    if width > max_size or height > max_size:
        if width > height:
            ratio = max_size / width
            new_size = (max_size, max(1, int(height * ratio)))
        else:
            ratio = max_size / height
            new_size = (max(1, int(width * ratio)), max_size)
        return image.resize(new_size, Image.LANCZOS)
    return image