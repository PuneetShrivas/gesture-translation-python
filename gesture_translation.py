from nltk import Tree
import spacy
import scipy.io
from tabulate import tabulate
nlp = spacy.load("en_core_web_lg")

features = [
    "PronType",
    "Gender",
    "Case",
    "VerbForm",
    "NumType",
    "Animacy",
    "Mood",
    "Poss",
    "NounClass",
    "Tense",
    "Reflex",
    "Number	",
    "Aspect",
    "Foreign",
    "Case	",
    "Voice",
    "Abbr	",
    "Definite	",
    "Evident",
    "Typo	",
    "Degree	",
    "Polarity",
    "Person",
    "Polite",
    "Clusivity"
]
verb_forms = ['VB', 'VBZ', 'VBD', 'VBG', 'VBN', 'VBP']
nouns = [
    "NN",
    "NNS",
    "NNP",
    "NNPS"
]
pronouns = [
    "PRP",
    "PRP$"
]
adverbs = [
'RB',
'RBR',
'RBS'
]
adjectives =[
'JJ',
'JJR',
'JJS',
]
auxiliaries_deps=[
'AUX',
'AUXPASS',
'CCONJ',
'TO',
]


def tok_format(tok):
    # if tok.tag_ in verb_forms:
        # print("VERB : ", tok.orth_,"'s part is ", partForVerb(tok.orth_.lower()))
    return "_".join([tok.orth_.upper(), tok.tag_, str(tok.morph)])

def to_nltk_tree(node):
    if node.n_lefts + node.n_rights > 0:
        return Tree(tok_format(node), [to_nltk_tree(child) for child in node.children])
    else:
        return tok_format(node)

def parse_doc(doc):
    phrases=[]
    meta_datas = []
    lemmas = []
    POS = []
    for i,token in enumerate(doc):
        token_meta_data = {}
        if token.pos_ in auxiliaries_deps or token.tag_ in auxiliaries_deps:
            POS.append('Auxiliary')            
        elif token.tag_ in pronouns:
            POS.append('Pronoun')
        elif token.tag_ in nouns:
            POS.append('Noun')
        elif token.tag_ in verb_forms:
            POS.append('Verb')
        elif token.tag_ in adverbs:
            POS.append('Adverb')
        elif token.tag_ in adjectives:
            POS.append('Adjective')
        else :
            POS.append('')
        for feature in features:
            feature=feature.strip()
            if len(token.morph.get(feature))>0:
                token_meta_data.update({feature:token.morph.get(feature)})
        phrases.append(token.text)
        meta_datas.append(token_meta_data)
        lemmas.append(token.lemma_)
    return [phrases,lemmas,meta_datas,POS]





# for token in doc:
#     print(tabulate([[token.text, token.lemma_, token.pos_, token.tag_, token.dep_,token.shape_, token.is_alpha, token.is_stop, token.morph]]))


doc = nlp("You eat there")
[phrases,lemmas,meta_datas,POS] = parse_doc(doc)
for count,phrase in enumerate(phrases):
    print(tabulate([[phrase,lemmas[count],meta_datas[count],POS[count]]]))

# scipy.io.savemat('res_from_python.mat',{'phrases':phrases,'lemmas':lemmas,'meta_datas':meta_datas,'POS':POS})



