# Notes to Anki 

## Overview

**Notes to Anki** is a web-based application that allows users to upload their notes in `.docx` format and automatically convert them into Anki flashcards. The application supports both basic definition cards and cloze deletion cards, making it easier to study and memorize important information. Notes to Anki is a service that I built in order to create Anki cards for Notes that I took in class, but wanted to review in a efficient manner such as anki cards. That why I decided to build Notes to Anki in a way that it simply needs you to adjust the way that you take notes such that you dictate what information is important, and what you need to reviewed. Below is the way that Notes to Anki expects you to take notes.

## How to use 

IMPORTANT:
To specify what information should be turned into a card, surround the information with "#|#"
->
Using this symbol denotes a basic card, where everything on the left of the arrow is the front of the card, and everything after is on the back of the card
[...]
Using this symbol denotes a cloze card, where everything in the bracket is hidden. There can be multiple clozes on one card
Examples
#|# The Mitochondria is the [powerhouse] of the cell #|#

#|# What cells use for energy -> ATP #|#

## Features

- **Custom Deck Name:** Users can specify a name for the Anki deck that will be generated.
- **Automatic Card Generation:**
  - **Definition Cards:** Automatically generated from `word -> definition` patterns in the notes.
  - **Cloze Deletion Cards:** Automatically generated from text enclosed in `[]` brackets.
- **Unique Delimiters:** The application looks for `#|#` delimiters in the notes to identify sections that should be converted into flashcards.

## Want to Customize it for yourself?

Feel free to fork the repository and adjust the code for your own note taking preferences as long as no monetization is involved. If you have any suggestions please free to contact me at ohashmi21@gmail.com, I am looking to improve the service and would appreciate all the feedback that I can get.

## Getting Started

### Prerequisites

To run this application locally, you need the following:

- Python 3.x
- Pip (Python package manager)
- Anki (to import and use the generated decks)

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/notes-to-anki.git
   cd notes-to-anki
2. **Install Dependencies:**
   pip install -r requirements.txt
  
3. **Run the Backend Server:**
   python app.py

4. **Run the frontend:**
   cd into front end
   run "npm run dev"
