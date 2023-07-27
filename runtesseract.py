from PIL import Image,ImageTk
import cv2
import pytesseract
import numpy as np
import tesseract_script
import tkinter as tk
from ttkbootstrap.constants import *
from ttkbootstrap.scrolled import ScrolledFrame
import ttkbootstrap as tb
import sys
#Stores the images that are displayed
img_paths = []

#Allows the print statement to print to text box
def redirector(inputStr):
    text_box.insert(END, inputStr)

sys.stdout.write = redirector

#Clear everything from images and text box
def clear():
    text_box.delete("1.0", END)
    for label in frameImages.winfo_children():
        if isinstance(label, tb.Label):
            label.destroy()

#Draws boxes around detected characters
def charboxes():
    for img_files in tesseract_script.images:
        data = pytesseract.image_to_data(img_files, output_type='dict', config=tesseract_script.config)
        boxes = len(data['level'])    
        img_cv2 = np.array(img_files) 
        for i in range(4, boxes):
            if data['conf'][i] >= 50 and data["text"][i] != "":
                (x, y, w, h) = (data['left'][i], data['top'][i], data['width'][i], data['height'][i])
                cv2.rectangle(img_cv2, (x, y), (x + w, y + h), (0, 255, 0), 2)
        img = ImageTk.PhotoImage(image=Image.fromarray(img_cv2))
        img_paths.append(img)
        tb.Label(frameImages, image=img).pack(pady=10)
        
#Translate everything and prepares it for another translation process
def translate_reset():
    try:
        charboxes()
        tesseract_script.run_tesseract()
        tesseract_script.images = []
    except:
        print("Paste a Support Img Type Pls")
        tesseract_script.images = []

#Root is the Window that contains everything
root = tb.Window(themename="darkly")
root.geometry("1000x900")
root.title("Tesseract Image Translater")

#This frame contains the text box and image boxs
frameForTextImage = tb.Frame(root, bootstyle = "Dark")
frameForTextImage.pack(side=TOP, padx=10,pady=10,fill=BOTH, )

#This frame contains the images that will be displayed
frameImages = ScrolledFrame(frameForTextImage, autohide=True, bootstyle=DARK)
frameImages.pack(side= LEFT, padx=10,pady=10,fill=BOTH,expand=TRUE)
#This is the text box for all of the outputted text
text_box = tk.Text(frameForTextImage, font=("Source Code Pro", 12))
text_box.pack(side=RIGHT, padx=10, pady=10, fill=BOTH,expand=TRUE)
text_box.config(width=35, height=21)

#Contains the buttons for running the app 
frame_for_controls = tb.Frame(root, bootstyle = "Dark")
frame_for_controls.pack(side=TOP, padx=10,pady=10,fill=BOTH,expand=TRUE)

frame_for_buttons = tb.Frame(frame_for_controls)
frame_for_buttons.pack(side=LEFT, padx=10,pady=10,fill=BOTH, expand=TRUE)

buttonRun = tb.Button(frame_for_buttons, text="Run Tesseract", bootstyle=(INFO, OUTLINE), command=translate_reset)
buttonRun.pack(padx=10, pady=10,fill=BOTH, expand=TRUE)

buttonFiles = tb.Button(frame_for_buttons, text="Click to Select Your Files\nCtrl+V to Paste Images", bootstyle=(INFO, OUTLINE), command=tesseract_script.file_selector)
buttonFiles.pack(padx=10, pady=10,fill=BOTH,expand=TRUE)

def ControlV(event):
    tesseract_script.paste_image()
root.bind("<Control-v>", ControlV)

clearButton = tb.Button(frame_for_buttons, text="Clear Everything", bootstyle=(DANGER, OUTLINE), command=clear)
clearButton.pack(padx=10, pady=10,fill=BOTH,expand=TRUE )

#Frame that contains the congfig options for tesseract 
frame_for_config = tb.Frame(frame_for_controls)
frame_for_config.pack(side=LEFT, padx=10,pady=10,fill=BOTH,expand= TRUE)

tesseract_config = tb.Label(frame_for_config, bootstyle = "Info", text= "Configure Tesseract Settings", font=("Source Code Pro", 10))
tesseract_config.pack(side=TOP, padx=10, pady= 5,fill=BOTH)

#Pick the Language
language_menu = tb.Menubutton(frame_for_config, bootstyle = (INFO, OUTLINE), text= "Pick Language")
language_menu.pack(side=TOP, padx=10, pady= 5,fill=BOTH,)
language_options = tb.Menu(language_menu)

def language_picker(language):
    tesseract_script.settings["language"] = language
    tesseract_script.setting_change()
    tesseract_script.language = language
    tesseract_script.config = f'--tessdata-dir "{tesseract_script.tessdata}" -c tessedit_char_blacklist=♥abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*\/|()<>-+=:; -l {language} --psm {tesseract_script.psm}'
    language_menu.config(text=f'Language: {language}')

for x in ["jpn", "jpn_vert", "kor", "kor_vert"]:
    language_options.add_radiobutton(label=x, command= lambda x=x: language_picker(x), font=("Source Code Pro", 8))
language_menu["menu"] = language_options

#Pick PSM Options
psm_menu = tb.Menubutton(frame_for_config, bootstyle = (INFO, OUTLINE), text= "Pick PSM Mode")
psm_menu.pack(side=TOP, padx=10, pady= 5,fill=BOTH,)
psm_options = tb.Menu(psm_menu)

def psm_picker(psm):
    tesseract_script.settings["psm"] = str(psm)
    tesseract_script.setting_change()
    tesseract_script.psm = psm
    tesseract_script.config = f'--tessdata-dir "{tesseract_script.tessdata}" -c tessedit_char_blacklist=♥abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ@#$%&*\/|()<>-+=:; -l {tesseract_script.language} --psm {psm}'

    psm_menu.config(text=f'PSM Mode: {psm}')
for x in range(14):
    psm_options.add_radiobutton(label=x, command= lambda x = x: psm_picker(x), font=("Source Code Pro", 8))
psm_menu['menu'] = psm_options

tesseract_picker = tb.Button(frame_for_config, bootstyle =(INFO, OUTLINE), text="Find Your Tesseract.exe", command= tesseract_script.ask_tesseract_path)
tesseract_picker.pack(side=TOP, padx=10, pady= 5,fill=BOTH,)

tessdata_picker = tb.Button(frame_for_config, bootstyle =(INFO, OUTLINE), text="Find Your Tessdata folder", command= tesseract_script.ask_tessdata_path)
tessdata_picker.pack(side=TOP, padx=10, pady= 5,fill=BOTH,)

root.mainloop()