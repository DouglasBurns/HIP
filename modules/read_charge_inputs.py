import ROOT
import numpy as np
import sys
from rootpy.io import root_open
from rootpy.plotting import Hist
from rootpy import asrootpy
import rootpy.plotting.root2matplotlib as rplt

from modules.pandas_utils import make_folder_if_not_exists
from modules.global_vars import REGIONS, CHARGE_CUTOFF

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import gc

mpl.rcParams['agg.path.chunksize'] = 50000

class input_charge_distributions(object):
	"""Create class for input charge distributions"""
	# def __init__(self, fName):

	def __init__(self, region, fName):
		self.region 	= region
		self.scd 		= fName
		self.scdFull 	= self._set_scd(isCut=False)
		self.scdCut 	= self._set_scd(isCut=True)

	def __call__(self):
		return

	def _set_scd(self, isCut=False):
		'''
		Return the SCD full distribution
		'''
		with root_open(self.scd) as f:
			if self._check_region():

				fName = ''
				if isCut: 
					fName = self.region+'_CutNormTo1'
				else: 
					fName = self.region+'_NormTo1'

				h = asrootpy(f.Get(fName).Clone())
				h.SetDirectory(0)
				self.nClusters = asrootpy(f.Get('nClusters')).integral()
				return h
			else:
				print "Cannot find input file :("
				sys.exit()

	def _check_region(self):
		'''
		Does region exist?
		'''
		if self.region not in REGIONS: 
			print "Incorrect region, Please try again..."
			return False
		else: return True



class ChargePreparation(object):
	"""docstring for ChargePreparation"""
	def __init__(self, fName):
		super(ChargePreparation, self).__init__()
		self.fName = fName
		self.dHist = {}
		self.isSCD = False
		self.dirName = None
		self._isSCD()

	def __call__(self):
		self._getHist()
		self._writeHist()
		return

	def _isSCD(self):
		if 'scd' in self.fName: 
			self.isSCD=True
			self.dirName = 'SCD'
		else: 
			self.dirName = 'Clusters'
		return

	def _getHist(self):
		with root_open(self.fName) as f:
			try:
				hClus = asrootpy(f.Get('demo/Clusters/nClusters'))
				hClus.SetDirectory(0)
				hClus.SetName('nClusters')
				self.dHist['nClusters'] = hClus
			except:
				self.dHist['nClusters'] = None

			for region in REGIONS:
				hOrig = asrootpy(f.Get('demo/'+self.dirName+'/'+region))
				hOrig.SetDirectory(0)
				hOrig.SetName(region+'_Original')

				hNorm = hOrig.Clone()
				hNorm.SetDirectory(0)
				hNorm.Scale(1 /hNorm.integral())
				hNorm.SetName(region+'_NormTo1')

				hCut = hOrig.Clone()
				hCut.SetDirectory(0)
				hCut = self._doCut(hCut)
				hCut.SetName(region+'_Cut')

				hCutNorm = hOrig.Clone()
				hCutNorm.SetDirectory(0)
				hCutNorm = self._doCut(hCutNorm)
				hCutNorm.Scale(1 /hCutNorm.integral())
				hCutNorm.SetName(region+'_CutNormTo1')

				hCDF = hOrig.Clone()
				hCDF.SetDirectory(0)
				hCDF = self._doCDF(hCDF)
				hCDF.SetName(region+'_CDF')

				hCutCDF = hOrig.Clone()
				hCutCDF.SetDirectory(0)
				hCutCDF = self._doCut(hCutCDF)
				hCutCDF = self._doCDF(hCutCDF)
				hCutCDF.SetName(region+'_CutCDF')

				self.dHist[region+'_Original'] 	= hOrig
				self.dHist[region+'_NormTo1'] 	= hNorm
				self.dHist[region+'_Cut'] 		= hCut
				self.dHist[region+'_CutNormTo1'] = hCutNorm
				self.dHist[region+'_CDF'] 		= hCDF
				self.dHist[region+'_CutCDF'] 	= hCutCDF
		return

	def _doCut(self, hist):
		bin_edges = list(hist.xedges())
		for bin in hist.bins_range():
			if bin_edges[bin] <= CHARGE_CUTOFF:
				hist.SetBinContent(bin, 0)
		return hist

	def _doCDF(self, hist):
		bin_edges = list(hist.xedges())
		ncdf = 0
		ntot = hist.integral()
		for bin in hist.bins_range():
			ncdf += hist.GetBinContent(bin)
			cdf = ncdf / ntot
			hist.SetBinContent(bin, cdf)
		return hist

	def _writeHist(self):
		with root_open(self.fName.replace('.root', '_all.root'), 'recreate') as f:
			if self.dHist['nClusters']:
				self.dHist['nClusters'].Write()
			for region in REGIONS:	
				self.dHist[region+'_Original'].Write()
				self.dHist[region+'_NormTo1'].Write()
				self.dHist[region+'_CDF'].Write()
				self.dHist[region+'_Cut'].Write()
				self.dHist[region+'_CutNormTo1'].Write()
				self.dHist[region+'_CutCDF'].Write()
		return


