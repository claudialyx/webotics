import spacy
input_dir = "C:\\Users\\User\\Desktop\\Back_end\\brain(iter-dr)\\b60-25"
nlp = spacy.load(input_dir)

# sentences =[
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

# for s in sentences:
    # print(s)
def return_matches(input):
    storage = []
    doc = nlp(u"'%s'" %str(input))
    for ent in doc.ents:
        print(doc, ent.text, ent.start_char, ent.end_char, ent.label_)
        storage.append(ent.text)
    return storage  

