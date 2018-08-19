from bs4 import BeautifulSoup
import telepot
import requests
import time
import os
import sys
import glob

os.chdir(sys.path[0])

known_chat_ids = [123456789,]
token = "telegram_token"
passphrase = "passphrase"


def get_detection_status():
    status = requests.get('http://localhost:8080/0/detection/status')
    soup = BeautifulSoup(status.text, 'html.parser')
    status_line = soup.find('body').get_text()
    return status_line


def get_files(directory):
    files = []
    for root, _, filenames in os.walk(directory):
        print(root, filenames)
        for filename in filenames:
            filepath = os.path.join(root, filename)
            size = os.path.getsize(filepath) / 1048576.0  # MBs
            filestr = '/{0}\n{1} MB'.format(filename.split('.')[0], round(size, 2))
            files.append(filestr)

    return '\n'.join(files)


def handle(msg):
    chat_id = msg['chat']['id']
    command = msg['text']
    print(str(chat_id) + ' - ' + command)

    if command == passphrase:
        known_chat_ids.append(chat_id)

    if not chat_id in known_chat_ids:
        return

    if command.startswith('/ping'):
        bot.sendChatAction(chat_id, 'typing')
        bot.sendMessage(chat_id, 'pong')

    elif command.startswith('/snapshot'):
        bot.sendChatAction(chat_id, 'upload_photo')
        lastsnap = 'lastsnap.jpg'
        requests.get('http://localhost:8080/0/action/snapshot')
        # No need to bot.sendPhoto as motion.conf will do that for us

    elif command.startswith('/motion_on'):
        bot.sendChatAction(chat_id, 'typing')
        requests.get('http://localhost:8080/0/detection/start')
        status = get_detection_status()
        bot.sendMessage(chat_id, status)

    elif command.startswith('/motion_off'):
        bot.sendChatAction(chat_id, 'typing')
        requests.get('http://localhost:8080/0/detection/pause')
        status = get_detection_status()
        bot.sendMessage(chat_id, status)

    elif command.startswith('/motion_status'):
        bot.sendChatAction(chat_id, 'typing')
        status = get_detection_status()
        bot.sendMessage(chat_id, status)

    elif command.startswith('/dir_'):
        bot.sendChatAction(chat_id, 'typing')
        files = get_files(command.replace('/dir_', ''))
        bot.sendMessage(chat_id, files)

    elif command.startswith('/delete '):
        bot.sendChatAction(chat_id, 'typing')
        partial_filename = command.replace('/delete ', '')
        filename, *_ = glob.glob('**/{}*'.format(partial_filename), recursive=True)
        os.remove(filename)
        bot.sendMessage(chat_id, 'Removed {}'.format(os.path.basename(filename)))

    elif command.startswith('/deletedir '):
        bot.sendChatAction(chat_id, 'typing')
        directory = command.replace('/deletedir ', '')
        deleted = ['Removed\n']
        for x in os.listdir(directory):
            filename = os.path.join(directory, x)
            os.remove(filename)
            deleted.append(x)
        bot.sendMessage(chat_id, '\n'.join(deleted))

    elif command.startswith('/'):
        filename, *_ = glob.glob('**{}*'.format(command), recursive=True)
        if filename.endswith('.jpg'):
            bot.sendChatAction(chat_id, 'upload_photo')
            bot.sendPhoto(chat_id, open(filename, 'rb'), caption=os.path.basename(filename))
        elif filename.endswith('.avi'):
            bot.sendChatAction(chat_id, 'upload_video')
            bot.sendVideo(chat_id, open(filename, 'rb'), caption=os.path.basename(filename))


bot = telepot.Bot(token)
print('bot is listening')
bot.message_loop(handle)

while True:
    time.sleep(10)
