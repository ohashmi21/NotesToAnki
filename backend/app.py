from flask import Flask, request, send_file
from flask_cors import CORS  # Import CORS
import os
from docx import Document
import genanki
import re

def process_request(dname, file):
    doc = read_document(file)
    def_card, cloze_card = extract_cards(doc)
    return create_anki_deck(def_card, cloze_card, dname)

def read_document(doc):
    document = Document(doc)
    text = []
    for paragraph in document.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_cards(text):
    definition_cards = []
    cloze_deletion_cards = []

    # Split text into parts separated by '#|#'
    parts = []
    stack = []
    start_index = None

    i = 0
    while i < len(text):
        if text[i:i+3] == "#|#":
            if not stack:
                start_index = i + 3  # Start after the first '#|#'
                stack.append("#|#")
                i += 3
            else:
                # Found a closing '#|#'
                part = text[start_index:i].strip()  # Extract content between '#|#'
                parts.append(part)
                stack.pop()
                i += 3
        else:
            i += 1

    # Now that we have the parts, let's extract cards
    for part in parts:
        # Regex to find "->" patterns for definition cards
        definition_pattern = re.compile(r'(.+?)\s*->\s*(.+)')
        for match in definition_pattern.finditer(part):
            word, definition = match.groups()
            definition_cards.append((word.strip(), definition.strip()))

        # Regex to find "[]" patterns for cloze deletion cards
        cloze_pattern = re.compile(r'\[(.+?)\]')
        cloze_matches = cloze_pattern.findall(part)
        for match in cloze_matches:
            bold_cloze = f"<b>{{{{c1::{match}}}}}</b>"  # Make the cloze text bold
            cloze_deletion = part.replace(f'[{match}]', bold_cloze)
            cloze_deletion_cards.append(cloze_deletion)

    return definition_cards, cloze_deletion_cards

def create_anki_deck(definition_cards, cloze_deletion_cards, deck_name="My Deck"):
    deck = genanki.Deck(
        2059400110,  # Unique deck ID
        deck_name
    )

    # Define the model for basic definition cards
    basic_model = genanki.Model(
        1607392319,  # Unique model ID
        'Basic Model',
        fields=[
            {'name': 'Word'},
            {'name': 'Definition'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{Word}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Definition}}',
            },
        ])

    # Define the model for cloze deletion cards
    cloze_model = genanki.Model(
        9988776611,  # Unique model ID
        'Cloze',
        fields=[
            {'name': 'Text'},
        ],
        templates=[
            {
                'name': 'Cloze Card',
                'qfmt': '{{cloze:Text}}',
                'afmt': '{{cloze:Text}}'
            },
        ],
        model_type=genanki.Model.CLOZE  # Ensure the model type is set to cloze
    )

    # Add definition cards to the deck
    for word, definition in definition_cards:
        note = genanki.Note(
            model=basic_model,
            fields=[word, definition]
        )
        deck.add_note(note)

    # Add cloze deletion cards to the deck
    for cloze_text in cloze_deletion_cards:
        note = genanki.Note(
            model=cloze_model,
            fields=[cloze_text]
        )
        deck.add_note(note)

    return deck

def save_deck(deck, file_name='output.apkg'):
    # Save the deck as an .apkg file
    genanki.Package(deck).write_to_file(file_name)

app = Flask(__name__)
CORS(app)

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
    return response

if __name__ == '__main__':
    app.run(port=3000)


