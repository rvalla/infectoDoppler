import os
import time as tm
import random as rd
import numpy as np
import pandas as pd
import json as js
from doppler import Doppler
from virus import Virus
from response import Response
from visualization import Visualization

class epidemicTest():
	"Configuring and running simulations to test model configuration"

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
	modecontacts = 0 #Default number of contacts
	response = False
	dp = []
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
		epidemicTest.configdata = js.load(open(configpath))
		epidemicTest.setConfig(epidemicTest.configdata)
		epidemicTest.infectiondata = epidemicTest.getInfectionDataList()
		epidemicTest.epidemic = epidemicTest.getEpidemicDataframe()
		epidemicTest.infectedsounds = epidemicTest.getInfectedSoundsDataframe()
		print(self)
		epidemicTest.buildPopulation(epidemicTest.filelist)
		epidemicTest.startInfections(epidemicTest.caseszero, epidemicTest.population)
		epidemicTest.starttime = tm.time()
		epidemicTest.saveFirstDay()
		epidemicTest.run()

	#Building a new epidemic simulation
	def run():
		print("                                ", end="\r")
		for d in range(epidemicTest.days):
			print("-- Simulating day: " + str(d), end="\r")
			epidemicTest.simulateAudioMerge(d)
			epidemicTest.simulateDay(d)
			epidemicTest.updateInfectedRatio()
			epidemicTest.saveDay(d)
		print("-- Simulation is finished!       ", end="\n")
		print("-- Time needed for simulating this epidemic: " + \
				epidemicTest.getSimulationTime(epidemicTest.starttime, tm.time()))
		epidemicTest.saveSimulationData()
		print("-- Plotting simulation's data...", end="\r")
		epidemicTest.vz.plotEpidemic(16, 9, epidemicTest.vname, epidemicTest.vpath + "charts/", \
		 					epidemicTest.epidemic, epidemicTest.audiodata, epidemicTest.population, \
							epidemicTest.days)
		print("-- Simulation for infecto Doppler saved!", end="\n")

	#Simulating audio merge
	def simulateAudioMerge(d):
		firstsample = d * epidemicTest.daysize
		for o in epidemicTest.infectedset:
			epidemicTest.evolInfection(epidemicTest.dp[o], d)
		epidemicTest.updateInfectedSet()

	#Simulating an epidemic day
	def simulateDay(d):
		actualinfected = epidemicTest.infectedset.copy()
		for o in actualinfected:
			epidemicTest.spread(epidemicTest.dp[o], d)
		epidemicTest.rp.checkResponse(d)

	def updateInfectedSet():
		epidemicTest.infectedset = epidemicTest.infectedset.difference(epidemicTest.recoveredset)
		epidemicTest.recoveredset = set()

	#Executing the virus spread
	def spread(idoppler, d):
		n = idoppler.getDayContactsCount(epidemicTest.modecontacts, epidemicTest.rp.getIsolationFactor())
		c = rd.sample(range(0, epidemicTest.population - 1), n)
		for i in range(len(c)):
			epidemicTest.decideInfection(epidemicTest.dp[c[i]], d)

	def decideInfection(doppler, d):
		t = rd.random()
		if t < epidemicTest.vr.infectionthreshold:
			epidemicTest.checkImmunity(doppler, epidemicTest.vr.immunityperiod, d)
			if (doppler.hasimmunity == False and doppler.isinfected == False):
				epidemicTest.setInfection(doppler, d)

	def setInfection(doppler, d):
		doppler.infectionnumber += 1
		doppler.isinfected = True
		doppler.infectiondate = d
		epidemicTest.infectiondata[1] += 1
		epidemicTest.infectiondata[2] += 1
		epidemicTest.infectiondata[doppler.dchannel + 3] += 1
		epidemicTest.infectedset.add(doppler.dnumber)

	def evolInfection(doppler, d):
		doppler.infectioncourse += epidemicTest.daysize
		if doppler.infectioncourse >= doppler.size:
			epidemicTest.setCure(doppler, d)

	def setCure(doppler, d):
		doppler.isinfected = False
		doppler.wasinfected = True
		doppler.hasimmunity = True
		doppler.enddate = d
		doppler.infectioncourse = 0
		epidemicTest.infectiondata[2] -= 1
		epidemicTest.infectiondata[doppler.dchannel + 3] -= 1
		epidemicTest.recoveredset.add(doppler.dnumber)
		epidemicTest.saveInfection(doppler)

	def startInfections(c, p):
		l = rd.sample(range(0, p - 1), c)
		for i in range(c):
			epidemicTest.setInfection(epidemicTest.dp[l[i]], 1)
		epidemicTest.updateInfectedRatio()
		print("-- Cases zero injected!", end="\n")

	def checkImmunity(doppler, period, d):
		if doppler.hasimmunity == True:
			if d > doppler.enddate + period:
				doppler.hasimmunity = False

	def updateInfectedRatio():
		epidemicTest.infectedratio = epidemicTest.infectiondata[2] / epidemicTest.population

	def setConfig(data):
		epidemicTest.ppath = data["pPath"]
		epidemicTest.vpath = data["vPath"]
		epidemicTest.vname = data["name"]
		epidemicTest.days = data["days"]
		epidemicTest.daysize = data["daySize"]
		epidemicTest.caseszero = data["casesZero"]
		epidemicTest.modecontacts = data["modeContacts"]
		epidemicTest.vr.infectionthreshold = data["infectionThreshold"]
		epidemicTest.vr.immunityperiod = data["immunityPeriod"]
		epidemicTest.response = data["response"]
		epidemicTest.rp.responseisactive = False
		epidemicTest.rp.responsestart = data["responseStart"]
		epidemicTest.rp.actionsperiod = data["actionsPeriod"]
		epidemicTest.rp.isolationfactor = data["isolationFactor"]
		epidemicTest.samplerate = data["sampleRate"]
		epidemicTest.channels = data["channels"]
		epidemicTest.audiolength = epidemicTest.days * epidemicTest.daysize
		epidemicTest.audiodata = np.zeros((epidemicTest.channels, epidemicTest.audiolength), dtype="float32")
		epidemicTest.filelist = os.listdir(data["pPath"])
		epidemicTest.cleanFileList(epidemicTest.filelist)
		epidemicTest.filelist.sort()
		if data["population"] > 0 and data["population"] <= len(epidemicTest.filelist):
			epidemicTest.population = data["population"]
		else:
			epidemicTest.population = len(epidemicTest.filelist)

	def buildPopulation(filelist):
		for f in range(epidemicTest.population):
			print("-- Loading sound object " + str(f), end="\r")
			epidemicTest.dp.append(Doppler(f, epidemicTest.channels, epidemicTest.ppath, filelist[f]))
		print("-- Sound objects loaded!          ", end="\n")

	def saveFirstDay():
		row = pd.DataFrame([(0,0,0,0,0,0,0,0.0)], columns = epidemicTest.epidemic.columns)
		epidemicTest.epidemic = pd.concat([epidemicTest.epidemic, row])

	def saveDay(d):
		epidemicTest.infectiondata[0] = d + 1
		epidemicTest.infectiondata[len(epidemicTest.infectiondata) - 1] = epidemicTest.infectedratio
		row = pd.DataFrame([epidemicTest.infectiondata[:]], columns = epidemicTest.epidemic.columns)
		epidemicTest.epidemic = pd.concat([epidemicTest.epidemic, row])

	def saveInfection(doppler):
		row = pd.DataFrame([[doppler.dnumber, doppler.name, doppler.infectionnumber, doppler.dchannel, \
							doppler.contactfactor, doppler.infectiondate, doppler.enddate, doppler.size]], \
							columns=epidemicTest.infectedsounds.columns)
		epidemicTest.infectedsounds = pd.concat([epidemicTest.infectedsounds, row])

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
		for c in range(epidemicTest.channels):
			l.append(0)
		l.append(0.0)
		return l

	def saveSimulationData():
		epidemicTest.epidemic.set_index("Day", inplace = True)
		epidemicTest.epidemic.to_csv(epidemicTest.vpath + "data/" + epidemicTest.vname + "_ep_test.csv")
		epidemicTest.infectedsounds.set_index("Number", inplace = True)
		epidemicTest.infectedsounds.to_csv(epidemicTest.vpath + "data/" + epidemicTest.vname + "_inf_test.csv")

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
		for c in range(epidemicTest.channels):
			columns.append("Infected in " + str(c))
		columns.append("Infected ratio")
		p = pd.DataFrame(columns=columns)
		p.index = p["Day"]
		p.index.name = "Day"
		return p

	#Calculating time needed for simulation to finish...
	def getSimulationTime(startTime, endTime):
		time = endTime - startTime
		formatedTime = epidemicTest.formatTime(time)
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
				"------------- epidemicTest ---------------\n" + \
				"------------- Version: 0.95 --------------\n" + \
				"-- Population: " + str(epidemicTest.population) + "\n" + \
				"-- Days: " + str(epidemicTest.days) + "\n" + \
				"-- Day size: " + str(epidemicTest.daysize) + "\n"
