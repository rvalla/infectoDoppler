import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Visualization:
	"A class to plot the infection curve"

	defaultfont = "Trebuchet MS"
	legendFont = "Trebuchet MS"
	fontcolor = [0.85, 0.85, 0.95]
	titlesize = 12
	subtitlesize = 10
	axislabelsize = 7
	ticksize = 5
	backgroundPlot = [0.15, 0.12, 0.12]
	backgroundFigure = [0.099, 0.078, 0.078]
	majorGridColor = [0.75, 0.75, 0.95]
	minorGridColor = [0.75, 0.75, 0.95]
	alphaMGC = 1.0
	alphamGC = 1.0
	imageResolution = 200
	widthbig = 2.5
	widthnormal = 2.0
	widthsmall = 1.5
	plotcolors = [(0.86, 0.08, 0.86), (0.86, 0.86, 0.24), (0.08, 0.24, 0.86), (0.86, 0.24, 0.24), (0.08, 0.86, 0.86)]

	def gridsAndBackground():
		plt.grid(which='both', axis='both')
		plt.minorticks_on()
		plt.grid(True, "major", "y", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "y", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.xticks(fontsize=Visualization.ticksize)
		plt.yticks(fontsize=Visualization.ticksize)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def xgridAndBackground():
		plt.grid(which='both', axis='x')
		plt.minorticks_on()
		plt.grid(True, "major", "x", ls="-", lw=0.8, c=Visualization.majorGridColor, alpha=Visualization.alphaMGC)
		plt.grid(True, "minor", "x", ls="--", lw=0.3, c=Visualization.minorGridColor, alpha=Visualization.alphamGC)
		plt.xticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.yticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def background():
		plt.xticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.yticks(fontsize=Visualization.ticksize, color=Visualization.fontcolor)
		plt.gca().set_facecolor(Visualization.backgroundPlot)

	def simulationVisualization(self, sname, sfolder, sdata, audiodata, srate, population, days):
		Visualization.plotSimulation(8, 4.5, True, sname + "_std", sfolder, sdata, audiodata, srate, population, days)
		Visualization.plotSimulation(8, 4.5, False, sname + "_nt", sfolder, sdata, audiodata, srate, population, days)
		Visualization.plotSimulation(6, 6, False, sname + "_pt", sfolder, sdata, audiodata, srate, population, days)

	def plotSimulation(w, h, titles, sname, sfolder, sdata, audiodata, srate, population, days):
		figure = plt.figure(num=None, figsize=(w, h), dpi=Visualization.imageResolution, \
							facecolor=Visualization.backgroundFigure, edgecolor='k')
		if titles == True:
			figure.suptitle("infectoDoppler epidemic for version " + sname, fontsize=Visualization.titlesize, \
							fontname=Visualization.defaultfont, color=Visualization.fontcolor)
		infections = plt.subplot2grid((2, 1), (0, 0))
		for c in range(audiodata.shape[0]):
			key = "Infected in " + str(c)
			infections = sdata[key].plot(kind="line", linewidth=Visualization.widthsmall, \
									color=Visualization.plotcolors[(c+4)%len(Visualization.plotcolors)], label=key, \
									ax=infections)
		infections = sdata["Infected"].plot(kind="line", linewidth=Visualization.widthbig, \
								color=Visualization.plotcolors[3], label="Total infected", ax=infections)
		if titles == True:
			infections.set_title("infected sounds curve", fontsize=Visualization.subtitlesize, \
							fontname=Visualization.defaultfont, color=Visualization.fontcolor)
			infections.set_ylabel("")
			infections.set_xlabel("days", fontsize=Visualization.axislabelsize, fontname=Visualization.defaultfont, \
								color=Visualization.fontcolor)
		else:
			infections.set_title("")
			infections.set_ylabel("")
			infections.set_xlabel("")
		infections.set_xlim(0, days - 1)
		Visualization.background()
		audio = plt.subplot2grid((2, 1), (1, 0))
		time = np.linspace(0, audiodata.shape[1] / srate, num=audiodata.shape[1])
		for c in range(audiodata.shape[0]):
			plt.plot(time, audiodata[c], label="channel " + str(c), alpha=1, \
					linewidth=Visualization.widthsmall, color=Visualization.plotcolors[c%len(Visualization.plotcolors)])
		if titles == True:
			plt.title("epidemic signal result", fontsize=Visualization.subtitlesize, fontname=Visualization.defaultfont, \
					color=Visualization.fontcolor)
			plt.ylabel("")
			plt.xlabel("seconds", fontsize=Visualization.axislabelsize, fontname=Visualization.defaultfont, \
					color=Visualization.fontcolor)
		else:
			infections.set_title("")
			infections.set_ylabel("")
			infections.set_xlabel("")
		plt.xlim(0, time[time.size - 1])
		Visualization.background()
		plt.tight_layout(rect=[0, 0, 1, 1])
		plt.savefig(sfolder + sname + ".png", facecolor=figure.get_facecolor())

	def __str__(self):
		return "------------------------------------------\n" + \
				"---------- infectoD o p p l e r ----------\n" + \
				"- rodrigovalla.gitlab.io/infectodoppler --\n" + \
				"- gitlab.com/rodrigovalla/infectodoppler -\n" + \
				"------------- Visualization --------------\n" + \
				"------------- Version: 0.95 --------------\n"
