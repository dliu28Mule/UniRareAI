from transformers import pipeline

# Load a Named Entity Recognition (NER) model for medical text
nlp = pipeline("ner", model="d4data/biomedical-ner-all", grouped_entities=True)

# Example medical text
text = "The patient was diagnosed with pneumonia and prescribed amoxicillin."

# Process the text
entities = nlp(text)

# Merge split entities and print the results
final_entities = []
current_entity = ""

for entity in entities:
    # If the entity is split (e.g., "am" and "##oxicillin"), merge them
    if entity['word'].startswith("##"):
        current_entity += entity['word'][2:]  # Remove "##" and append the word
    else:
        if current_entity:
            final_entities.append({'word': current_entity, 'entity_group': entity['entity_group'], 'score': 1.0})  # Use 1.0 score for merged entities
        current_entity = entity['word']  # Start a new entity
final_entities.append({'word': current_entity, 'entity_group': entities[-1]['entity_group'], 'score': 1.0})  # Append the last entity

# Print the merged entities
print("Merged Entities:")
for entity in final_entities:
    print(f"{entity['word']} -> {entity['entity_group']} (score: {entity['score']:.2f})")





