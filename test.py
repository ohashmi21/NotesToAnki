from docx import Document
import genanki
import re

def read_document(file_path):
    # Open the Word document and read the paragraphs
    doc = Document(file_path)
    text = []
    for paragraph in doc.paragraphs:
        text.append(paragraph.text)
    return '\n'.join(text)

def extract_cards(text):
    definition_cards = []
    cloze_deletion_cards = []

    # Regex to find "->" patterns for definition cards
    definition_pattern = re.compile(r'(.+?)\s*->\s*(.+)')
    for match in definition_pattern.finditer(text):
        word, definition = match.groups()
        definition_cards.append((word.strip(), definition.strip()))

    # Regex to find "[]" patterns for cloze deletion cards
    cloze_pattern = re.compile(r'\[(.+?)\]')
    cloze_matches = cloze_pattern.findall(text)
    for match in cloze_matches:
        cloze_deletion = text.replace(f'[{match}]', f'{{{{c1::{match}}}}}')
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
                'afmt': '{{cloze:Text}}'  # The key here is `{{cloze:Text}}`
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

# Define the path to your Word document
file_path = 'Test.docx'
text = read_document(file_path)
definition_cards, cloze_deletion_cards = extract_cards(text)
deck = create_anki_deck(definition_cards, cloze_deletion_cards)
save_deck(deck, 'test.apkg')
