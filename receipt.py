from PIL import Image
import pytesseract as pt
from fuzzywuzzy import fuzz

from search import stores

# string = pt.image_to_string(Image.open('target.JPG'))
# string = string.lower()
# text = string.split('\n')
# text = list(filter(lambda x: x == '' or ' ', text))
# print(text)

FILTER = ['', ' ']
FINAL_THRESHOLD = 75

class Detector:
    def __init__(self, image):
        self.text = self._detect_text(image)

    def _clean_text(self, text):
        text = text.lower().split('\n')
        while '' or ' ' in text:
            text.remove('')
            text.remove(' ')
        return text

    def _detect_text(self, image):
        text = pt.image_to_string(Image.open(image))
        return self._clean_text(text)

    def hard_check_store(text):
        print('Hard check called...')
        b_store = ['',0]
        for i in text:
            for store in stores:
                ratio = fuzz.ratio(store, i)
                if ratio > b_store[1]:
                    b_store[0] = store
                    b_store[1] = ratio
        if b_store[1] < FINAL_THRESHOLD:
            return soft_check_store(text)
        else:
            return b_store

    def soft_check_store(text):
        print('Soft check called...')
        threshold = 75
        choices = [{'store': store, 'sum': 0, 'stores': 0} for store in stores]
        for i in text:
            for store in stores:
                ratio = fuzz.partial_ratio(store, i)
                if ratio >= threshold and len(i) > len(store):
                    for st in choices:
                        if st['store'] == store:
                            st['sum'] += ratio
                            st['stores'] += 1
        b_store = ['',0]
        for st in choices:
            if st['sum'] == 0:
                continue
            else:
                if st['stores'] > 1 and st['sum']/st['stores'] > FINAL_THRESHOLD:
                    b_store[0] = st['store']
                    b_store[1] = st['sum']/st['stores']
        if b_store[1] > 0:
            return b_store
        else:
            return 'No store found...'


image = Detector('target.JPG')
# img = image._detect_text('target.JPG')
print(image.text)
# store = hard_check_store(text)
# print(store)