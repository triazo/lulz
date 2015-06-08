#!/usr/bin/python3

import socket
import random
import time
import threading
import subprocess

global ircsock

# currently configured for rpisec network
server = "irc.rpis.ec"
channel = "#rpisec"
botnick = "Cowbot"

def ping():
    ircsock.send("PONG :Pong\n")


def cowsay(s):
    try:
        s = subprocess.check_output(['cowsay']+s.split(' ')).decode('UTF-8')
        for line in s.split('\n'):
            ircsock.send("PRIVMSG "+ channel +" : "+ line +"\n")
            time.sleep(1)
    except Exception as e:
        ircsock.send("PRIVMSG " + channel + " : Cowbot failed: " + str(e) + "\n")

class MySock(socket.socket):
    def send(self, s):
        self.sendall(bytes(s, "UTF-8"))


def stripnick(n):
    if n[0] == '~' or n[0] == '@':
        return n[1:].strip()
    return n


def main():
    global ircsock
    ircsock = MySock(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, 6667))

    ircsock.send("NICK "+ botnick +"\n")
    ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Test bot for fruit matrix")

    ircsock.send("JOIN "+ channel +"\n")

    joined = False
    while True:
        ircmsg = ircsock.recv(2048).decode('UTF-8')
        if 'PING' in ircmsg:
            ping()

        print(ircmsg, end='')

        if not joined and 'MODE' in ircmsg:
            ircsock.send("JOIN "+ channel +"\n")
            joined = True

        if 'cowsay ' in ircmsg.lower():
            cowsay(ircmsg[ircmsg.lower().index('cowsay ')+7:])


if __name__ == "__main__":
    main()
