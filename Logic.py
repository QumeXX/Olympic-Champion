import pytesseract
from PIL import Image, ImageGrab

def text_response():
    img = Image.open('img.png')
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    txt = pytesseract.image_to_string(img, lang='rus+equ')
    return txt
