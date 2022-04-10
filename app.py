from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
from werkzeug.utils import secure_filename, redirect
import os
from os import abort
import PyPDF2

app = Flask(__name__)
bootstrap = Bootstrap5(app)

user = {}

app.config['MAX_CONTENT_LENGTH'] = 1024*1024
app.config['UPLOAD_EXTENSIONS'] = ['.pdf']
app.config['UPLOAD_PATH'] = 'uploads'

@app.route('/home')
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/application', methods=["POST", "GET"])
def parse():  # put application's code here
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
        for i in range(text.count(" ")):
            # Printing the line
            # Lines are seprated using "\n"
            text.remove(" ")
            # For Seprating the Pages

        print(text)

        # Finally the lines are stored into list
        # For iterating over list a loop is used
        user['name'] = text[2] + text[3] + text[4]
        user['email'] = text[10]
        #user['education'] = text[25]
        user['major'] = text[27].removeprefix("Major:  ")
        user['expGrad'] = text[29].removeprefix("Expected Graduation Date:  ")
        #user['work history']

        '''for i in range(len(text)):
            # Printing the line
            # Lines are seprated using "\n"
            print(text[i], end="\n")
            # For Seprating the Pages
        '''
    
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        major = request.form["major"]
        expgrad = request.form["expgrad"]
        f = open('data.txt', 'w')
        f.write(str(name) + '\n' + str(email) + '\n' + str(major) + '\n' + str(expgrad))
        f.close
    # closing the pdf file object
    pdfFileObj.close()
    return render_template("application.html", user=user)

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
            return redirect('/application')
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
