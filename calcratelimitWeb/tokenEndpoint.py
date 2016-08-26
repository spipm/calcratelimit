#!/usr/bin/env python
# 

import cgi
import sqlite3
from os import urandom, environ

# print header
print "Content-Type: text/plain;charset=utf-8"
print ""

# open token db
conn = sqlite3.connect('../calcratelimitTokens.db')
c = conn.cursor()

# get ip
ip = environ["REMOTE_ADDR"]

# remove any old tokens
parameters = (ip,)
c.execute("DELETE from tokens WHERE ip = ?", parameters)
conn.commit()

# generate token
tokenBytes = urandom(64)
token = tokenBytes[:16].encode('base64').replace('=','').replace('+','').replace('/','')

# save token
parameters = (token,ip)
c.execute("INSERT INTO tokens (token,ip) VALUES (?,?)", parameters)
conn.commit()
conn.close()

# send token to user
print token