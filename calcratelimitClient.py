import urllib

from hashlib import sha512
import random, string

class calcRatelimitClient(object):
	""" Client for calcRatelimit endpoint """

	def __init__(self):
		self.hashPrefix = '1337'
		self.tokenEndpoint = 'localhost'
		self.APIEndpoint = 'localhost'

	def setTokenEndpoint(self, url):
		self.tokenEndpoint = url

	def setAPIEndpoint(self, url):
		self.APIEndpoint = url

	def generateAdditionalToken(self, token):
		''' Generate additional token such that sha512(token + additionalToken) starts with the right prefix '''

		generatedHash = 'foobar'

		while generatedHash[:len(self.hashPrefix)] != self.hashPrefix:
			additionalToken = ''.join(random.choice(string.lowercase) for i in range(25))

			generatedHash = sha512(token + additionalToken).hexdigest()

		return additionalToken

	def performAPICall(self):
		''' Perform API call using calculation endpoint '''

		data = urllib.urlopen(self.tokenEndpoint)
		token = data.read().strip("\n\r")

		additionalToken = self.generateAdditionalToken(token)

		data = urllib.urlopen(self.APIEndpoint + "?token="+token+"&additionalToken="+additionalToken)
		result = data.read()

		return result

ratelimitClient = calcRatelimitClient()

ratelimitClient.setTokenEndpoint("http://node/tokenEndpoint.py")
ratelimitClient.setAPIEndpoint("http://node/apiEndpoint.py")

print ratelimitClient.performAPICall()
