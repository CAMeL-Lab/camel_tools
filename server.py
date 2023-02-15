import spacy
from camel_tools.morphology.analyzer import Analyzer
from camel_tools.morphology.database import MorphologyDB
from ntpath import join
from flask import Flask
from camel_tools.disambig.mle import MLEDisambiguator
from flask import request
from flask import jsonify
import sys

app = Flask(__name__)
mle = MLEDisambiguator.pretrained()

db = MorphologyDB.builtin_db()

# Create analyzer with no backoff
analyzer = Analyzer(db)
nlp = spacy.load("en_core_web_sm")


@app.route("/analyze", methods=['POST'])
def analyze_word():
    content = request.get_json()
    words = content['sentence'].split()
    return jsonify(
        {"grammatical_information": disam_with_actual_word('pos', words, wordKey='word', grammarKey='grammar')})


@app.route("/conll-u-format", methods=['POST'])
def conll_u_word():
    content = request.get_json()
    array_of_sentences = content['sentence']
    return convert_to_conll_u_format(array_of_sentences)
    # return array_of_sentences


def convert_to_conll_u_format(array_of_sentences):
    # head_information = get_head_indformation_of_sentence(array_of_sentences)
    final_data_array = []
    for (sentence) in array_of_sentences:
        words = sentence['text'].split()
        interpretation = mle.disambiguate(words)
        for (index, words) in enumerate(interpretation):
            if len(words.analyses) > 0:
                final_data_array.append(
                    {
                        "SENTENCE_ID": sentence['_id'],
                        "id": index + 1,
                        "form": words.analyses[0].analysis['diac'],
                        "lemma": words.analyses[0].analysis['stem'],
                        "pos": words.analyses[0].analysis['pos'],
                        # "HEAD": head_information[index]['head_index'],
                        # "DEPREL": head_information[index]['dep'],
                        "features": "ASPECT= " + words.analyses[0].analysis['asp'] +
                                 "|"
                                 + "CASE= " + words.analyses[0].analysis['cas'] +
                                 "|"
                                 + "GENDER= " + words.analyses[0].analysis['gen'] +
                                 "|"
                                 + "MOOD= " + words.analyses[0].analysis['mod'] +
                                 "|"
                                 + "NUMBER= " + words.analyses[0].analysis['form_num'] +
                                 "|"
                                 + "PERSON= " + words.analyses[0].analysis['per'] +
                                 "|"
                                 + "STATE= " + words.analyses[0].analysis['stt'] +
                                 "|"
                                 + "VOICE= " + words.analyses[0].analysis['vox'],
                    }
                )
    return final_data_array


def get_head_indformation_of_sentence(text):
    formatted_text_to_observe = nlp(text)
    data_array = []
    for token in formatted_text_to_observe:
        word = token.text
        dep = token.dep_
        head = token.head.text
        head_index = 0 if (word == head) else text.split().index(head) + 1
        data_array.append(
            {"dep": dep, "head_index": head_index},
        )
    return data_array


@app.route("/diac", methods=['POST'])
def diac():
    content = request.get_json(silent=True)
    sentences = content['text'].split('\n')
    print(sentences)
    arr = []
    for sent in sentences:
        diacSent = disam('diac', sent.split())
        arr.append(
            ' '.join(['' if word is None else word for word in diacSent]))
    return jsonify({"text": '\n'.join(arr), "type": 'lex'})



@app.route("/lemma", methods=['POST'])
def lemma():
    content = request.get_json()
    sentence = content['text'].split()
    return jsonify({"text": disam('lex', sentence), "type": 'lex'})


@app.route("/lemmaList", methods=['POST'])
def lemmaList():
    lemmaArray = []
    content = request.get_json()
    sentence = content['text'].split()
    print("sentence", sentence)
    analyses = analyzer.analyze(sentence[0])
    for analysis in analyses:
        lemmaArray.append(analysis["lex"])
    return jsonify({"text": list(set(lemmaArray)), "type": 'lex'})


@app.route("/morph", methods=['POST'])
def morph():
    content = request.get_json(silent=True)
    sentence = content['text'].split()
    return morph(sentence)


def disam(type, sentence):
    # We expect a sentence to be whitespace/punctuation tokenized beforehand.
    # We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
    # See camel_tools.tokenizers.word.simple_word_tokenize.
    disambig = mle.disambiguate(sentence)
    # Let's, for example, use the top disambiguations to generate a diacritized
    # version of the above sentence.
    # Note that, in practice, you'll need to make sure that each word has a
    # non-zero list of analyses.
    return [(d.analyses[0].analysis[type] if len(d.analyses) > 0 else None) for d in disambig]


def disam_with_actual_word(type, sentence, wordKey='word', grammarKey='grammar'):
    interpretation = mle.disambiguate(sentence)
    print(interpretation)
    final_data_array = []
    for data in interpretation:
        if len(data.analyses) > 0:
            final_data_array.append(
                {
                    wordKey: data.analyses[0].analysis['diac'],
                    grammarKey: data.analyses[0].analysis[type]
                }
            )
    return final_data_array


def morph(sentence):
    # We expect a sentence to be whitespace/punctuation tokenized beforehand.
    # We provide a simple whitespace and punctuation tokenizer as part of camel_tools.
    # See camel_tools.tokenizers.word.simple_word_tokenize.

    words = []
    for d in sentence:
        if d:
            x = {
                'word': d,
                'analyses': analyzer.analyze(d),
            }
            words.append(x)
        else:
            words.append(None)
    return jsonify(words)
