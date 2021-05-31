import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import sys
 
# pip install -U spacy
# python -m spacy download en_core_web_sm

def summarizer(text, k=3):
    stopwords = list(STOP_WORDS)
    nlp = spacy.load("en_core_web_sm")
    docx = nlp(text)

    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1

    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():  
            word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

    sentence_list = [ sentence for sentence in docx.sents ]

    sentence_scores = {}  
    for sent in sentence_list:  
            for word in sent:
                if word.text.lower() in word_frequencies.keys():
                    # if len(sent.text.split(' ')) < 50:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    sentence_scores = dict(sorted(sentence_scores.items(), key=lambda item: item[1], reverse=True))
    sumario= ""
    for i in range(k):
        if i <= len(sentence_scores.keys()):
            sumario += str(list(sentence_scores.keys())[i]) + "\n"
    return sumario

if __name__=="__main__":
    text = input("Text: ")
    k=3
    try:
        k = int(sys.argv[1:][0])
    except:
        pass
    try:
        res = summarizer(text, k)
        print(f"\nResult: \n\n{res}")
    except:
        print("Input error")