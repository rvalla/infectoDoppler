import os
import re
from doppler import Doppler

class CheckPopulation():
	"Methos to check sounds population files"

	def __init__(self, ppath):
		self.filelist = os.listdir(ppath)
		CheckPopulation.cleanFileList(self.filelist)
		self.filelist.sort()
		self.population = len(self.filelist)
		self.dplist = []
		CheckPopulation.loadPopulation(self, ppath, self.dplist)
		self.samplerate = self.dplist[0].samplerate

	def checkMissingFiles(self):
		last = 1
		for i in range(len(self.filelist) - 1):
			filename = re.split("_|.w", self.filelist[i+1])
			actual = int(filename[1])
			if CheckPopulation.checkConsecutiveFiles(last, actual) == False:
				print(self.filelist[i+1])
			last = actual

	def checkConsecutiveFiles(a, b):
		if a == b - 1:
			return True
		else:
			return False

	def cleanFileList(filelist):
		f = 0
		while (f < len(filelist)):
			if filelist[f].startswith("."):
				del filelist[f]
			else:
				f += 1

	def loadPopulation(self, ppath, dpl):
		for f in range(self.population):
			dpl.append(Doppler(f, 4, ppath, self.filelist[f]))

	def getPopulationDuration(self):
		t = 0
		for d in range(len(self.dplist)):
			t += self.dplist[d].size / self.samplerate
		return CheckPopulation.formatTime(t)

	def formatTime(time):
		ms = ""
		minutes = time // 60
		seconds = time - minutes * 60
		seconds = round(seconds, 2)
		ms = "{:02d}".format(int(minutes))
		ms += ":"
		ms += "{:05.2f}".format(seconds)
		return ms

	def __str__(self):
		return "------------------------------------------\n" + \
				"---------- infectoD o p p l e r ----------\n" + \
				"- rodrigovalla.gitlab.io/infectodoppler --\n" + \
				"- gitlab.com/rodrigovalla/infectodoppler -\n" + \
				"----- Tools for sound files checking -----\n" + \
				"------------- Version: 0.95 --------------\n"
