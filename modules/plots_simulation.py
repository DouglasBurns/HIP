from __future__ import division
from modules.global_vars import EFFECTIVE_THRESHOLD, REGIONS, REGION_DETAILS
from modules.pandas_utils import make_folder_if_not_exists

from modules.HistoMaker import plot_hist, plot_profile

import ROOT
from rootpy.io import root_open
from rootpy import asrootpy

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import gc

from matplotlib import rc, rcParams
mpl.rcParams['agg.path.chunksize'] = 50000


def plot_simulation(title, folder_path, simulation_all, sim_details):
	'''
	Plot any simulation distributions
	'''
	print "- - - - - - - - - - - - - - - - - - -"
	print "Plotting Simulation Distributions"
	print "- - - - - - - - - - - - - - - - - - -"

	NOISE = sim_details['noise']
	region = sim_details['region']
	occ = sim_details['occupancy']

	# nEventsSim 			= len(simulation_all[simulation_all.isBeam != 0]['q_dep_e'])
	# nEventsSim 			= len(simulation_all[simulation_all.q_dep_e != 0]['q_dep_e'])
	nEventsSim 			= len(simulation_all['q_dep_e'])
	h_sim_weight 		= 1/nEventsSim
	nStrips 			= REGION_DETAILS[region]['nStrips_eta_lt1']
	nStripsFull 		= REGION_DETAILS[region]['nStrips']
	nEvents 			= 0

	with root_open('input/180406/landau_Sim_scd_060418_all.root') as f:
		hTmp = asrootpy(f.Get(region+'_Original').Clone())
		bin_edges =  np.array(list(hTmp.xedges()))

	charge_bins 		= np.array([a*1000 for a in range(1,100)])
	charge_bins_medium 	= np.array([a*5000 for a in range(1,200)])
	charge_bins_large 	= np.array([a*15000 for a in range(1,100)])
	charge_bins_vlarge 	= np.array([a*15000 for a in range(1,200)])
	voltage_bins 		= np.array([a*10 for a in range(0,80)])
	gain_bins 			= np.array([a for a in range(0,40)])
	gain_bins_mv_fc 	= np.array([a*0.01 for a in range(0,1000)])

	########################################################################################################################
	### CHARGE DEPOSITION DISTRIBUTION
	########################################################################################################################
	print 'Plotting Cut SCD Charge Deposition Distribution'
	with root_open('input/180406/landau_Sim_060418_all.root') as f:
		h_cmssw 						= asrootpy(f.Get(region+'_Cut').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_cmssw_weight 					= 1/(nStrips*nEvents)
		h_cmssw.SetDirectory(0)
	with root_open('input/180406/landau_Data_060418_all.root') as f:
		h_data_lowOcc 					= asrootpy(f.Get(region+'_Cut').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_lowOcc_weight 			= 1/(nStrips*nEvents)
		h_data_lowOcc.SetDirectory(0)
	with root_open('input/180406/landau_Data_278770_060418_VFPFix_False_all.root') as f:
		h_data_highOcc_preFix 			= asrootpy(f.Get(region+'_Cut').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_highOcc_preFix_weight 	= 1/(nStrips*nEvents)
		h_data_highOcc_preFix.SetDirectory(0)
	with root_open('input/180406/landau_Data_278808_060418_VFPFix_True_all.root') as f:
		h_data_highOcc_postFix 			= asrootpy(f.Get(region+'_Cut').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_highOcc_postFix_weight 	= 1/(nStrips*nEvents)
		h_data_highOcc_postFix.SetDirectory(0)

	plot = plot_hist()
	h1 = plot.create_rootpy_hist(
		vals=simulation_all[simulation_all.q_dep_e != 0]['q_dep_e'], 
		bins=bin_edges, 
		htype='VALS', 
		norm=h_sim_weight, 
		upperCut=True
	)
	h2 = plot.create_rootpy_hist(
		hist=h_data_lowOcc, 
		htype='ROOTPY', 
		norm=h_data_lowOcc_weight
	)
	h3 = plot.create_rootpy_hist(
		hist=h_data_highOcc_preFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_preFix_weight
	)
	h4 = plot.create_rootpy_hist(
		hist=h_data_highOcc_postFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_postFix_weight
	)
	h5 = plot.create_rootpy_hist(
		hist=h_cmssw, 
		htype='ROOTPY', 
		norm=h_cmssw_weight
	)

	plot.hists 		= [h1, h2, h3, h4, h5]

	plot.plotType 	= ['Simulation', 'Data', 'Data', 'Data', 'CMSSW']
	plot.label 		= ['Charge Deposition', 'Data lowOcc charge (strips in clusters)', 'Data highOcc charge (strips in clusters) no VFP fix', 'Data highOcc charge (strips in clusters)', 'Simulated charge (strips in clusters)']
	plot.addRatio 	= True

	plot.stitle 	= 'Charge Distribution Deposited on Strip'
	plot.title 		= title
	plot.xlabel 	= 'Charge deposited on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'ChargeDepositedInAPVe_cutSCD.png'

	plot.xlim 		= [1000, 70000]
	plot.ylim 		= [0.0000001,0.1]
	plot.xrlim 		= [0, 70000]
	# plot.yrlim 		= [0.002,200]
	plot.yrlim 		= [0,2]
	plot.logy 		= False
	plot.rlogy 		= False
	plot()
	del plot


	########################################################################################################################
	### FULL SCD CHARGE DEPOSITION DISTRIBUTION
	########################################################################################################################
	print 'Plotting Full SCD Charge Deposition Distribution'
	with root_open('input/180406/landau_Sim_060418_all.root') as f:
		h_cmssw 						= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAveSim 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAveSim / nClusterAveSim
		h_cmssw_weight 					= 1/(nStrips*nEvents*clusterWeight)
		h_cmssw.SetDirectory(0)
	with root_open('input/180406/landau_Data_060418_all.root') as f:
		h_data_lowOcc 					= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_lowOcc_weight 			= 1/(nStrips*nEvents*clusterWeight)
		h_data_lowOcc.SetDirectory(0)
	with root_open('input/180406/landau_Data_278770_060418_VFPFix_False_all.root') as f:
		h_data_highOcc_preFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_highOcc_preFix_weight 	= 1/(nStrips*nEvents*clusterWeight)
		h_data_highOcc_preFix.SetDirectory(0)
	with root_open('input/180406/landau_Data_278808_060418_VFPFix_True_all.root') as f:
		h_data_highOcc_postFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_highOcc_postFix_weight 	= 1/(nStrips*nEvents*clusterWeight)
		h_data_highOcc_postFix.SetDirectory(0)

	plot = plot_hist()
	h1 = plot.create_rootpy_hist(
		vals=simulation_all[simulation_all.q_dep_e != 0]['q_dep_e'], 
		bins=bin_edges, 
		htype='VALS', 
		norm=h_sim_weight, 
		upperCut=True
	)
	h2 = plot.create_rootpy_hist(
		hist=h_data_lowOcc, 
		htype='ROOTPY', 
		norm=h_data_lowOcc_weight
	)
	h3 = plot.create_rootpy_hist(
		hist=h_data_highOcc_preFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_preFix_weight
	)
	h4 = plot.create_rootpy_hist(
		hist=h_data_highOcc_postFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_postFix_weight
	)
	h5 = plot.create_rootpy_hist(
		hist=h_cmssw, 
		htype='ROOTPY', 
		norm=h_cmssw_weight
	)

	plot.hists 		= [h1, h2, h3, h4, h5]

	plot.plotType 	= ['Simulation', 'Data', 'Data', 'Data', 'CMSSW']
	plot.label 		= ['Charge Deposition', 'Data lowOcc charge (strips in clusters)', 'Data highOcc charge (strips in clusters) no VFP fix', 'Data highOcc charge (strips in clusters)', 'Simulated charge (strips in clusters)']
	plot.addRatio 	= True

	plot.stitle 	= 'Charge Distribution Deposited on Strip'
	plot.title 		= title
	plot.xlabel 	= 'Charge deposited on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'ChargeDepositedInAPVe_fullSCD.png'

	plot.xlim 		= [0.1, 70000]
	plot.ylim 		= [0.0000001,0.001]
	plot.xrlim 		= [0, 70000]
	# plot.yrlim 		= [0.002,200]
	plot.yrlim 		= [0,2]
	plot.logy 		= False
	plot.rlogy 		= False
	plot()
	del plot


	########################################################################################################################
	### CUT SCD EFFECTIVE CHARGE DEPOSITION TMP: _Cut-> _Original
	########################################################################################################################
	# nEvents is asrootpy(f.Get('nClusters')).integral(overflow=True)
	print 'Plotting Cut SCD Effective Charge Deposition'
	with root_open('input/180406/landau_Sim_060418_all.root') as f:
		h_cmssw 						= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_cmssw_weight 					= 1/(nStrips*nEvents)
		h_cmssw.SetDirectory(0)
	with root_open('input/180406/landau_Data_060418_all.root') as f:
		h_data_lowOcc 					= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_lowOcc_weight 			= 1/(nStrips*nEvents)
		h_data_lowOcc.SetDirectory(0)
	with root_open('input/180406/landau_Data_278770_060418_VFPFix_False_all.root') as f:
		h_data_highOcc_preFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_highOcc_preFix_weight 	= 1/(nStrips*nEvents)
		h_data_highOcc_preFix.SetDirectory(0)
	with root_open('input/180406/landau_Data_278808_060418_VFPFix_True_all.root') as f:
		h_data_highOcc_postFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		h_data_highOcc_postFix_weight 	= 1/(nStrips*nEvents)
		h_data_highOcc_postFix.SetDirectory(0)

	plot = plot_hist()
	h1 = plot.create_rootpy_hist(
		vals=simulation_all[simulation_all.q_dep_e != 0]['q_eff_e'], 
		bins=bin_edges, 
		htype='VALS', 
		norm=h_sim_weight, 
		upperCut=True
	)
	h2 = plot.create_rootpy_hist(
		hist=h_data_lowOcc, 
		htype='ROOTPY', 
		norm=h_data_lowOcc_weight
	)
	h3 = plot.create_rootpy_hist(
		hist=h_data_highOcc_preFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_preFix_weight
	)
	h4 = plot.create_rootpy_hist(
		hist=h_data_highOcc_postFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_postFix_weight
	)
	h5 = plot.create_rootpy_hist(
		hist=h_cmssw, 
		htype='ROOTPY', 
		norm=h_cmssw_weight
	)

	plot.hists 		= [h1, h2, h3, h4, h5]

	plot.plotType 	= ['Simulation', 'Data', 'Data', 'Data', 'CMSSW']
	plot.label 		= ['Charge Deposition', 'Data lowOcc charge (strips in clusters)', 'Data highOcc charge (strips in clusters) no VFP fix', 'Data highOcc charge (strips in clusters)', 'Simulated charge (strips in clusters)']
	plot.addRatio 	= True

	plot.stitle 	= 'Effective Charge Deposited on Strip (from Gain)'
	plot.title 		= title
	plot.xlabel 	= 'Effective charge deposited on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'EffectiveChargeDepositedInAPVe_cutSCD.png'

	plot.xlim 		= [0.1, 70000]
	plot.ylim 		= [0,0.002]
	if occ < 0.001:
		plot.ylim 		= [0,0.0001]
	else:
		plot.ylim 		= [0,0.002]
	plot.xrlim 		= [0, 70000]
	# plot.yrlim 		= [0.1,10]
	plot.yrlim 		= [0,2]
	plot.logy 		= False
	plot.rlogy 		= False
	plot()
	del plot



	########################################################################################################################
	### FULL SCD EFFECTIVE CHARGE DEPOSITION
	########################################################################################################################
	print 'Plotting Full SCD Effective Charge Deposition'
	with root_open('input/180406/landau_Sim_060418_all.root') as f:
		h_cmssw 						= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAveSim 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAveSim / nClusterAveSim
		h_cmssw_weight 					= 1/(nStrips*nEvents*clusterWeight)
		h_cmssw.SetDirectory(0)
	with root_open('input/180406/landau_Data_060418_all.root') as f:
		h_data_lowOcc 					= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_lowOcc_weight 			= 1/(nStrips*nEvents*clusterWeight)
		h_data_lowOcc.SetDirectory(0)
	with root_open('input/180406/landau_Data_278770_060418_VFPFix_False_all.root') as f:
		h_data_highOcc_preFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_highOcc_preFix_weight 	= 1/(nStrips*nEvents*clusterWeight)
		h_data_highOcc_preFix.SetDirectory(0)
	with root_open('input/180406/landau_Data_278808_060418_VFPFix_True_all.root') as f:
		h_data_highOcc_postFix 			= asrootpy(f.Get(region+'_Original').Clone())
		nEvents 						= asrootpy(f.Get('nClusters')).integral(overflow=True)
		nClusterAve 					= asrootpy(f.Get('nClusters')).GetMean()
		clusterWeight 					= nClusterAve / nClusterAveSim
		h_data_highOcc_postFix_weight 	= 1/(nStrips*nEvents*clusterWeight)
		h_data_highOcc_postFix.SetDirectory(0)

	plot = plot_hist()
	h1 = plot.create_rootpy_hist(
		vals=simulation_all[simulation_all.q_dep_e != 0]['q_eff_e'], 
		bins=bin_edges, 
		htype='VALS', 
		norm=h_sim_weight, 
		upperCut=True
	)
	h2 = plot.create_rootpy_hist(
		hist=h_data_lowOcc, 
		htype='ROOTPY', 
		norm=h_data_lowOcc_weight
	)
	h3 = plot.create_rootpy_hist(
		hist=h_data_highOcc_preFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_preFix_weight
	)
	h4 = plot.create_rootpy_hist(
		hist=h_data_highOcc_postFix, 
		htype='ROOTPY', 
		norm=h_data_highOcc_postFix_weight
	)
	h5 = plot.create_rootpy_hist(
		hist=h_cmssw, 
		htype='ROOTPY', 
		norm=h_cmssw_weight
	)

	plot.hists 		= [h1, h2, h3, h4, h5]

	plot.plotType 	= ['Simulation', 'Data', 'Data', 'Data', 'CMSSW']
	plot.label 		= ['Charge Deposition', 'Data lowOcc charge (strips in clusters)', 'Data highOcc charge (strips in clusters) no VFP fix', 'Data highOcc charge (strips in clusters)', 'Simulated charge (strips in clusters)']
	plot.addRatio 	= True

	plot.stitle 	= 'Effective Charge Deposited on Strip (from Gain)'
	plot.title 		= title
	plot.xlabel 	= 'Effective charge deposited on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'EffectiveChargeDepositedInAPVe_fullSCD.png'

	plot.xlim 		= [0.1, 70000]
	plot.ylim 		= [0,0.0002]
	plot.xrlim 		= [0, 70000]
	# plot.yrlim 		= [0.1,10]
	plot.yrlim 		= [0,2]
	plot.logy 		= False
	plot.rlogy 		= False
	plot()
	del plot



	########################################################################################################################
	### EFFECTIVE CHARGE VS CHARGE
	########################################################################################################################
	print 'Plotting Effective Charge VS Charge'
	plot = plot_hist()
	h1 = plot.create_rootpy_hist(
		vals 		= simulation_all[simulation_all.q_dep_e != 0]['q_eff_e'], 
		bins 		= bin_edges, 
		htype 		= 'VALS', 
		norm 		= h_sim_weight, 
		upperCut 	= True
	)
	h2 = plot.create_rootpy_hist(
		vals 		= simulation_all[simulation_all.q_dep_e != 0]['q_dep_e'], 
		bins 		= bin_edges, 
		htype		= 'VALS', 
		norm		= h_sim_weight, 
		upperCut	= True
	)
	plot.hists 		= [h1, h2]

	plot.plotType 	= ['CMSSW', 'CMSSW']
	plot.label 		= ['Effective Charge Deposited', 'Actual Charge Deposited']
	plot.addRatio 	= True
	plot.hDivide 	= h2

	plot.stitle 	= 'Comparison of Charge vs. Effective Charge Deposited on Strip'
	plot.title 		= title
	plot.xlabel 	= 'Charge deposited on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'EffectiveChargeVsChargeInAPVe.png'

	plot.xlim 		= [0.1, 70000]
	# plot.ylim 		= [0.0000001,0.1]
	plot.xrlim 		= [0, 70000]
	# plot.yrlim 		= [0.5,5]
	plot.yrlim 		= [0,2]
	plot.logy 		= False
	plot.rlogy 		= False
	plot()
	del plot


	########################################################################################################################
	### BASELINE APV CHARGE DISTRIBUTION
	########################################################################################################################
	print 'Plotting APV Baseline Charge Distribution'
	plot = plot_hist()
	h1 				= plot.create_rootpy_hist(vals=simulation_all[simulation_all.isBeam != 0]['q_apv_e'], bins=charge_bins_medium, htype='VALS')

	plot.hists 		= [h1]
	plot.plotType 	= ['Simulation']
	plot.label 		= ['Baseline charge distribution']

	plot.stitle 	= 'Baseline Charge Distribution In APV'
	plot.title 		= title
	plot.xlabel 	= 'Charge on APV in a bx(e)'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'BaselineChargeInAPVe.png'

	plot.xlim 		= [0.1, 200000]
	# plot.ylim 		= [0.0001,1.]
	# plot.logy 		= True
	plot()
	del plot

	########################################################################################################################
	### BASELINE APV VOLTAGE DISTRIBUTION
	########################################################################################################################
	print 'Plotting APV Baseline Voltage Distribution'
	plot = plot_hist()
	h1 = plot.create_rootpy_hist(vals=simulation_all[simulation_all.q_dep_e != 0]['V_baseline_mV'], bins=voltage_bins, htype='VALS')

	plot.hists 		= [h1]
	plot.plotType 	= ['Simulation']
	plot.label 		= ['Baseline voltage distribution']

	plot.stitle 	= 'Baseline Voltage Distirbution In APV'
	plot.title 		= title
	plot.xlabel 	= 'Voltage Baseline [mV]'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'BaselineVoltageInAPVmV.png'

	plot()
	del plot


	########################################################################################################################
	### AMPLIFIER RESPONSE DISTRIBUTION
	########################################################################################################################
	print 'Plotting APV Response Distribution'
	plot = plot_hist()
	h1 = plot.create_rootpy_hist(vals=simulation_all[simulation_all.q_dep_e != 0]['V_response_mV'], bins=gain_bins, htype='VALS')

	plot.hists 		= [h1]
	plot.plotType 	= ['Simulation']
	plot.label 		= [None]

	plot.stitle 	= 'Response ($V_{out}-V_{0}$)'
	plot.title 		= title
	plot.xlabel 	= '$V_{out}-V_{0}$ [mV]'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'ResponseInAPV.png'

	plot.xlim 		= [0,40]
	# plot.ylim 		= [0,1]
	plot()
	del plot
	#TO ADD: plt.axvline(x=EFFECTIVE_THRESHOLD, linewidth=4, color='r', label = 'Min Threshold')


	########################################################################################################################
	### AMPLIFIER GAIN DISTRIBUTION
	########################################################################################################################
	print 'Plotting APV Gain Distribution'
	plot = plot_hist()
	h1 = plot.create_rootpy_hist(vals=simulation_all[simulation_all.q_dep_e != 0]['V_gain_mV_fC'], bins=gain_bins_mv_fc, htype='VALS')

	plot.hists 	= [h1]
	plot.plotType 	= ['Simulation']
	plot.label 		= [None]

	plot.stitle 	= 'Gain ($\\frac{V_{\\mathrm{out}}-V_{0}}{Q_{\\mathrm{dep}}}$)'
	plot.title 		= title
	plot.xlabel 	= 'Gain [mV/fC]'
	plot.ylabel 	= 'N'
	plot.outfolder 	= folder_path
	plot.outfile 	= 'GainInAPV.png'

	plot.xlim 		= [0,6]
	plot()
	del plot


	########################################################################################################################
	### Profiles
	########################################################################################################################

	########################################################################################################################
	### BASELINE VOLTAGE ON BUNCH PRESENCE
	########################################################################################################################
	print 'Plotting APV Baseline Voltage Profile'
	plot = plot_profile()

	plot.profile 	= simulation_all['V_baseline_mV'][:10000]
	plot.BX 		= simulation_all['bunchCrossing'][:10000]
	plot.BS 		= simulation_all['isBeam'][:10000]

	plot.stitle 	= 'Baseline Voltage Profile'
	plot.title 		= title
	plot.xlabel 	= 'Voltage Baseline [mV]'
	plot.ylabel 	= 'N'
	plot.profile_label 	= ['Baseline voltage distribution']
	plot.bs_label 	= ['BX Structure from Run 276226']
	plot.outfolder 	= folder_path
	plot.outfile 	= 'BaselineVoltageProfile.png'

	plot.xlim 		= [0,10000]
	plot.ylim 		= [0,730]
	plot.logy 		= False
	plot.rlogy 		= False

	plot()
	del plot


	########################################################################################################################
	### BASELINE CHARGE ON BUNCH PRESENCE
	########################################################################################################################
	print 'Plotting APV Baseline Charge Profile'
	plot = plot_profile()

	plot.profile 	= simulation_all['q_apv_e'][:10000]
	plot.BX 		= simulation_all['bunchCrossing'][:10000]
	plot.BS 		= simulation_all['isBeam'][:10000]

	plot.stitle 	= 'Baseline Charge Profile'
	plot.title 		= title
	plot.xlabel 	= 'Charge Baseline [e]'
	plot.ylabel 	= 'N'
	plot.profile_label 	= ['Baseline charge distribution']
	plot.bs_label 	= ['BX Structure from Run 276226']
	plot.outfolder 	= folder_path
	plot.outfile 	= 'BaselineChargeProfile.png'

	plot.xlim 		= [0,10000]
	plot.ylim 		= [0,200000]
	plot.logy 		= False

	plot()
	del plot

