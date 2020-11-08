class Virus:
	"The virus that spreads and infect doppler sound objects"

	def __init__(self):
		self.infectionthreshold = 0.10
		self.immunityperiod = 360

	def __str__(self):
		return "------------------------------------------\n" + \
				"---------- infectoD o p p l e r ----------\n" + \
				"- rodrigovalla.gitlab.io/infectodoppler --\n" + \
				"- gitlab.com/rodrigovalla/infectodoppler -\n" + \
				"----------------- Virus ------------------\n" + \
				"------------- Version: 0.95 --------------\n" + \
				"-- Infection threshold: " + str(self.infectionThreshold) + "\n" + \
				"-- Immunity period: " + str(self.immunityPeriod) + "\n"
