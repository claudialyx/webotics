from __future__ import unicode_literals, print_function
import json
import os
import spacy
import plac # wrapper over argparse
import random
from pathlib import Path
# from tqdm import tqdm #loading bar
from spacy.util import minibatch, compounding
from NLP.training_data2 import TRAIN_DATA

# Start of sharing location on "brain folder" generation on server.py and test.py
brain_name = "brain3_25"
brain_folder_name = os.path.join(os.path.dirname(
	os.path.abspath(__file__)), f"trained_model\\{brain_name}")

nlp1 = spacy.load('en_core_web_sm')
# new entity label = 'FSERV' stands for financial services
LABEL = 'FSERV'

@plac.annotations(
    model=("en_core_web_sm", "option", "m", str),
    new_model_name=("New model name for model meta.", "option", "nm", str),
    output_dir=(f"{brain_folder_name}", "option", "o", Path),
    n_iter=(25, "option", "n", int))

# def main(model=None, new_model_name='fserv', output_dir=None, n_iter=10):
def main(model="en_core_web_sm", new_model_name='fserv', output_dir=f"{brain_folder_name}", n_iter=25):
    # """Set up the pipeline and entity recognizer, and train the new entity."""
    print(output_dir)
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")
    # Add entity recognizer to model if it's not in the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if 'ner' not in nlp.pipe_names:
        ner = nlp.create_pipe('ner')
        nlp.add_pipe(ner)
    # otherwise, get it, so we can add labels to it
    else:
        ner = nlp.get_pipe('ner')
    
    ner.add_label(LABEL)   # add new entity label to entity recognizer
    if model is None:
        optimizer = nlp.begin_training()
    else:
        # Note that 'begin_training' initializes the models, so it'll zero out
        # existing entity types.
        optimizer = nlp.entity.create_optimizer()

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):  # only train NER
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(texts, annotations, sgd=optimizer, drop=0.4,losses=losses)
            print('Losses', losses)

    # Run these codes to test the trained model:
    # test_text =[
#     "They are considering to get a JCL Personal loan",
#     "personal loan, car loan, house loans, personal financing, business loan",
#     "personal loans, car loans, house loans, personal financings, business loans",
#     "Singapore officially the Republic of Singapore is an island city-state in Southeast Asia.",
#     "personal loans, car loans, house loans, housing loans, personal financings, business loan",
#     "Islamic personal loan",
#     "Apple is looking at buying U.K. startup for $1 billion",
#     "Jack is searching for the best interest rate for small business loans",
#     "Compare Malaysian housing loans with our housing loan calculator.",
#     "for a new mortgage loan or refinance your mortgage with Citibank's competitive mortgage loan",
#     "Donald John Trump (born June 14, 1946) is the 45th and current president of the United States.",
#     "Get the latest news, updates, and happenings at Google.",
#     "He is in need of some personal financing advice"
#     ]
    # test_text = 'RHB Easy-Pinjaman Ekspres, JCL Personal loan, AEON i-Cash Personal Financing are some examples of personal loans available in Malaysia.'
    # test_text = test_text.lower()
    # doc = nlp(test_text)
    # print("Entities in '%s'" % test_text)
    # for ent in doc.ents:
    #     print(ent.label_, ent.text)

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.meta['name'] = new_model_name  # rename model
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)
        print("a", output_dir)

    # Run these code to test the saved model:
    # print("Loading from", output_dir)
    # nlp2 = spacy.load(output_dir)
    # doc2 = nlp2(test_text)
    # for ent in doc2.ents:
    #     print(ent.label_, ent.text)

if __name__ == '__main__':
    plac.call(main)


