import re
from collections import defaultdict
import string


class Pan:
    """
        Extracts Pan Card data of user from the extracted string of the image.
        >> Name
        >> PAN Number
        >> DOB
    """

    def __init__(self, img_data) -> None:
        self.img_data = img_data
        self.processed_data = ""
        self.clarity_flag=False

    def _check_alphabet_patterns(self,str):
        vowels_consonants = '[^\S\r\n].*?(([aeiou]{3,})|([^aeiou\s0-9]{4,})).*?[^\S\r\n]'
        text = re.sub(vowels_consonants, " ", str, re.IGNORECASE)
        anti_title_case = "[^\S\r\n][A-Z]*[a-z]+[A-Z][a-zA-Z]*?[^\S\r\n]"
        text = re.sub(anti_title_case, " ", text)
        return text


    def preprocess_data(self):
        text = re.sub('[^-a-zA-Z0-9/\s]',' ',self.img_data)
        text = re.sub('[^\S\r\n]',' ',text)
        text = re.sub('\n+','\n',text)
        text = self._check_alphabet_patterns(text)
        lines = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line)>3:
                lines.append(line)
        self.processed_data = '\n'.join(lines)

        print(self.img_data)
        print('+'*25)
        print(self.processed_data)
    def get_pan_details(self) -> dict:
        self.preprocess_data()
        names = self.get_names()
        pan_data = {
            'pan_no': self.get_pan_number(),
            'dob': self.get_dob(),
            'name': names.get('holder_name',None),
            'father_name' : names.get('father_name',None)
        }
        if not self.clarity_flag:
            pan_data['error'] = "Image not clear enough"
        return pan_data

    def get_pan_number(self):
        pan_no = None
        for line in self.processed_data.split('\n'):
            if self.clarity_flag:
                try:
                    return re.search('[A-Z]{5}[0-9]{4}[A-Z]',line).group()
                except Exception:
                    self.clarity_flag = False
                    print('PAN Number not found')
            if re.search('Permanent Account Number',line):
                self.clarity_flag = True
        return pan_no

    def get_names(self):
        prev_line = ''
        names = defaultdict()
        for line in self.processed_data.split('\n'):
            if re.search('income|tax|department|government|india|govt',prev_line, re.IGNORECASE):
                try:
                    names['holder_name'] = max(re.findall('[A-Z ]+',line), key=len)
                    prev_line = "name_detected"
                    continue
                except Exception as e:
                    print(f'Error in Name Detection: {e}')
                return None
            elif "name_detected" in prev_line:
                try:
                    names['father_name'] = max(re.findall('[A-Z ]+',line), key=len)
                except Exception as e:
                    print(f'Error in Father Name Detection: {e}')
            prev_line = line
        return names

    def get_dob(self):
        dob = defaultdict()
        try:
            dobstr = re.search(r'[0-9]{2}/[0-9]{2}/[0-9]{4}', self.processed_data).group()
            dobstr = dobstr.split('/')
            if int(dobstr[1])<=12:
                dob['day'] = dobstr[0]
                dob['month'] = dobstr[1]
            else:
                dob['day'] = dobstr[1]
                dob['month'] = dobstr[0]
            dob['year'] = dobstr[2]
        except Exception as e:
            print(f'Error in DOB: {e}')
        return dob
