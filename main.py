import io
import pytesseract
from PIL import Image
import requests
import re

from cards.aadhaar import Aadhaar

# response = requests.get('https://haptikappimg.haptikapi.com/uploads/b61e9f97a524696e2815f8e27f41f62e.jpeg')

# img = Image.open(io.BytesIO(response.content))
img_data = pytesseract.image_to_string('/Users/santhoshreddy/Downloads/aadharsindhu.jpeg', lang='eng')

aadhaar_data = Aadhaar(img_data).front_aadhar_data()

print("Aadhaar data:: ", aadhaar_data)
