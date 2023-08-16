import requests
from bs4 import BeautifulSoup
import re
import argparse
import sys

'''
This program allows user to connect to context reverso translator and translate words through the terminal:
Example: python translator.py english french hello
Apart from giving showing the output directly, the code does also create a file named after the searched word with
the same content. The list of the supported languages is printed i the beginning and there is an option to
search for the translation to all the supported languages (python translator.py english all hello).
The code supports basic exceptions like the absence of the word and non-existent or not supported language.
'''

parser = argparse.ArgumentParser(description='calling translator')
parser.add_argument('source_language')
parser.add_argument('target_language')
parser.add_argument('word')

args = parser.parse_args()

headers = {'User-Agent': 'Mozilla/5.0'}
lang_list = ['Arabic', 'German', 'English', 'Spanish', 'French', 'Hebrew', 'Japanese', 'Dutch', 'Polish', 'Portuguese',
             'Romanian', 'Russian', 'Turkish']

print('''Hello, welcome to the translator. Translator supports:
1. Arabic
2. German
3. English
4. Spanish
5. French
6. Hebrew
7. Japanese
8. Dutch
9. Polish
10. Portuguese
11. Romanian
12. Russian
13. Turkish
''')


def intro():

    source_language = args.source_language
    target_language = args.target_language
    word_to_translate = args.word

    if target_language == 'all':
        target_language = 0

    return word_to_translate, source_language, target_language


def all_lang(word, language_in):
    for lang in lang_list:
        parsing(language_in, word, lang.lower())


def parsing(source_language, word, target_language):

    with open(f'{word}.txt', 'a', encoding='utf-8') as f:

        translations = []
        translations_sentence = []
        link_final = f'https://context.reverso.net/translation/{source_language}-{target_language}/{word}'
        r = requests.get(link_final, headers=headers)
        soup = BeautifulSoup(r.content, 'html.parser')

        error_check = soup.find_all('span', class_="wide-container message", limit=5)
        translation_word = soup.find_all('span', class_="display-term", limit=5)

        if error_check and not translation_word:
            print(f"Sorry, unable to find {word}")
            sys.exit()
        for word in translation_word:
            if len(translations) == 0:
                translations.append(word.text)

        translations = [re.sub(r'( f|m)$', '', i).strip() for i in translations]

        f.write(f'{target_language.capitalize()} Translations:\n')

        for i in translations:
            f.write(f'{i}\n')

        translation_sentence1 = soup.find_all('div', class_="src ltr", limit=5)
        translation_sentence2 = soup.find_all('div', class_=["trg ltr", "trg rtl arabic", "trg rtl"], limit=5)

        for word1, word2 in zip(translation_sentence1, translation_sentence2):
            translations_sentence.append(word1.text.strip())
            translations_sentence.append(word2.text.strip())
        f.write(f'\n{target_language.capitalize()} Example:\n')

        for i in range(0, len(translations_sentence), 2):
            if i < 1:
                f.write(f'{translations_sentence[i]}:\n')
                f.write(f'{translations_sentence[i+1]}\n\n\n')


def action():

    word, language_in, language_out = intro()

    if language_out == 0:
        all_lang(word, language_in)
        with open(f'{word}.txt', 'r', encoding='utf-8') as f1:
            for line in f1:
                print(line, end='')
    elif language_in.capitalize() not in lang_list:
        print(f"Sorry, the program doesn't support {language_in}")
    elif language_out.capitalize() not in lang_list:
        print(f"Sorry, the program doesn't support {language_out}")
        pass
    else:
        parsing(language_in, word, language_out)

        with open(f'{word}.txt', 'r', encoding='utf-8') as f1:
            for line in f1:
                print(line, end='')


if __name__ == "__main__":
    action()
