from scipy.io import wavfile as wf

class AudioControl:
	"Functions to process audio output"

	def __init__(self):
		self.gainfactor = 1
		self.gainfactorat0 = 0.25
		self.gainfactorat1 = 1.0
		self.gaincontrol = "polynomial"
		self.linearP = 0
		self.linearO = 0
		self.polynomialA = 0
		self.polynomialC = 0
		AudioControl.startVariables(self)

	def processAndSave(self, filename, samplerate, audiodata, audiomax):
		audiodata = audiodata / (audiomax * audiodata.shape[0])
		for c in range(audiodata.shape[0]):
			print("-- Saving channel " + str(c) + "          ", end="\r")
			wf.write(filename + "_" + str(c) + ".wav", samplerate, audiodata[c])

	def updateDopplerSampleAmplitude(self, a):
		return a * self.gainfactor

	#Adjusting audio level depending on infected population ratio
	def updateAudioGain(self, infectedratio):
		f = 0
		if self.gaincontrol == "linear":
			f = infectedratio * self.linearP + self.linearO
		elif self.gaincontrol == "polynomial":
			f = infectedratio * infectedratio * self.polynomialA + self.polynomialC
		self.gainfactor = f

	#Starting variables to store functions coefficients
	def startVariables(self):
		self.linearP = self.gainfactorat1 - self.gainfactorat0
		self.linearO = self.gainfactorat0
		self.polynomialA = self.gainfactorat1 - self.gainfactorat0
		self.polynomialC = self.gainfactorat0

	def __str__(self):
		return "------------------------------------\n" + \
				"------- infectoD o p p l e r -------\n" + \
				"- rvalla.github.io/infectoDoppler --\n" + \
				"- github.com/rvalla/infectoDoppler -\n" + \
				"---------- Audio Control -----------\n" + \
				"---------- Version: 0.95 -----------\n" + \
				"-- Gain factor: " + str(self.gainfactor) + "\n"
