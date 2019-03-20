import spacy

from NLP.server import brain_folder_name

input_dir = brain_folder_name
nlp = spacy.load(input_dir)

def return_matches(input):
    storage = []
    doc = nlp(u"'%s'" %str(input))
    for ent in doc.ents:
        print(doc, ent.text, ent.start_char, ent.end_char, ent.label_)
        storage.append(ent.text)
    return storage