# # deprecated
# def fit_charge_landaus():
# 	# from global_vars import tracker_deets
# 	from mathematical_tools import return_rnd_Uniform, amplifier_response, charge_transformation
# 	import rootpy.plotting.root2matplotlib as rplt
# 	from rootpy.plotting import Legend, Canvas
# 	from rootpy.plotting.utils import draw

# 	# import other externals
# 	import matplotlib as mpl
# 	import matplotlib.pyplot as plt
# 	import numpy as np
# 	import gc
	
# 	from ROOT import gStyle
# 	gStyle.SetOptStat(0);

# 	d_fit = {}
# 	with root_open('input/simLandau.root') as f:
# 		for region in REGIONS:
# 			print 'Doing region {}'.format(region)
# 			if 'TIB' in region or '5' in region or '6' in region: l = 7500
# 			elif 'TOB' in region: l = 10000

# 			# Get Normalised Strip Charge Distribution from Region in Tracker
# 			h = f.Get(region).Clone()
# 			h.SetDirectory(0)

# 			edges = list(h.xedges())
# 			h.Scale(1 /h.Integral())

# 			# R = Range of fit
# 			# 0 = Fit not drawn
# 			# Q = Quiet
# 			# R = 
# 			# M = 

# 			fit_exp = ROOT.TF1("bkg", "expo", 0, l)
# 			fe = h.Fit(fit_exp, "SMR0+")

# 			fit_gs = ROOT.TF1("g", "gaus", 0, l)
# 			fg = h.Fit(fit_gs, "SMR0+")

# 			fit_lnd = ROOT.TF1("sig", "landau", l, 100000)
# 			fl = h.Fit(fit_lnd, "SMR0+")

# 			fit_tot = ROOT.TF1("el", "expo(0)+landau(2)", 0, 100000)
# 			c1 = fe.Parameter(0)
# 			c2 = fe.Parameter(1)
# 			c3 = fl.Parameter(0)
# 			c4 = fl.Parameter(1)
# 			c5 = fl.Parameter(2)
# 			fit_tot.SetParameters(c1, c2, c3, c4, c5)
# 			ft1 = h.Fit(fit_tot, "SMR0+")

# 			fit_tot2 = ROOT.TF1("eg", "gaus(0)+landau(3)", 0, 100000)
# 			d1 = fg.Parameter(0)
# 			d2 = fg.Parameter(1)
# 			d3 = fg.Parameter(2)
# 			d4 = fl.Parameter(0)
# 			d5 = fl.Parameter(1)
# 			d6 = fl.Parameter(2)
# 			fit_tot2.SetParameters(d1, d2, d3, d4, d5, d6)
# 			ft2 = h.Fit(fit_tot2, "SMR0+")

# 			d_fit[region] = [h, fe, fl, fg, ft1, ft2]


# 	with root_open('input/DataChargeFits.root', 'recreate') as f:
# 		for region, histfit in d_fit.iteritems():
# 			hist = histfit[0]

# 			fit_exp = histfit[1]
# 			a1 = fit_exp.Parameter(0)
# 			b1 = fit_exp.Parameter(1)
# 			# print a1, b1

# 			fit_lnd = histfit[2]
# 			a2 = fit_lnd.Parameter(0)
# 			b2 = fit_lnd.Parameter(1)
# 			c2 = fit_lnd.Parameter(2)
# 			# print a2, b2, c2

# 			fit_gs = histfit[3]
# 			a3 = fit_gs.Parameter(0)
# 			b3 = fit_gs.Parameter(1)
# 			c3 = fit_gs.Parameter(2)
# 			# print a3, b3, c3

# 			fit_el = histfit[4]
# 			a4 = fit_el.Parameter(0)
# 			b4 = fit_el.Parameter(1)
# 			c4 = fit_el.Parameter(2)
# 			d4 = fit_el.Parameter(3)
# 			e4 = fit_el.Parameter(4)
# 			# print a4, b4, c4, d4, e4

# 			fit_gl = histfit[5]
# 			a5 = fit_el.Parameter(0)
# 			b5 = fit_el.Parameter(1)
# 			c5 = fit_el.Parameter(2)
# 			d5 = fit_el.Parameter(3)
# 			e5 = fit_el.Parameter(4)
# 			f5 = fit_el.Parameter(5)
# 			# print a5, b5, c5, d5, e5, f5

