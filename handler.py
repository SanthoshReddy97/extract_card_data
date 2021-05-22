import io
import pytesseract
from PIL import Image
import requests
import logging
import pdf2image
from cards.aadhaar import Aadhaar
from cards.pan import Pan


class CardHandler:

    def __init__(self, request_body):
        self.request_body = request_body
        self.response = ""
        self.extracted_data = ""

    def extract_card_data(self):

        self.response = self.get_image_data()
        if self.response in ["Timeout Error", "API Error"]:
            return self.response
        mime_type = self.response.headers['content-type']
        logging.debug("Mime type of the document {}".format(mime_type))
        if mime_type in ['image/jpg', 'image/jpeg', 'image/png']:
            self.extracted_data = self.extract_image_to_string()
        elif mime_type in 'application/pdf':
            self.extracted_data = self.extract_document_to_string()
        else:
            return f"{mime_type} does not match, upload only image or application/pdf."
        parsed_data = self.parse_string_data()
        return parsed_data

    def get_image_data(self):
        """
            Using requests library we call the url received and return the raw binary image data
            received from the url
        """
        url = self.request_body.get('url')
        try:
            response = requests.get(url, timeout=25)
            return response
        except requests.exceptions.Timeout as err:
            logging.exception("Timeout error url:: {} Error: {}".format(url, err))
            return "Timeout Error"
        except requests.exceptions.HTTPError as err:
            logging.exception("API error url::{} Error:{}".format(url, err))
            return "API ERROR"

    def extract_image_to_string(self):
        """
            Extracts string from image using pytesser
        """
        img_raw_data = Image.open(io.BytesIO(self.response.content))
        image_data = pytesseract.image_to_string(img_raw_data, lang='eng')
        return image_data

    def extract_document_to_string(self):
        """
            Extracts string from document
        """
        document = pdf2image.convert_from_bytes(self.response.content)
        document_data = pytesseract.image_to_string(document[0], lang='eng')
        return document_data

    def parse_string_data(self):
        """
            Parse the image string
        """
        if self.request_body.get('type') == 'aadhaar':
            card_data = Aadhaar(self.extracted_data).front_aadhaar_data()
        elif self.request_body.get('type') == 'pan':
            card_data = Pan(self.extracted_data).get_pan_details()
        else:
            card_data = {
                'error': 'No card found, please send the correct type of your card'
            }
        return card_data
