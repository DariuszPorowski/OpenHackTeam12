from io import BytesIO
from PIL import Image

def file_to_image(file):
    memory = BytesIO()
    file.save(memory)
    memory.seek(0)
    return Image.open(memory)