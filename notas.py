from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super secret key'
socketio = SocketIO(app)

key = 'aaaaabbbbbabbbaabbababbaaababaab'
alphabet = 'abcdefghijklmnopqrstuvwxyz'
groupLen = 5


@app.route('/')
def hello_world():
    return render_template('index.html', async_mode=socketio.async_mode)


@socketio.on('encrypt')
def encrypt(data):
    msg = data['msg']
    mask = data['mask'].lower()

    encrypted = []

    for letter in msg:
        index = alphabet.find(letter)
        encrypted.append(key[index:index + groupLen])

    encr_str = ''.join(encrypted)

    if mask != '':
        mask_arr = list(filter(str.isalpha, mask))
    else:
        print('empty mask field')
        mask_arr = []
        for i in range(len(encr_str)):
            mask_arr.append(random.choice(alphabet))

    index = 0
    message = ''
    for letter in encr_str:
        if letter == 'a':
            message += mask_arr[index].lower()
        else:
            message += mask_arr[index].upper()
        index += 1

    emit('server_encr', {'encrypted': message})


@socketio.on('decrypt')
def decrypt(text):
    input_text = text['data']
    input_text_arr = list(filter(str.isalpha, input_text))
    input_text = ''.join(input_text_arr)
    output = ""
    numberOfGroups = int(len(input_text) / 5)
    for i in range(numberOfGroups):
        group = input_text[(i * groupLen): (i * groupLen) + groupLen]
        converted_group = []
        for letter in group:
            converted_group.append('a' if letter.islower() else 'b')
        output += alphabet[key.find(''.join(converted_group))]
    emit('server_decr', {'decrypted': output})


if __name__ == '__main__':
    socketio.run(app, debug=True)