# 			f_exp = ROOT.TF1("fexp","exp([0]+[1]*x)",0,100000)
# 			f_exp.SetParameters(a1, b1)
# 			f_gs = ROOT.TF1("fgaus","[0]*exp(-0.5*((x-[1])/[2])^2)",0,100000)
# 			f_gs.SetParameters(a3, b3, c3)
# 			f_lnd = ROOT.TF1("flnd","[0]*TMath::Landau(x,[1],[2],0)",0,100000)
# 			f_lnd.SetParameters(a2, b2, c2)
# 			f_el = ROOT.TF1("fexplnd","exp([0]+[1]*x)+[2]*TMath::Landau(x,[3],[4],0)",0,100000)
# 			f_el.SetParameters(a4, b4, c4, d4, e4)
# 			f_gl = ROOT.TF1("fgauslnd","[0]*exp(-0.5*((x-[1])/[2])^2)+[3]*TMath::Landau(x,[4],[5],0)",0,100000)
# 			f_gl.SetParameters(a5, b5, c5, d5, e5, f5)

# 			hist.SetName(region+'_Hist')
# 			hist.Write()
# 			f_exp.SetName(region+'_FitExp')
# 			f_exp.Write()
# 			f_gs.SetName(region+'_FitGaus')
# 			f_gs.Write()
# 			f_lnd.SetName(region+'_FitLnd')
# 			f_lnd.Write()
# 			f_el.SetName(region+'_FitEL')
# 			f_el.Write()
# 			f_gl.SetName(region+'_FitGL')
# 			f_gl.Write()

# 	with root_open('input/DataChargeFits.root', 'open') as f:
# 		for region in REGIONS:
# 			t1 = f.Get(region+'_FitExp')
# 			t2 = f.Get(region+'_FitGaus')
# 			t3 = f.Get(region+'_FitLnd')
# 			t4 = f.Get(region+'_FitEL')
# 			t5 = f.Get(region+'_FitGL')	
# 			h_input = f.Get(region+'_Hist').Clone()
# 			h = Hist(edges, name=region)
# 			input_charge_fitting_folder = 'plots/inputChargeFitting/'
# 			make_folder_if_not_exists(input_charge_fitting_folder)

# 			# Cant figure out how to draw TF1 in matplotlib so reverting to pyroot
# 			canvasA = Canvas(width=700, height=500)
# 			h_input.SetTitle("Data Charge Distribution in {};Charge [e]; N".format(region))
# 			h_input.Draw()
# 			t1.Draw("same")
# 			t3.Draw("same")
# 			t4.SetColor(1)
# 			t4.Draw("same")
# 			canvasA.Modified()
# 			canvasA.Update()
# 			canvasA.SaveAs(input_charge_fitting_folder+'FittedChargeDistribution2_{}.pdf'.format(region))

# 			# Cant figure out how to draw TF1 in matplotlib so reverting to pyroot
# 			canvasB = Canvas(width=700, height=500)
# 			h_input.SetTitle("Data Charge Distribution in {};Charge [e]; N".format(region))
# 			h_input.Draw()
# 			t2.Draw("same")
# 			t3.Draw("same")
# 			t5.SetColor(1)
# 			t5.Draw("same")
# 			canvasB.Modified()
# 			canvasB.Update()
# 			canvasB.SaveAs(input_charge_fitting_folder+'FittedChargeDistribution_{}.pdf'.format(region))

# 			# # RNG from TF1
# 			# n=0
# 			# while n < 100000:
# 			# 	r = t.GetRandom()
# 			# 	h.Fill(r)
# 			# 	n+=1
# 			# h.Scale(1 /h.Integral())

# 			# fig = plt.figure()
# 			# ax = fig.add_subplot(1, 1, 1)
# 			# rplt.hist(
# 			# 	h, 
# 			# 	histtype='step',
# 			# 	facecolor='red', 
# 			# 	edgecolor='red',
# 			# 	fill = True,
# 			# 	alpha=0.5,
# 			# 	label='Simulated Charge Distribution',
# 			# )
# 			# rplt.hist(
# 			# 	h_input, 
# 			# 	histtype='step',
# 			# 	facecolor='blue', 
# 			# 	edgecolor='blue',
# 			# 	fill = True,
# 			# 	alpha=0.5,
# 			# 	label='Data Charge Distribution',
# 			# )

# 			# ax.set_ylim([0,0.25])
# 			# ax.set_xlabel('Charge [e]')
# 			# ax.set_ylabel('N')
# 			# fig.suptitle('Simulated vs Data Charge Distribution', fontsize=14, fontweight='bold')
# 			# leg = plt.legend(loc='best')
# 			# leg.draw_frame(False)	

# 			# fig.savefig(input_charge_fitting_folder+'ModelledChargeDistribution_{}.pdf'.format(region), bbox_inches='tight')
# 			# fig.clf()
# 			# plt.close()
# 			# gc.collect()
# 	return

