import pytesseract
import json
import os
from PIL import Image,ImageGrab
from tkinter import filedialog
from translate import Translator

#Json Setting File
if os.path.isfile("setting.json"):
    with open("setting.json", "r") as f:
        settings = json.load(f)
else:
    settings = {
        "tesseract_path": "", 
        "tessdata_path": "", 
        "language": "", 
        "psm": "", 
        "blacklist": ""
    }
    with open('settings.json', 'w') as f:
        json.dump(settings, f)

def setting_change():
    with open("setting.json", "w") as f:
        json.dump(settings, f)

#config for tesseract OCR
pytesseract.pytesseract.tesseract_cmd = settings["tesseract_path"]
tessdata = settings["tessdata_path"]
language = settings["language"]
psm = settings["psm"]
blacklist = settings["blacklist"]
config = f'--tessdata-dir "{tessdata}" -c tessedit_char_blacklist={blacklist} -l {language} --psm {psm}'

translate_dictionary = {
    "jpn": "ja",
    "jpn_vert": "ja",
    "kor": "ko",
    "kor_vert": "ko"
}

#Will contain the filepaths for all the of pasted images
images = []

def remove_string_stuff(text):
    return text.replace(" ", "").replace("\n", "").strip()

#Path for Tesseract
def ask_tesseract_path():
    settings["tesseract_path"] = filedialog.askopenfilename()
    setting_change()
    pytesseract.pytesseract.tesseract_cmd = settings["tesseract_path"]

def ask_tessdata_path():
    global tessdata
    settings["tessdata_path"] = filedialog.askdirectory()
    setting_change()
    global config
    config = f'--tessdata-dir "{settings["tessdata_path"]}" -c tessedit_char_blacklist=♥abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*\/|()<>-+=:; -l {language} --psm {psm}'

#Allows you to paste image and saves it automatically
def paste_image(): 
    img = ImageGrab.grabclipboard()
    if img == None:
        print("Failed to Paste Image")
        return
    print("Paste Successful")
    images.append(img)

#Selects files that you want to be translated
def file_selector():
    #file(s) selector 
    filepaths = filedialog.askopenfilenames()
    for paths in filepaths:
        img = Image.open(paths)
        images.append(img)

def run_tesseract():
    #Extract text from each image selected
    for imgs in images:
        text = pytesseract.image_to_string(imgs, config=config)
        text = remove_string_stuff(text)
        print(text)
        #translates text
        translation = Translator(to_lang="en", from_lang= translate_dictionary[language])
        translated = translation.translate(text)
        print(translated.replace("\n", "").strip())
