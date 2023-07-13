import nltk
from collections import Counter
import operator
import random
import re
x = 0
user_input = input()
with open(user_input, "r", encoding="utf-8") as f:
    content = f.read()
tokenized_words = nltk.WhitespaceTokenizer().tokenize(content)
starting = [i for i in tokenized_words if re.match(r"^[A-Z][^\.\!\?]*?$", i) != None]
body = [i for i in tokenized_words if re.match(r"^[a-z]*?$", i) != None]
ending = [i for i in tokenized_words if re.match(r"[A-Za-z]*[\.!\?\;]$", i) != None]
words_counter = 0
sentences_counter = 0
sentence = []

def functional():
    global word, sentence, x
    word = random.choice(tokenized_words)
    bigrams = nltk.bigrams(tokenized_words)
    list_bigrams = list(bigrams)
    obj1_dictionary = {}

    for head, tail in list_bigrams:
        obj1_dictionary.setdefault(head, []).append(tail)
    frequency = Counter(obj1_dictionary[word])

    wordlist_sorted = sorted(frequency.items(), key=operator.itemgetter(1), reverse=True)
    wordlist_sorted
    names = [i[0] for i in wordlist_sorted]
    probs = [i[1] for i in wordlist_sorted]
    word = random.choices(names, probs)[0]
    if word in starting and len(sentence) == 0:
        sentence.append(word)
    elif word not in starting and len(sentence) == 0:
        pass

    elif word in starting and word in ending:
        pass
    elif word in ending and len(sentence) >= 4:
        sentence.append(word)
        x = 1
    elif word in ending and len(sentence) < 5:
        sentence.append(word)

    else:
        sentence.append(word)



for sent in range(10):

    while x == 0:
        functional()

    print(" ".join(sentence))
    x = 0
    words_counter = 0
    sentences_counter = 0
    sentence = []
f.close()



