class Virus:
	"The virus that spreads and infect doppler sound objects"

	def __init__(self):
		self.infectionthreshold = 0.10
		self.immunityperiod = 360

	def __str__(self):
		return "------------------------------------\n" + \
				"------- infectoD o p p l e r -------\n" + \
				"- rvalla.github.io/infectoDoppler --\n" + \
				"- github.com/rvalla/infectoDoppler -\n" + \
				"-------------- Virus ---------------\n" + \
				"---------- Version: 0.90 -----------\n" + \
				"-- Infection threshold: " + str(self.infectionThreshold) + "\n" + \
				"-- Immunity period: " + str(self.immunityPeriod) + "\n"
