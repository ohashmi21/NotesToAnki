from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
from genDeck import process_request, save_deck
import os

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/upload', methods=['POST'])
def upload_file():
    dname = request.form['dname']
    file = request.files['notes']
    
    # Process the file and create the Anki deck
    deck = process_request(dname, file)
    
    # Save the deck to a file
    output_file = f"{dname}.apkg"
    save_deck(deck, output_file)
    response = send_file(output_file, as_attachment=True, download_name=output_file)
    os.remove(f"{dname}.apkg")
    return response

if __name__ == '__main__':
    app.run(port=3000)
