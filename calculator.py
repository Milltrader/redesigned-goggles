import string
import sys
import re

user_input = ''
commands = ("/exit", "/help")
Operators = set(['+', '-', '*', '/', '(', ')', '^'])  # collection of Operators
Priority = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}  # dictionary having priorities of Operators
split_symbols = r'(\^|\-|\*|\/|\+|\(|\))'

class InvalidExpression(Exception):
    pass


class UnknownCommand(Exception):
    pass


def exceptions(x):
    try:
        if x in commands or (x == ''):
            return 1
        elif len(user_input.split()) == 1 and user_input.endswith(('1','2','3','4','5','6','7','8','9','0')):
            return 1
        if x.startswith('/') and (x not in commands):
            raise UnknownCommand
        elif all(char not in x for char in Operators) \
                or x.endswith(('-','+')) \
                or any(char.isalpha() for char in x)\
                or '(' in x and ')' not in x\
                or ')' in x and '(' not in x\
                or re.search(r'\*{2,}', x)\
                or re.search(r'/{2,}', x):
            raise InvalidExpression
        else:
            return 1

    except UnknownCommand:
        print("Unknown command")
    except InvalidExpression:
        print("Invalid expression")


def action(numbers):
    numbers_cleared = []

    for i in numbers:
        if ('-' in i and len(i) % 2 == 0 and i[1] not in string.digits) or ('+' in i):
            numbers_cleared.append('+')
        else:
            numbers_cleared.append(i)

    return numbers_cleared





def infixToPostfix(expression):
    stack = []  # initialization of empty stack
    output = []
    for character in expression:

        if character not in Operators:  # if an operand append in postfix expression
            output.append(character)
        elif character == '(':  # else Operators push onto stack
            stack.append('(')
        elif character == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != '(' and Priority[character] <= Priority[stack[-1]]:
                output += stack.pop()
            stack.append(character)
    while stack:
        output += stack.pop()
    stack_result = []
    result = ''
    for character in output:

        if character not in Operators and character not in var_dict:
            stack_result.append(character)
        elif character in var_dict:
            stack_result.append(var_dict[character])
        elif character in Operators:
            b = stack_result.pop()
            a = stack_result.pop()
            if character == '+':
                stack_result.append(int(a) + int(b))
            elif character == '-':
                stack_result.append(int(a) - int(b))
            elif character == '*':
                stack_result.append(int(a) * int(b))
            elif character == '/':
                stack_result.append(int(a) / int(b))
            elif character == '^':
                stack_result.append(int(a) ** int(b))
    result = stack_result[-1]

    return result





var_dict = {}


def variable(user_input):
    global var_dict
    user_input2 = []

    if user_input in var_dict :
        print(var_dict[user_input])

        main()

    if '=' in user_input:

        y = user_input.split('=')
        if user_input.count('=') > 1:
            print('Invalid assignment')
            pass
        x = [item.strip() for item in y]

        if any(character.isdigit() for character in x[0]):
            print('Invalid identifier')
            pass
        elif any(character.isalpha() for character in x[-1]):
            right_side = x[-1]
            if right_side in var_dict:
                right_side_value = var_dict[right_side]
                x[-1] = right_side_value  # Replace right-side variable with its value

                # Replace any occurrences of the right-side variable in previously assigned values
                for key, value in var_dict.items():
                    var_dict[key] = value.replace(right_side, right_side_value)

                pass
            else:
                print('Invalid assignment')
                pass
        var_dict[x[0]] = x[-1].replace(r'*=', '')

        main()


    for item in user_input:
        if item.isalpha() and item in var_dict:
            user_input2.append(var_dict[item])
        elif user_input.startswith('/'):
            user_input2 = user_input
        elif item.isalpha() and item not in var_dict:
            print('Unknown variable')
            break
        else:
            user_input2.append(item)

    return ''.join(user_input2)

def main():

    global user_input

    while True:
        user_input = input().rstrip()
        user_input = variable(user_input)

        if exceptions(user_input):
            if user_input == "/exit":
                print("Bye!")
                sys.exit()
            elif user_input == "":
                continue
            elif user_input == "/help":
                print("The program calculates the sum of numbers")
                continue
            if user_input[0] == '+':
                user_input = user_input[1:]
            numbers = re.split(split_symbols, user_input)
            numbers = [s.strip() for s in numbers if s.strip() != '']
            temp = action(numbers)
            print(infixToPostfix(temp))

if __name__ == "__main__":
    main()

