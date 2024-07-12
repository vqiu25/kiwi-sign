from flask import Flask, render_template, request, jsonify
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
    
    # Here you would integrate your interpreting model
    word = interpret_image('captured_image.png')
    translated_word = translate_to_maori(word)
    
    return jsonify({'word': word, 'translated_word': translated_word}), 200

def interpret_image(image_path):
    # Dummy function to simulate image interpretation
    # Replace this with your actual model inference code
    return "Hello"

def translate_to_maori(word):
    # Dummy function to simulate translation
    # Replace this with your actual translation API call
    translations = {
        "Hello": "Kia ora",
        "Goodbye": "Haere rā",
        "Thank you": "Ngā mihi",
        # Alphabet (only including different terms)
        "A": "Ā",
        "E": "Ē",
        "I": "Ī",
        "O": "Ō",
        "U": "Ū",
        # Numbers (written out)
        "Zero": "Kore",
        "One": "Tahi",
        "Two": "Rua",
        "Three": "Toru",
        "Four": "Whā",
        "Five": "Rima",
        "Six": "Ono",
        "Seven": "Whitu",
        "Eight": "Waru",
        "Nine": "Iwa",
        # Days of the week
        "Monday": "Rāhina",
        "Tuesday": "Rātū",
        "Wednesday": "Rāapa",
        "Thursday": "Rāpare",
        "Friday": "Rāmere",
        "Saturday": "Rāhoroi",
        "Sunday": "Rātapu",
        # Months
        "January": "Kohitātea",
        "February": "Hui-tanguru",
        "March": "Poutū-te-rangi",
        "April": "Paenga-whāwhā",
        "May": "Haratua",
        "June": "Pipiri",
        "July": "Hōngongoi",
        "August": "Here-turi-kōkā",
        "September": "Mahuru",
        "October": "Whiringa-ā-nuku",
        "November": "Whiringa-ā-rangi",
        "December": "Hakihea",
        # Introductory Terms
        "Welcome": "Nau mai",
        "Please": "Tēnā koa",
        "Yes": "Āe",
        "No": "Kāo",
        "Excuse me": "Aroha mai",
        # Te Reo Terms
        "Family": "Whānau",
        "Friend": "Hoa",
        "House": "Whare",
        "Food": "Kai",
        "Water": "Wai"
    }
    return translations.get(word, " ")

if __name__ == '__main__':
    app.run(debug=True)
