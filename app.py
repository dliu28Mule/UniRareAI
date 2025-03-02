from flask import Flask, request, render_template, redirect, url_for, flash
import os
from transformers import pipeline
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this key for production

nlp = pipeline("ner", model="d4data/biomedical-ner-all", grouped_entities=True)

# Folder to store uploaded files
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def merge_entities(entities):
    merged_entities = []  # List to store merged entities
    current_entity = None  # Track the entity in progress

    for entity in entities:
        word = entity['word']
        entity_group = entity['entity_group']
        score = entity['score']

        # If the word is part of a split entity (either starts with "##" or continues a previous entity)
        if (word.startswith("##") or (current_entity and entity_group == current_entity["entity_group"])):
            current_entity["word"] += word.lstrip("#")  # Remove "##" and merge
        else:
            # If a previous entity was in progress, save it
            if current_entity:
                merged_entities.append(current_entity)

            # Start a new entity
            current_entity = {"word": word, "entity_group": entity_group, "score": score}

    # Don't forget the last entity
    if current_entity:
        merged_entities.append(current_entity)

    return merged_entities


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    entities = []
    if request.method == 'POST':
        print(request.form)
        print(request.files)
        
        file = request.files['medical_file']  # Get file from the form
        if file:
            text = file.read().decode("utf-8")  # Assuming the file is text-based (adjust if necessary)
            
            # 🔹 Process text with NLP model
            raw_entities = nlp(text)

            # 🔹 Print raw entity output BEFORE merging
            print("Raw Entities:", raw_entities)  # <--- ADD THIS LINE

            # 🔹 Merge entities correctly
            entities = merge_entities(raw_entities)

            # 🔹 Print merged entity output
            print("Merged Entities:", entities)

            return render_template('upload.html', entities=entities)  # Pass merged entities
        else:
            flash('No file selected or file format incorrect.')
            return redirect(request.url)

    return render_template('upload.html', entities=entities)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)