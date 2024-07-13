from flask import Flask, render_template, request, jsonify, session
import base64

app = Flask(__name__, static_url_path='/static')
app.secret_key = 'your_secret_key'

words = {
    "greetings": {
        "Hello": "Kia ora",
        "Goodbye": "Haere rā",
        "Thank you": "Ngā mihi"
    },
    "numbers": {
        "Zero": "Kore",
        "One": "Tahi",
        "Two": "Rua",
        "Three": "Toru",
        "Four": "Whā",
        "Five": "Rima",
        "Six": "Ono",
        "Seven": "Whitu",
        "Eight": "Waru",
        "Nine": "Iwa"
    },
    "days": {
        "Monday": "Rāhina",
        "Tuesday": "Rātū",
        "Wednesday": "Rāapa",
        "Thursday": "Rāpare",
        "Friday": "Rāmere",
        "Saturday": "Rāhoroi",
        "Sunday": "Rātapu"
    },
    "months": {
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
        "December": "Hakihea"
    },
    "terms": {
        "Welcome": "Nau mai",
        "Please": "Tēnā koa",
        "Yes": "Āe",
        "No": "Kāo",
        "Excuse me": "Aroha mai",
        "Family": "Whānau",
        "Friend": "Hoa",
        "House": "Whare",
        "Food": "Kai",
        "Water": "Wai"
    }
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/pokedex')
def pokedex():
    seen_words = session.get('seen_words', [])
    return render_template('pokedex.html', words=words, seen_words=seen_words)

@app.route('/category/<category>')
def category(category):
    category_words = words.get(category, {})
    seen_words = session.get('seen_words', [])
    return render_template('category.html', category=category.capitalize(), words=category_words, seen_words=seen_words)

@app.route('/upload', methods=['POST'])
def upload():
    image_data = request.form['image']
    image_data = image_data.split(',')[1]  # Remove the header part
    image_data = base64.b64decode(image_data)
    
    with open('captured_image.png', 'wb') as f:
        f.write(image_data)
    
    word = interpret_image('captured_image.png')
    translated_word = translate_to_maori(word)
    
    # Update seen words in session
    seen_words = session.get('seen_words', [])
    if word not in seen_words:
        seen_words.append(word)
    session['seen_words'] = seen_words
    
    return jsonify({'word': word, 'translated_word': translated_word}), 200

def interpret_image(image_path):
    return "Hello"  # This should be replaced with your actual model logic

def translate_to_maori(word):
    translations = {
        "Hello": "Kia ora",
        "Goodbye": "Haere rā",
        "Thank you": "Ngā mihi",
        "A": "Ā",
        "E": "Ē",
        "I": "Ī",
        "O": "Ō",
        "U": "Ū",
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
        "Monday": "Rāhina",
        "Tuesday": "Rātū",
        "Wednesday": "Rāapa",
        "Thursday": "Rāpare",
        "Friday": "Rāmere",
        "Saturday": "Rāhoroi",
        "Sunday": "Rātapu",
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
        "Welcome": "Nau mai",
        "Please": "Tēnā koa",
        "Yes": "Āe",
        "No": "Kāo",
        "Excuse me": "Aroha mai",
        "Family": "Whānau",
        "Friend": "Hoa",
        "House": "Whare",
        "Food": "Kai",
        "Water": "Wai"
    }
    return translations.get(word, " ")

if __name__ == '__main__':
    app.run(debug=True)
