import re
from collections import defaultdict
import string


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
        self.processed_data = ""

    def _check_alphabet_patterns(self, str):

        vowels_consonants = '[^\S\r\n].*?(([aeiou]{3,})|([^aeiou\s0-9]{4,})).*?[^\S\r\n]'
        print(re.findall(vowels_consonants, str, re.IGNORECASE))
        text = re.sub(vowels_consonants, " ", str, flags=re.IGNORECASE)

        print(f'3.1: {text}')
        anti_title_case = "[^\S\r\n][A-Z]*[a-z]+[A-Z][a-zA-Z]*?[^\S\r\n]"
        text = re.sub(anti_title_case, " ", text)
        print(f'3.2: {text}')

        return text

    def preprocess_data(self):
        text = re.sub('[^-a-zA-Z0-9/\s]', ' ', self.img_data)
        print(f'1: {text}')
        text = re.sub('[^\S\r\n]', ' ', text)
        print(f'2: {text}')
        text = re.sub('\n+', '\n', text)
        print(f'3: {text}')
        text = self._check_alphabet_patterns(text)
        print(f'4: {text}')
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 3:
                lines.append(line)
        self.processed_data = '\n'.join(lines)

        print(self.img_data)
        print('+' * 25)
        print(self.processed_data)

    def front_aadhaar_data(self) -> dict:
        self.preprocess_data()
        aadhaar_data = {
            'aadhaar_id': self.get_aadhaar_id(),
            'dob': self.get_dob(),
            'gender': self.get_gender(),
            'name': self.get_name()
        }
        return aadhaar_data

    def get_aadhaar_id(self):
        aadhaar_id = None
        try:
            aadhaar_id = re.search('(?<!([0-9] ))[0-9]{4} [0-9]{4} [0-9]{4}(?!( [0-9]))', self.processed_data).group()
        except Exception as error:
            print('Error in parsing aadhaar id::', error)
        return aadhaar_id

    def get_name(self):
        try:
            text = re.sub(".*government|india", "", self.processed_data, flags=re.IGNORECASE | re.DOTALL)
            print(re.findall('(?:(?:^|\s)[A-Z][a-z]*)+', text))
            return re.sub('(^\s)|(\s$)', '', max(re.findall('(?:(?:^|\s)[A-Z][a-z]*)+', text), key=len))
        except Exception as e:
            print(f'Error in Name Detection: {e}')
        return None

    def get_dob(self):
        lines = self.processed_data.split('\n')
        dob = defaultdict()
        for line in lines:
            if re.search('(year)|(yob)', line, re.IGNORECASE):
                try:
                    dob['year'] = re.search('[0-9]{4}', line)
                except Exception as e:
                    print(f'Error in YOB: {e}')

            elif re.search('(date )|(dob)|(d0b)', line, re.IGNORECASE):
                print(f'Found DOB line: {line}')
                try:
                    dobstr = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', line).group()
                    dobstr = dobstr.split('/')
                    if int(dobstr[1]) <= 12:
                        dob['day'] = dobstr[0]
                        dob['month'] = dobstr[1]
                    else:
                        dob['day'] = dobstr[1]
                        dob['month'] = dobstr[0]
                    dob['year'] = dobstr[2]
                except Exception as e:
                    print(f'Error in DOB: {e}')
        return dob

    def get_gender(self):
        for line in self.processed_data.split('\n'):
            if re.search('[male]{4}', line, re.IGNORECASE):
                print(f'Found Gender line: {line}')
                if re.search('female|emal', line, re.IGNORECASE):
                    return "FEMALE"
                elif re.search('male', line, re.IGNORECASE):
                    return "MALE"
                else:
                    print('Gender Not Found')

        return None
