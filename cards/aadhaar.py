import re


class Aadhaar:
    """
        Extracts Aadhaar data of user from the extracted string of the image.
        -> Here we are using 're' library to search for the keys we needed.
        -> Printing the errors if we don't find exact matching of the keywords
        -> Reasons we don't find the exact keys:
            - Image uploaded by user may be blur.
            - Tesseracts extracted string may have some unexpected strings.
    """

    def __init__(self, img_data) -> None:
        self.img_data = img_data

    def front_aadhar_data(self) -> dict:
        aadhar_data = {
            'aadhar_id': self.get_aadhar_id(),
            'name': self.get_name(),
            'dob': self.get_dob(),
            'gender': self.get_gender()
        }
        return aadhar_data

    def get_aadhar_id(self):
        aadhar_id = ''
        try:
            aadhar_id = re.search('[0-9]{4} [0-9]{4} [0-9]{4}', self.img_data).group()
        except Exception as error:
            print('Error in parsing aadhar id::', error)
        return aadhar_id

    def get_name(self):
        name = ''
        try:
            name = re.search('\n(.*)\n\n', self.img_data).group()
            name = re.sub('\W+', ' ', name).strip()
        except Exception as error:
            print('Error in parsing name ::', error)
        return name

    def get_dob(self):
        try:
            dob = re.search('[0-9]{2}/[0-9]{2}/[0-9]{4}', self.img_data).group()
        except Exception as err:
            print("Error::", err)
            dob = ''
        return dob

    def get_gender(self):
        gender = "MALE"
        if "FEMALE" in self.img_data:
            gender = "FEMALE"
        return gender
