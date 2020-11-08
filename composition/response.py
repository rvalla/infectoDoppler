class Response:
	"Social response to the epidemic outbreak"

	def __init__(self):
		self.responseisactive = None
		self.responsestart = None
		self.actionsperiod = None
		self.isolationfactor = None

	def getIsolationFactor(self):
		if self.responseisactive == True:
			return self.isolationfactor
		else:
			return 1.0

	def checkResponse(self, d):
		if d == self.responsestart:
			Response.setResponse(self, True)
		elif d == self.responsestart + self.actionsperiod:
			Response.setResponse(self, False)

	def setResponse(self, status):
		self.responseisactive = status

	def __str__(self):
		return "------------------------------------------\n" + \
				"---------- infectoD o p p l e r ----------\n" + \
				"- rodrigovalla.gitlab.io/infectodoppler --\n" + \
				"- gitlab.com/rodrigovalla/infectodoppler -\n" + \
				"--------------- Response -----------------\n" + \
				"------------- Version: 0.95 --------------\n" + \
				"-- Is response active?: " + str(Response.responseisactive) + "\n" + \
				"-- Response start day: " + str(Response.responsestart) + "\n" + \
				"-- Actions period: " + str(Response.actionsperiod) + "\n" + \
				"-- Isolation factor: " + str(Response.isolationfactor) + "\n"
