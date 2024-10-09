# Python-Tesseract-Test
First Application: Tkinter Desktop App that translates text from an image. You need to have python 3.11 installed. This app also only works on Windows 11.
# Required Libaries
- [Pillow](https://pypi.org/project/pillow/)
- [Ttkbootstrap](https://pypi.org/project/ttkbootstrap/)
- [Translate](https://pypi.org/project/translate/) Hasn't been updated in awhile will probably replace with a translator API.
- [Opencv](https://pypi.org/project/opencv-python/)
- [Numpy](https://pypi.org/project/numpy/) Both Opencv and Numpy are used in one function called charboxes that highlight the text being translated. You can disable this function in the runtesseract.py file to not have to install these two libraries.
- [Pytesseract](https://pypi.org/project/pytesseract/)\
You also need [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html) the app. You can specify the directory of it in the application.
# How to Run
Just download all the required libraries and tesseract and run the runtesseract.py file and it should start up. 
# Future Features 
- Horizontal Scrolling
- character blacklist customizability - DONE
