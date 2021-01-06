import telebot
from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerUser, InputPeerChannel
from telethon import TelegramClient, sync, events


class PushNotifications:
    apiId = 'APIID'
    apiHash = 'APIHASH'
    token = 'TELEGRAMTOKEN'
    phone = 'YOUR_NUMBER'
    notificationUsers = []
    receivers = []

    def __init__(self, debug = True):
        self.debug = debug
        self.client = TelegramClient('session', self.apiId, self.apiHash)
        self.client.connect()

        if not self.client.is_user_authorized():

            self.client.send_code_request(self.phone)

            # signing in the client
            self.client.sign_in(self.phone, input('Enter the code: '))

        self.me = self.client.get_me()

    def getReceivers(self, notificationUsers):
        receivers = []
        for userName in notificationUsers:
            receivers.append(self.client.get_entity(userName))
        return receivers

    def sendMessageToMe(self, notificationUsers, message):
        message = 'Send to {}:\n{}'.format(('me', notificationUsers)[len(notificationUsers) > 0], message)
        print(message)

        try:
            self.client.send_message(self.me, message, parse_mode='html')
        except Exception as e:
            print(e)

    def sendMessage(self, notificationUsers, message):
        self.sendMessageToMe(notificationUsers, message)
        if self.debug:
          return
        receivers = self.getReceivers(notificationUsers)
        try:
            for receiver in receivers:
                self.client.send_message(receiver, message, parse_mode='html')
        except Exception as e:
            print(e)
