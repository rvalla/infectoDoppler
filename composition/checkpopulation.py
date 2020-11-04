import os
import re

class CheckPopulation():
	"Methos to check sounds population files"

	def __init__(self, ppath):
		self.filelist = os.listdir(ppath)
		CheckPopulation.cleanFileList(self.filelist)
		self.filelist.sort()

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

	def __str__(self):
		return "------------------------------------\n" + \
				"------- infectoD o p p l e r -------\n" + \
				"- rvalla.github.io/infectoDoppler --\n" + \
				"- github.com/rvalla/infectoDoppler -\n" + \
				"-- Tool for sounds files checking  -\n" + \
				"---------- Version: 0.90 -----------\n"
