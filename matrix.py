#!/usr/bin/python3

import socket
import random
import time
import threading

global nicks
global ircsock

server = "irc.freenode.net"
channel = "#fruit"
botnick = "Fruitbot_31337"

fruits = open('/tmp/fruits.txt', 'r').read().split('\n')

good_nicks = {'triazo', 'droghio', 'ChanServ', 'not-inept', botnick, 'fruit_bat'}

columns = 17
colheights = []
cols = []

for i in range(columns):
    colheights.append(0)
    cols.append("")

def ping():
  ircsock.send("PONG :Pong\n")

def sendmsg(chan , msg):
  ircsock.send("PRIVMSG "+ chan +" :"+ msg +"\n")


def getfruitline():

    while min(colheights) <= getfruitline.curline:
        space = random.randint(2,12)
        fruit = random.sample(fruits, 1)[0]
        i = colheights.index(min(colheights))
        cols[i]+=(fruit + " "*space)
        colheights[i] += (len(fruit)+space)

    line = ''

    for c in cols:
        line += c[getfruitline.curline]
        line += '   '

    getfruitline.curline+=1
    return line

getfruitline.curline = 0

class MySock(socket.socket):
    def send(self, s):
        self.sendall(bytes(s, "UTF-8"))


def fruitloop():
    time.sleep(15)
    while True:
        time.sleep(2)
        if len(nicks - good_nicks) != 0 :
            print(nicks-good_nicks)
            ircsock.send("PRIVMSG "+ channel +" :"+ getfruitline() +"\n")


def stripnick(n):
    if n[0] == '~' or n[0] == '@':
        return n[1:].strip()
    return n

def header(msg):
    return ''.join(msg.split(':')[:2])

def main():
    global ircsock
    ircsock = MySock(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, 6667))

    ircsock.send("NICK "+ botnick +"\n")
    ircsock.send("USER "+ botnick +" "+ botnick +" "+ botnick +" :Test bot for fruit matrix")

    ircsock.send("JOIN "+ channel +"\n")

    global nicks
    nicks = set({})

    fruitthread = threading.Thread(target=fruitloop, args=())
    fruitthread.start()

    joined = False
    initnicks = 0
    while True:
        ircmsg = ircsock.recv(2048).decode('UTF-8')
        #ircmsg = ircmsg.strip('\n').strip('\r')
        if 'PING' in ircmsg:
            ping()
        print(ircmsg, end='')

        if not joined and 'MODE' in ircmsg:
            ircsock.send("JOIN "+ channel +"\n")

        elif channel in ircmsg and initnicks == 1:
            initnicks += 1
            nicks = set([stripnick(n) for n in ircmsg.split(':')[2].split(' ')])
            print(nicks)

        elif channel in ircmsg:
            initnicks += 1

        if 'JOIN' in header(ircmsg):
            nick = stripnick(ircmsg.split('!')[0].split(':')[1])
            print("%s joined"%nick)
            nicks = nicks | {nick}
            print(nicks)

        if 'QUIT' in header(ircmsg) or 'PART' in header(ircmsg):
            nicks = nicks - {stripnick(ircmsg.split('!')[0].split(':')[1]) }
            print(nicks)

        if 'NICK' in header(ircmsg) and initnicks > 1:
            nicks = nicks - { stripnick(ircmsg.split('!')[0].split(':')[1]).strip() }
            nicks = nicks | { stripnick(ircmsg.split(':')[2]).strip() }
            print(nicks)


if __name__ == "__main__":
    main()


#    :orwell.freenode.net 353 Fruitbot_24324 = #fruit :Fruitbot_24324 Fruitbot_242324 droghio triazo @ChanServ
