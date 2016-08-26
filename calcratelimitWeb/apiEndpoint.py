#!/usr/bin/env python
# 

import cgi
import sqlite3
from os import environ
from json import dumps
from hashlib import sha512


def getJSONSucessAPI():
	''' Some method that is executed when the client calculated a correct hash '''

	return "This is a succesful API call"


# set header
print "Content-Type: application/json;charset=utf-8"
print ""

# set error message
errorMessage = dumps({"error":"token error"})

# get token arguments
arguments = cgi.FieldStorage()
try:
	token = arguments['token'].value
	additionalToken = arguments['additionalToken'].value

	if len(token) < 20 or len(token) > 30 or len(additionalToken) < 20 or len(additionalToken) > 30:
		print errorMessage
		exit(0)
except:
	print errorMessage
	exit(0)

# connect to db
conn = sqlite3.connect('../calcratelimitTokens.db')
c = conn.cursor()

# get token from db
parameters = (environ["REMOTE_ADDR"],)
c.execute("SELECT token from tokens WHERE ip = ?", parameters)

# validate tokens
try:
	valueFromDB = c.fetchone()[0].strip("\n")

	if valueFromDB == token:
		testValue = sha512(valueFromDB + additionalToken).hexdigest()

		if testValue[:4] == '1337':
			result = getJSONSucessAPI()
			
		else:
			result = errorMessage
	else:
		result = errorMessage
except:
	result = errorMessage

# remove all tokens
c.execute("DELETE from tokens WHERE ip = ?", parameters)
conn.commit()
conn.close()


print "/**/" + result