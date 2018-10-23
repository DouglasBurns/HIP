from __future__ import division

import ROOT
import rootpy.plotting.root2matplotlib as rplt
from rootpy.plotting import Hist
from rootpy import asrootpy

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import gc
from matplotlib import rc, rcParams
mpl.rcParams['agg.path.chunksize'] = 50000

class plot_hist(object):
	"""
	Plot Type = 'Simulation' 'Data' 'CMSSW'
	"""
	def __init__(self):
		self.hists 		= []

		self.stitle 	= None
		self.title 		= None
		self.label 		= []
		self.xlabel 	= None
		self.ylabel 	= None
		self.outfolder 	= None
		self.outfile 	= None

		self.plotType 	= []
		self.setManual 	= False

		self.xlim 		= None
		self.ylim 		= None
		self.xrlim 		= None
		self.yrlim 		= None
		self.logy 		= False
		self.rlogy 		= False
		self.normalise 	= False
		self.addRatio  = False
		self.hDivide  	= None
		self.ylabelratio= 'Ratio'
		self.colour 	= []
		self.alpha 		= []
		self.fill 		= []
		self.zorder 	= []

	def __call__(self):
		self._setupFigure()
		if not self.setManual:
			self._set_plotting_defaults()
		self._plotFigure()
		self._plotStyling()
		if self.addRatio:
			self._generate_ratios()
			self._ratioFigure()
			self._ratioStyling()
		self._closeFigure()
		return None

	def _setupFigure(self):
		self.fig = plt.figure()
		self.fig.suptitle(self.stitle, fontsize=14, fontweight='bold')

		if self.addRatio:
			self.gs 	= gridspec.GridSpec( 2, 1, wspace=0.025, hspace=0.025, height_ratios = [4, 1] )
		else:
			self.gs 	= gridspec.GridSpec( 1, 1, wspace=0.025, hspace=0.025 ) 
		return None

	def _set_plotting_defaults(self):
		'''
		'''
		cSim = ['green', 'blue', 'red', 'magenta']
		cCMSSW = ['hotpink', 'cyan', 'darkgreen', 'lime']
		cData = ['black', 'blue', 'red', 'magenta']
		nSim, nData, nCMSSW = 0, 0, 0
		zorder_CMSSW = 0
		zorder_Data = len(self.plotType)
		for p in self.plotType:
			if p == 'Simulation':
				self.colour.append(cSim[nSim])
				self.alpha.append(1)
				self.fill.append(True)
				self.zorder.append(-1)
				nSim+=1
			if p == 'CMSSW':
				self.colour.append(cCMSSW[nCMSSW])
				self.alpha.append(1)
				self.fill.append(False)
				self.zorder.append(zorder_CMSSW)
				nCMSSW+=1
				zorder_CMSSW+=1
			if p == 'Data':
				self.colour.append(cData[nData])
				self.alpha.append(None)
				self.fill.append(None)
				self.zorder.append(zorder_Data)
				nData+=1
				zorder_Data+=1
		return None

	def _plotFigure(self):
		self.ax 	= plt.subplot( self.gs[0] )
		for i, hist in enumerate(self.hists):
			if self.plotType[i] == 'Data':
				rplt.errorbar(
					hist, 
					label= self.label[i],
					markerfacecolor= self.colour[i],
					markersize=8,
					xerr = False,
					yerr = False,
					elinewidth=0,
					markeredgewidth=0,
					markeredgecolor=self.colour[i],
					emptybins = False,
					zorder=self.zorder[i],
					axes=self.ax
				)
			elif self.plotType[i] == 'Simulation':
				rplt.hist(
					hist, 
					label=self.label[i],
					color=self.colour[i],
					alpha=self.alpha[i],
					fill =self.fill[i],
					zorder=self.zorder[i],
					axes=self.ax
				)
			elif self.plotType[i] == 'CMSSW':
				rplt.step(
					hist, 
					label=self.label[i],
					color=self.colour[i],
					zorder=self.zorder[i],
					linewidth=2,
					axes=self.ax
				)
			else:
				pass
		return None
		
	def _plotStyling(self):
		plt.title(self.title, loc='right')
		if self.xlim:
			self.ax.set_xlim(self.xlim)
		if self.ylim:
			self.ax.set_ylim(self.ylim)
		if self.logy:
			self.ax.set_yscale("log", nonposy='clip')
		self.ax.set_ylabel(self.ylabel)
		if not self.addRatio:
			self.ax.set_xlabel(self.xlabel)

		if not all(v is None for v in self.label):
			leg = self.ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=1)
			leg.draw_frame(False)
		return

	def _ratioFigure(self):
		self.axR 	= plt.subplot( self.gs[1] )
		for i, ratio in enumerate(self.ratios):
			if self.plotType[i] == 'Data':
				rplt.errorbar(
					ratio, 
					label= self.label[i],
					markerfacecolor= self.colour[i],
					markersize=8,
					xerr = False,
					yerr = False,
					elinewidth=0,
					markeredgewidth=0,
					markeredgecolor=self.colour[i],
					emptybins = False,
					zorder=self.zorder[i],
					axes=self.axR
				)
			elif self.plotType[i] == 'CMSSW':
				rplt.step(
					ratio, 
					label=self.label[i],
					color=self.colour[i],
					zorder=self.zorder[i],
					linewidth=2,
					axes=self.axR
				)
			elif self.plotType[i] == 'Simulation':
				plt.axhline(
					y = 1, 
					color = 'black', 
					linewidth = 2,
					axes=self.axR
				)
			else:
				pass
		return None
	
	def _ratioStyling(self):
		plt.setp( self.ax.get_xticklabels(), visible = False )

		if self.xrlim:
			self.axR.set_xlim(self.xrlim)
		if self.yrlim:
			self.axR.set_ylim(self.yrlim)
		if self.rlogy:
			self.axR.set_yscale("log", nonposy='clip')
		self.axR.set_xlabel(self.xlabel)
		self.axR.set_ylabel(self.ylabelratio)

		return

	def _closeFigure(self):
		self.gs.tight_layout(self.fig, rect=[0, 0.03, 1, 0.95])  
		self.fig.savefig(self.outfolder+self.outfile, bbox_inches='tight')
		self.fig.clf()
		plt.close()
		gc.collect()
		return None

	def _generate_ratios(self, compare='Simulation'):
		self.ratios = []
		if self.hDivide == None:
			try:
				self.hDivide = self.hists[self.plotType.index(compare)]
			except:
				self.addRatio = False
				print "Nothing to compare to..."
		else:
			pass

		for hist in self.hists:
			self.ratios.append(hist.divide(hist,self.hDivide))
		return


	def create_rootpy_hist(self, vals=None, bins=None, hist=None, norm=None, upperCut=False, htype=''):
		'''
		htype = VALS, ROOT or ROOTPY
		'''
		if htype == "VALS":
			h_rtpy = Hist(bins)
			for v in vals: 
				h_rtpy.Fill(v)
		elif htype == "ROOTPY":
			h_rtpy = hist
		elif htype == "ROOT":
			h_rtpy = asrootpy(hist)
		else:
			print "Please provide some histograms..."
			return None

		if upperCut:
			h_rtpy = self.apply_max_cutoff(h_rtpy)
		if norm: 
			h_rtpy.Scale(norm)
		return h_rtpy

	def apply_max_cutoff(self, h):
		'''
		Apply the max charge cutoff: 62,500 == bin 126
		'''
		tot = 0
		bin_edges = list(h.xedges())
		for bin in h.bins_range():
			if bin >= 126: 
				tot+=h.GetBinContent(bin)
				h.SetBinContent(bin, 0)
		h.SetBinContent(126, tot)
		return h


