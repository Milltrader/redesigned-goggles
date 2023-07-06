import random
import string
import sys
words = ['python', 'java', 'swift', 'javascript']
correct = random.choice(words)
hidden = list('-' * len(correct))
attempts_count = 8
letters_bank = []
repeating_words = []
wins_counter = 0
loses_counter = 0

def game():
    global letters_bank, attempts_count, hidden, repeating_words

    print("".join(hidden))
    x = input(f'Input a letter: ')
    if len(x) == 1 and x in string.ascii_lowercase:
        if x in correct and x not in repeating_words:
            repeating_words.append(x)
            for i in range(len(correct)):
                if correct[i] == x:
                    hidden[i] = x

        elif x in repeating_words:
            print("You've already guessed this letter.")
        else:
            repeating_words.append(x)
            attempts_count -= 1
            print(f"That letter doesn't appear in the word.  #{attempts_count} attempts")

    elif len(x) != 1:
        print('Please, input a single letter.')

    elif x not in string.ascii_lowercase:
        print('Please, enter a lowercase letter from the English alphabet.')


def menu():
    global wins_counter, loses_counter, attempts_count, letters_bank, hidden, repeating_words, correct
    while True:
        print(f'H A N G M A N  # {attempts_count} attempts')

        menu_text = input('Type "play" to play the game, "results" to show the scoreboard, and "exit" to quit:')
        if menu_text == 'play':
            print()
            correct = random.choice(words)
            hidden = list('-' * len(correct))
            attempts_count = 8
            letters_bank = []
            repeating_words = []
            start_and_finish()
        elif menu_text == 'results':
            print(f'You won: {wins_counter} times.\n'
                  f'You lost: {loses_counter} times.')
            menu()
        elif menu_text == 'exit':
            sys.exit()
        else:
            menu()


def start_and_finish():
    global wins_counter, loses_counter
    while attempts_count != 0:
        if '-' not in hidden:
            print(f'You guessed the word {"".join(hidden)}!')
            print('You survived!')
            wins_counter += 1
            menu()
        game()
    else:
        print("\nYou lost!")
        loses_counter += 1
        menu()

menu()