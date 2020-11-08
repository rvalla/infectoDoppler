import warnings
import random as rd
from scipy.io import wavfile as wf

warnings.simplefilter("ignore", wf.WavFileWarning)

class Doppler:
	"Each of the sound objects to build an InfectoDoppler version"

	def __init__(self, n, vchannels, fpath, filename):
		self.name = filename
		self.dnumber = n
		self.infectionnumber = 0
		self.dchannel = rd.randint(0, vchannels - 1)
		self.contactfactor = rd.triangular(0.5, 1.5, 1)
		self.hasimmunity = False
		self.isinfected = False
		self.wasinfected = False
		self.infectioncourse = 0
		self.infectiondate = 0
		self.enddate = 0
		self.samplerate, self.audiodata = wf.read(fpath + filename)
		self.size = self.audiodata.size

	def getDayContactsCount(self, bc, ifactor):
		n = rd.triangular(0, bc, round(bc/2)) * self.contactfactor * ifactor
		return round(n)

	def __str__(self):
		return "------------------------------------------\n" + \
				"---------- infectoD o p p l e r ----------\n" + \
				"- rodrigovalla.gitlab.io/infectodoppler --\n" + \
				"- gitlab.com/rodrigovalla/infectodoppler -\n" + \
				"---------------- Doppler -----------------\n" + \
				"------------- Version: 0.95 --------------\n" + \
				"-- Channel: " + self.dchannel + "\n" + \
				"-- Contact factor: " + str(self.contactfactor) + "\n" + \
				"-- Has immunity?: " + str(self.hasimmunity) + "\n" + \
				"-- Is infected?: " + str(self.isinfected) + "\n"
