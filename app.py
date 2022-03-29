from flask import Flask, render_template, request
from flask_bootstrap5 import Bootstrap
from werkzeug.utils import secure_filename
import os
from os import abort
import PyPDF2

app = Flask(__name__)
bootstrap = Bootstrap(app)

user = {}

app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/')
def index():  # put application's code here
    pdfFileObj = open('static/sample_resume.pdf', 'rb')
    # Creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
    # Getting number of pages in pdf file
    pages = pdfReader.numPages
    # Loop for reading all the Pages
    for i in range(pages):
        # Creating a page object
        pageObj = pdfReader.getPage(i)
        # Printing Page Number
        print("Page No: ", i)
        # Extracting text from page
        # And splitting it into chunks of lines
        text = pageObj.extractText().split('\n')
        print(text)
        # Finally the lines are stored into list
        # For iterating over list a loop is used
        user['name'] = text[40]
        user['email'] = text[47]
        user['education'] = text[25]
        #user['major']
        #user['minor']
        #user['work history']

        '''for i in range(len(text)):
            # Printing the line
            # Lines are seprated using "\n"
            print(text[i], end="\n")
            # For Seprating the Pages
        '''
    # closing the pdf file object
    pdfFileObj.close()
    return render_template("index.html", user=user)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filename = secure_filename(uploaded_file.filename)
        if filename !='':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    return render_template('fileUpload.html')

if __name__ == '__main__':
    app.run()
