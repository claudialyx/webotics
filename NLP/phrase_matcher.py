import spacy
from spacy.matcher import Matcher
from spacy.matcher import PhraseMatcher

nlp = spacy.load('en_core_web_sm')

#### to get start_char & end_char for FSERV
# initialise the Matcher with a vocab.
# the matcher must always share the same vocab with the documents it will operate on
matcher = PhraseMatcher(nlp.vocab)
# terminology_list = ['personal loan', 'personal financing', 'housing loan', 'car loan', 'home loan', 'islamic personal loan', 'small business loan', 'business loan']

terminology_list = [
    'personal loan',
    'personal loans',
    'personal financing',
    'personal financings',
    'housing loan',
    'housing loans',
    'home loan',
    'home loans',
    'house loan',
    'house loans',
    'property loan',
    'property loans',
    'car loan',
    'car loans',
    'auto loan',
    'auto loans',
    'auto financing',
    'hire purchase',
    'car financing',
    'vehicle financing',
    'islamic personal loan',
    'islamic personal loans',
    'islamic loan',
    'islamic loans',
    'islamic personal loans',
    'small business loan',
    'small business loans',
    'business loan',
    'business loans',
    'sme loan',
    'sme loans',
    ]

pattern = [nlp.make_doc(text) for text in terminology_list]
matcher.add('TerminologyList', None, *pattern)

sentence = "There are 2 types of car loans: conventional car loan and islamic car loan."

doc = nlp(u"'%s'" %sentence)
matches = matcher(doc)
for match_id, start, end in matches:
    string_id = nlp.vocab.strings[match_id]  # get string representation
    span = doc[start:end]  # the matched span
    # print(match_id, string_id, start, end, span.text, span.start_char, span.end_char)
    print(doc, span.text, span.start_char, span.end_char)

doc1 = nlp(u"'%s'" %sentence)

for ent in doc1.ents:
    print(doc, ent.text, ent.start_char, ent.end_char, ent.label_)

# ---------------------------------------------------------------------------------------------
# WORD VECTOR:
# def most_similar(word):
#      by_similarity = sorted(word.vocab, key=lambda w: word.similarity(w), reverse=True)
#      return [w.orth_ for w in by_similarity[:10]]


# # terminology_list = ['personal loan', 'personal financing', 'housing loan', 'car loan', 'home loan', 'islamic personal loan', 'small business loan', 'business loan']
# # for word in terminology_list:
# #     print(most_similar(nlp.vocab[u"%s" %word]))
