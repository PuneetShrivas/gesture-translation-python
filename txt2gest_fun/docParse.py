from nltk import Tree
from tabulate import tabulate
import spacy
from translate import Translator
translator= Translator(to_lang="en",from_lang='ja')
nlp_en = spacy.load("en_core_web_lg")
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
adjectives = [
    'JJ',
    'JJR',
    'JJS',
]
auxiliaries_deps = [
    'AUX',
    'AUXPASS',
    'CCONJ',
    'TO',
]
modals = [
    'MD'
]
punctuations = [
    'PUNCT'
]
question_words=[
'WDT',
'WP',
'WP$',
'WRB',
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


def parse_doc(text):
    # text = str(translator.translate(text))
    doc = nlp_en(text)
    phrases = []
    meta_datas = []
    lemmas = []
    POS = []
    for i, token in enumerate(doc):
        token_meta_data = {}
        if token.tag_ in modals:
            POS.append('Modal')
        elif token.tag_ in question_words:
            POS.append('Question_Words')
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
        elif token.pos_ in punctuations:
            POS.append('Punctuation')
        elif token.pos_ in auxiliaries_deps or token.tag_ in auxiliaries_deps:
            POS.append('Auxiliary')
        else:
            POS.append('')
        for feature in features:
            feature = feature.strip()
            if len(token.morph.get(feature)) > 0:
                token_meta_data.update({feature: token.morph.get(feature)})
        phrases.append(token.text)
        meta_datas.append(token_meta_data)
        lemmas.append(token.lemma_)
    return [phrases, lemmas, meta_datas, POS]
