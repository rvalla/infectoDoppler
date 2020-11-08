import os
import time as tm
import random as rd
import numpy as np
import pandas as pd
import json as js
from audiocontrol import AudioControl
from doppler import Doppler
from virus import Virus
from response import Response
from visualization import Visualization

class infectoDoppler():
	"Configuring and running simulations to build a version"

	configdata = None
	ppath = None
	vpath = None
	filelist = None
	vname = None
	starttime = 0
	population = 0 #Sounds population size
	infectedratio = 0.0 #Infected population ratio
	days = 0 #Duration for the simulation in days
	daysize = 0 #Day duration in audio samples
	caseszero = 0 #Number of infected objects for the first day
	basecontacts = 0 #Default number of contacts
	response = False
	dp = []
	ac = AudioControl()
	samplerate = None
	channels = 0
	audiodata = None
	audiolength = 0 #Output audio length in samples
	audiomax = 0.0 #Here we save the maximum level of the audio signal
	vr = Virus()
	rp = Response()
	vz = Visualization()
	infectedset = set()
	recoveredset = set()
	infectiondata = None
	epidemic = None
	infectedsounds = None

	def __init__(self, configpath):
		infectoDoppler.configdata = js.load(open(configpath))
		infectoDoppler.setConfig(infectoDoppler.configdata)
		infectoDoppler.infectiondata = infectoDoppler.getInfectionDataList()
		infectoDoppler.epidemic = infectoDoppler.getEpidemicDataframe()
		infectoDoppler.infectedsounds = infectoDoppler.getInfectedSoundsDataframe()
		print(self)
		infectoDoppler.buildPopulation(infectoDoppler.filelist)
		infectoDoppler.startInfections(infectoDoppler.caseszero, infectoDoppler.population)
		infectoDoppler.starttime = tm.time()
		infectoDoppler.saveFirstDay()
		infectoDoppler.run()

	#Building a new infecto Doppler version
	def run():
		print("                                ", end="\r")
		for d in range(infectoDoppler.days):
			print("-- Simulating day: " + str(d), end="\r")
			infectoDoppler.mergeInfections(d)
			infectoDoppler.simulateDay(d)
			infectoDoppler.updateInfectedRatio()
			infectoDoppler.ac.updateAudioGain(infectoDoppler.infectedratio)
			infectoDoppler.saveDay(d)
		print("-- Simulation is finished!       ", end="\n")
		print("-- Time needed for building this version: " + \
				infectoDoppler.getSimulationTime(infectoDoppler.starttime, tm.time()))
		infectoDoppler.saveSimulationData()
		infectoDoppler.saveVersion()
		infectoDoppler.plotData()
		print("-- Plotting version's data...", end="\r")
		infectoDoppler.vz.simulationVisualization(infectoDoppler.vname, infectoDoppler.vpath + "charts/", \
		 					infectoDoppler.epidemic, infectoDoppler.audiodata, infectoDoppler.samplerate, \
							infectoDoppler.population, infectoDoppler.days)
		print("-- New version of infecto Doppler saved!", end="\n")

	#Merging audio data from infected doppler objects
	def mergeInfections(d):
		for s in range(infectoDoppler.daysize):
			firstsample = d * infectoDoppler.daysize
			for o in infectoDoppler.infectedset:
				infectoDoppler.sumAmplitude(infectoDoppler.dp[o], firstsample + s)
				infectoDoppler.evolInfection(infectoDoppler.dp[o], d)
			infectoDoppler.updateInfectedSet()

	#Adding doppler object sample to sound stream
	def sumAmplitude(doppler, s):
		amplitude = infectoDoppler.ac.updateDopplerSampleAmplitude(doppler.audiodata[doppler.infectioncourse])
		infectoDoppler.audiodata[doppler.dchannel][s] += amplitude
		infectoDoppler.checkAudioMax(infectoDoppler.audiodata[doppler.dchannel][s])

	#Saving de maximum amplitude value to normalize before saving
	def checkAudioMax(a):
		if infectoDoppler.audiomax < abs(a):
			infectoDoppler.audiomax = abs(a)

	#Simulating an epidemic day
	def simulateDay(d):
		actualinfected = infectoDoppler.infectedset.copy()
		for o in actualinfected:
			infectoDoppler.spread(infectoDoppler.dp[o], d)
		infectoDoppler.rp.checkResponse(d)

	def updateInfectedSet():
		infectoDoppler.infectedset = infectoDoppler.infectedset.difference(infectoDoppler.recoveredset)
		infectoDoppler.recoveredset = set()

	#Executing the virus spread
	def spread(idoppler, d):
		n = idoppler.getDayContactsCount(infectoDoppler.basecontacts, infectoDoppler.rp.getIsolationFactor())
		c = rd.sample(range(0, infectoDoppler.population - 1), n)
		for i in range(len(c)):
			infectoDoppler.decideInfection(infectoDoppler.dp[c[i]], d)

	def decideInfection(doppler, d):
		t = rd.random()
		if t < infectoDoppler.vr.infectionthreshold:
			infectoDoppler.checkImmunity(doppler, infectoDoppler.vr.immunityperiod, d)
			if (doppler.hasimmunity == False and doppler.isinfected == False):
				infectoDoppler.setInfection(doppler, d)

	def setInfection(doppler, d):
		doppler.infectionnumber += 1
		doppler.isinfected = True
		doppler.infectiondate = d
		infectoDoppler.infectiondata[1] += 1
		infectoDoppler.infectiondata[2] += 1
		infectoDoppler.infectiondata[doppler.dchannel + 3] += 1
		infectoDoppler.infectedset.add(doppler.dnumber)

	def evolInfection(doppler, d):
		doppler.infectioncourse += 1
		if doppler.infectioncourse == doppler.size:
			infectoDoppler.setCure(doppler, d)

	def setCure(doppler, d):
		doppler.isinfected = False
		doppler.wasinfected = True
		doppler.hasimmunity = True
		doppler.enddate = d
		doppler.infectioncourse = 0
		infectoDoppler.infectiondata[2] -= 1
		infectoDoppler.infectiondata[doppler.dchannel + 3] -= 1
		infectoDoppler.recoveredset.add(doppler.dnumber)
		infectoDoppler.saveInfection(doppler)

	def startInfections(c, p):
		l = rd.sample(range(0, p - 1), c)
		for i in range(c):
			infectoDoppler.setInfection(infectoDoppler.dp[l[i]], 1)
		infectoDoppler.updateInfectedRatio()
		print("-- Cases zero injected!", end="\n")

	def checkImmunity(doppler, period, d):
		if doppler.hasimmunity == True:
			if d > doppler.enddate + period:
				doppler.hasimmunity = False

	def updateInfectedRatio():
		infectoDoppler.infectedratio = infectoDoppler.infectiondata[2] / infectoDoppler.population

	def setConfig(data):
		infectoDoppler.ppath = data["pPath"]
		infectoDoppler.vpath = data["vPath"]
		infectoDoppler.vname = data["name"]
		infectoDoppler.days = data["days"]
		infectoDoppler.daysize = data["daySize"]
		infectoDoppler.caseszero = data["casesZero"]
		infectoDoppler.basecontacts = data["baseContacts"]
		infectoDoppler.vr.infectionthreshold = data["infectionThreshold"]
		infectoDoppler.vr.immunityperiod = data["immunityPeriod"]
		infectoDoppler.response = data["response"]
		infectoDoppler.rp.responseisactive = False
		infectoDoppler.rp.responsestart = data["responseStart"]
		infectoDoppler.rp.actionsperiod = data["actionsPeriod"]
		infectoDoppler.rp.isolationfactor = data["isolationFactor"]
		infectoDoppler.samplerate = data["sampleRate"]
		infectoDoppler.channels = data["channels"]
		infectoDoppler.audiolength = infectoDoppler.days * infectoDoppler.daysize
		infectoDoppler.audiodata = np.zeros((infectoDoppler.channels, infectoDoppler.audiolength), dtype="float32")
		infectoDoppler.ac.gaincontrol = data["gainControl"]
		infectoDoppler.ac.gainfactorat0 = data["gainFactorAt0"]
		infectoDoppler.ac.gainfactorat1 = data["gainFactorAt1"]
		infectoDoppler.filelist = os.listdir(data["pPath"])
		infectoDoppler.cleanFileList(infectoDoppler.filelist)
		infectoDoppler.filelist.sort()
		if data["population"] > 0 and data["population"] <= len(infectoDoppler.filelist):
			infectoDoppler.population = data["population"]
		else:
			infectoDoppler.population = len(infectoDoppler.filelist)

	def buildPopulation(filelist):
		for f in range(infectoDoppler.population):
			print("-- Loading sound object " + str(f), end="\r")
			infectoDoppler.dp.append(Doppler(f, infectoDoppler.channels, infectoDoppler.ppath, filelist[f]))
		print("-- Sound objects loaded!          ", end="\n")

	def saveFirstDay():
		row = pd.DataFrame([(0,0,0,0,0,0,0,0.0)], columns = infectoDoppler.epidemic.columns)
		infectoDoppler.epidemic = pd.concat([infectoDoppler.epidemic, row])

	def saveDay(d):
		infectoDoppler.infectiondata[0] = d + 1
		infectoDoppler.infectiondata[len(infectoDoppler.infectiondata) - 1] = infectoDoppler.infectedratio
		row = pd.DataFrame([infectoDoppler.infectiondata[:]], columns = infectoDoppler.epidemic.columns)
		infectoDoppler.epidemic = pd.concat([infectoDoppler.epidemic, row])

	def saveInfection(doppler):
		row = pd.DataFrame([[doppler.dnumber, doppler.name, doppler.infectionnumber, doppler.dchannel, \
							doppler.contactfactor, doppler.infectiondate, doppler.enddate, doppler.size]], \
							columns=infectoDoppler.infectedsounds.columns)
		infectoDoppler.infectedsounds = pd.concat([infectoDoppler.infectedsounds, row])

	def saveVersion():
		filename = infectoDoppler.vpath + "audio/" + infectoDoppler.vname
		infectoDoppler.ac.processAndSave(filename, infectoDoppler.samplerate, infectoDoppler.audiodata, \
										infectoDoppler.audiomax)

	def plotData():
		return 1

	def cleanFileList(filelist):
		f = 0
		while (f < len(filelist)):
			if filelist[f].startswith("."):
				del filelist[f]
			else:
				f += 1

	def getInfectionDataList():
		l = []
		l.append(0)
		l.append(0)
		l.append(0)
		for c in range(infectoDoppler.channels):
			l.append(0)
		l.append(0.0)
		return l

	def saveSimulationData():
		infectoDoppler.epidemic.set_index("Day", inplace = True)
		infectoDoppler.epidemic.to_csv(infectoDoppler.vpath + "data/" + infectoDoppler.vname + "_ep.csv")
		infectoDoppler.infectedsounds.set_index("Number", inplace = True)
		infectoDoppler.infectedsounds.to_csv(infectoDoppler.vpath + "data/" + infectoDoppler.vname + "_inf.csv")

	def getInfectedSoundsDataframe():
		columns = ["Number", "Name", "Infections", "Channel", "CF", "I start", "I end", "Size"]
		p = pd.DataFrame(columns=columns)
		p.index = p["Number"]
		p.index.name = "Number"
		return p

	def getEpidemicDataframe():
		columns = []
		columns.append("Day")
		columns.append("Total infected")
		columns.append("Infected")
		for c in range(infectoDoppler.channels):
			columns.append("Infected in " + str(c))
		columns.append("Infected ratio")
		p = pd.DataFrame(columns=columns)
		p.index = p["Day"]
		p.index.name = "Day"
		return p

	#Calculating time needed for simulation to finish...
	def getSimulationTime(startTime, endTime):
		time = endTime - startTime
		formatedTime = infectoDoppler.formatTime(time)
		return formatedTime

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
				"------------ infectoDoppler --------------\n" + \
				"------------- Version: 0.95 --------------\n" + \
				"-- Version name: " + str(infectoDoppler.vname) + "\n" + \
				"-- Channels: " + str(infectoDoppler.channels) + "\n" + \
				"-- Population: " + str(infectoDoppler.population) + "\n" + \
				"-- Days: " + str(infectoDoppler.days) + "\n" + \
				"-- Day size: " + str(infectoDoppler.daysize) + "\n"