class plot_profile(object):
	"""
	Plot Type = 'None'
	"""
	def __init__(self):
		self.profile 	= None
		self.BX 		= None
		self.BS 		= None

		self.stitle 	= None
		self.title 		= None
		self.bs_label 	= None
		self.profile_label = None
		self.xlabel 	= None
		self.ylabel 	= None
		self.outfolder 	= None
		self.outfile 	= None

		self.xlim 		= None
		self.ylim 		= None
		self.logy 		= False
		self.rlogy 		= False

	def __call__(self):
		self._setupFigure()
		self._plotFigure()
		self._plotStyling()
		self._closeFigure()
		return None

	def _setupFigure(self):
		self.fig = plt.figure()
		self.fig.suptitle(self.stitle, fontsize=14, fontweight='bold')
		self.gs = gridspec.GridSpec( 1, 1, wspace=0.025, hspace=0.025 ) 
		return None


	def _plotFigure(self):
		self.ax 	= plt.subplot( self.gs[0] )

		if self.xlim:
			y_low = self.ylim[0]
			y_high = self.ylim[1]
		else:
			y_low = 0
			y_high = np.amax(self.profile)

		if self.BS is not None:
			self.ax.fill_between(
				self.BX,
				y_low, y_high, 
				where=self.BS>0,
				facecolor='green', 
				alpha=0.2,
				label=self.bs_label
			)
		else:
			pass
		plt.plot(
			self.BX, 
			self.profile,
			label=self.profile_label,
		)
		return None
		
	def _plotStyling(self):
		plt.title(self.title, loc='right')
		if self.xlim:
			self.ax.set_xlim(self.xlim)
		if self.ylim:
			self.ax.set_ylim(self.ylim)
		if self.logy:
			self.ax.set_yscale("log", nonposy='clip')
		self.ax.set_ylabel(self.ylabel)

		if self.profile_label is not None:
			leg = self.ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=1)
			leg.draw_frame(False)
		return None

	def _closeFigure(self):
		self.gs.tight_layout(self.fig, rect=[0, 0.03, 1, 0.95])  
		self.fig.savefig(self.outfolder+self.outfile, bbox_inches='tight')
		self.fig.clf()
		plt.close()
		gc.collect()
		return None


