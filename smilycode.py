#!/usr/bin/python

import string
one = "☺"
zero = "☹"
inputstr = input("Enter string to encrypt: ")
shift =  int(input("Enter shift amount: "))

def caesar(plainText, shift):
    cipherText = ""
    for ch in plainText:
        if ch.isalpha():
            stayInAlphabet = ord(ch) + shift
            if stayInAlphabet > ord('z'):
                stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
            cipherText += finalLetter
        else:
            cipherText += ch
    print("Your ciphertext is: ", cipherText)
    return cipherText
                                            
shiftedstr = caesar(inputstr, shift)
newstr = ''
for c in shiftedstr:
    newstr+= bin(ord(c)+256)[3:].replace('0', zero).replace('1', one)

print(newstr)

