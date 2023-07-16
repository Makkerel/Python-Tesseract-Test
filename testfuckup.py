from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pytesseract
from googletrans import Translator

def select_images():
    # Open file dialog
    file_paths = filedialog.askopenfilenames(filetypes=[('Image Files', '*.png;*.jpg;*.jpeg')])

    for file_path in file_paths:
        if file_path:
            # Open image
            img = Image.open(file_path)

            # Convert image to text
            text = pytesseract.image_to_string(img)

            # Translate text to English
            translator = Translator()
            translated_text = translator.translate(text, dest='en').text

            # Create label to display image
            img = ImageTk.PhotoImage(img)
            img_label = Label(root, image=img)
            img_label.pack()

            # Create label to display translated text
            text_label = Label(root, text=translated_text)
            text_label.pack()

# Create root window
root = Tk()

# Create button to select images
select_button = Button(root, text='Select Images', command=select_images)
select_button.pack()

# Run main loop
root.mainloop()
