from flask import Flask, render_template, request
import os
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.form['image']
    image_data = image_data.split(',')[1]  # Remove the header part
    image_data = base64.b64decode(image_data)
    
    with open('captured_image.png', 'wb') as f:
        f.write(image_data)
    
    return 'Image received', 200

if __name__ == '__main__':
    app.run(debug=True)
