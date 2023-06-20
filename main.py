from flask import Flask, request, redirect, url_for
import os
import PyPDF3
import pyttsx3
import pdfplumber

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads/'  # replace with the path to your uploads folder
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return redirect(url_for('upload'))


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        # filename = file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'sample_pdf.pdf')
        file.save(filepath)
        book = open(filepath,'rb')
        pdfReader = PyPDF3.PdfFileReader(book)
        pages = pdfReader.numPages
        finalText = ""
        with pdfplumber.open(filepath) as pdf:
            page_one = pdf.pages[1]
            text = page_one.extract_text()
            finalText += text
            engine = pyttsx3.init()
            final_file_name = 'audio/sample.mp3'
            engine.save_to_file(finalText,final_file_name)
            engine.runAndWait()
            return "<br><br><h3 style='text-align: center;'>Uploaded Successdfully</h3>"


    return '''
        <!DOCTYPE html><html><head><title>File Upload Form</title><link rel='stylesheet' href='/uploads/bootstrap/bootstrap.css'></head><body>
        <center>
        <div class='box-radius'>
        <br><br>
         <h1>Upload PDF to convert to MP3</h1>
            <form class='form-group' method="post" enctype="multipart/form-data">
                <input class='form-control' type="file" name="file">
                <input  class='btn' type="submit" value="Convert">
            </form></body></html>
        </div>
        </center>
        <style>
        .form-control{
        border: solid blue 2px;
         padding: 12px;
         width: 300px;
          border-radius: 5px;
        
        
        }
        .btn {
             border: solid blue 1px;
             background: blue;
             padding: 18px;
             width: 150px;
             color: white;
             border-radius: 5px;
        }
        .box-radius{
          width: 70%;
          height: 300px;
          background-color: #fff;
          box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
          margin-top: 100px;
        
        }
        .btn:hover {
             border: solid black 1px;
             background: black;
             padding: 18px;
             width: 150px;
             color: white;
             border-radius: 5px;
        }
        
        </style>
    '''

if __name__ == '__main__':
    app.run(debug=True)
