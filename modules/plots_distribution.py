from modules.global_vars import EFFECTIVE_THRESHOLD, REGIONS, REGION_DETAILS
from modules.pandas_utils import make_folder_if_not_exists
from modules.mathematical_tools import return_strip_charge_from_Samples, return_strip_charge_from_Poisson, return_strip_charge_per_BX
# import root
import ROOT
from rootpy.plotting import Hist
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt
from rootpy import asrootpy

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import gc


from matplotlib import rc, rcParams

def setup_matplotlib():
	'''
		Seup matplotlib with all the latex fancyness we have
	'''
	rc( 'text', usetex = True )
	rcParams['text.latex.preamble'] = compile_package_list()
	
def compile_package_list():
	'''
		We are looking for 3 packages:
		- siunitx for scientific units
		- helvet for Helvetica font (CMS style)
		- sansmath for sans serif math (CMS style)
		For this we use the 'kpsewhich'
	'''
	package_list = []
	# upright \micro symbols, \TeV, etc
	package_list.append(r'\usepackage{siunitx}')
	# force siunitx to actually use your fonts
	package_list.append(r'\sisetup{detect-all}')
	# set the normal font here
	package_list.append(r'\usepackage{helvet}')
	# load up the sansmath so that math -> helvet
	package_list.append(r'\usepackage{sansmath}')
	# <- tricky! -- gotta actually tell tex to use!
	package_list.append(r'\sansmath')

	return package_list

mpl.rcParams['agg.path.chunksize'] = 50000
# setup_matplotlib()

def run_distributions(title, folder_path, d_mip_variables, sim, NOISE, region):
	'''
	Plot any ditributions
	'''
	print "- - - - - - - - - - - - - - - - - - -"
	print "Plotting Simulation Distributions"
	print "- - - - - - - - - - - - - - - - - - -"

	########################################################################################################################
	### SIGNAL CHARGE DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	# xmax = max(d_mip_variables['q_dep_fC'])
	plt.hist(
		sim['q_dep_fC'], 
		np.arange(0, 20, 0.1),
		histtype='step',
		label='MIP Charge',
		edgecolor='blue',
		alpha=1,
		fill = True,
	)
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlim([0,5])
	fig.suptitle('Charge Distribution Deposited on Strip', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	ax.set_xlabel('Charge deposited on APV in a bx(fC) ')
	ax.set_ylabel('N')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'ChargeDepositedInAPVfC.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	# xmax = max(d_mip_variables['q_dep_e'])
	# print xmax
	plt.hist(
		sim['q_dep_e'], 
		np.arange(0, 100000, 1000),
		histtype='step',
		label='MIP Charge',
		edgecolor='blue',
		alpha=1,
		fill = True,
	)
	ax.set_yscale("log", nonposy='clip')
	ax.set_xlim([0,100000])
	fig.suptitle('Charge Distribution Deposited on Strip', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	ax.set_xlabel('Charge deposited on APV in a bx(e) ')
	ax.set_ylabel('N')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'ChargeDepositedInAPVe.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### AMPLIFIER GAIN DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['V_gain_mV_fC'], 
		bins=np.arange(-0.05, 6.05, 0.1), # For Floats
		histtype='step',	
		edgecolor='green',
		alpha=1,
		fill = True
	)
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('Gain on APV [mV/fC]')
	ax.set_ylabel('N')
	fig.suptitle('Amplifier Gain Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	fig.savefig(folder_path+'GainInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['V_response_mV'], 
		bins=np.arange(0, 500, 10), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	plt.axvline(x=EFFECTIVE_THRESHOLD, linewidth=4, color='r', label = 'Min Threshold')
	ax.set_xlabel('$V_{out}-V_{0}$ [mV]')
	ax.set_ylabel('N')
	fig.suptitle('Amplifier $V_{out}-V_{0}$ Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	fig.savefig(folder_path+'ResponseInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### AMPLIFIER BASELINE DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['V_baseline_mV'], 
		bins=np.arange(min(sim['V_baseline_mV']), 740, 10), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	ax.set_xlim([0, 740])
	fig.suptitle('Amplifier Baseline Voltage Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('Voltage Baseline [mV]')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'BaselineInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	# ########################################################################################################################
	# ### Track Eta Distribution
	# ########################################################################################################################
	# fig = plt.figure()
	# ax = fig.add_subplot(1, 1, 1)
	# plt.hist(
	# 	d_mip_variables['track_eta'], 
	# 	bins=np.arange(-1., 1., 0.01), # For Floats
	# 	histtype='step',	
	# 	color='black',
	# 	facecolor='green', 
	# 	alpha=1,
	# 	fill=True,
	# )
	# fig.suptitle('Track $\eta$ Distribution', fontsize=14, fontweight='bold')
	# plt.title(title, loc='right')
	# # ax.set_yscale("log", nonposy='clip')
	# ax.set_xlabel('$\eta$')
	# ax.set_ylabel('N')

	# fig.savefig(folder_path+'TrackEta.pdf', bbox_inches='tight')
	# fig.clf()
	# plt.close()
	# gc.collect()

	# ########################################################################################################################
	# ### Track Length Distribution
	# ########################################################################################################################
	# fig = plt.figure()
	# ax = fig.add_subplot(1, 1, 1)
	# plt.hist(
	# 	d_mip_variables['track_length'], 
	# 	bins=np.arange(200, 800, 10), # For Floats
	# 	histtype='step',	
	# 	color='black',
	# 	facecolor='green', 
	# 	alpha=1,
	# 	fill=True,
	# )
	# fig.suptitle('Silicon Track Length Distribution', fontsize=14, fontweight='bold')
	# plt.title(title, loc='right')
	# # ax.set_yscale("log", nonposy='clip')
	# ax.set_xlabel('Track Length')
	# ax.set_ylabel('N')

	# fig.savefig(folder_path+'TrackLength.pdf', bbox_inches='tight')
	# fig.clf()
	# plt.close()
	# gc.collect()


	########################################################################################################################
	### SPECIALIST PLOTS
	########################################################################################################################

	########################################################################################################################
	### SIGNAL DEPENDENCE ON BUNCH PRESENCE
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ))
	ax = fig.add_subplot(1, 1, 1)
	ax.set_xlim([0,5000])
	ax.set_ylim([0,730])

	ax.fill_between(
		sim['bunchCrossing'],
		0, 730, 
		where=sim['isBeam']>0,
		facecolor='green', 
		alpha=0.2,
		label='Bunches Present'
	)

	plt.plot(
		sim['bunchCrossing'], 
		sim['V_baseline_mV'],
		label='APV Response',
	)

	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('APV Response [mV]')
	fig.suptitle('$V_{out}$ with Bunch Crossing Dependence', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	filename = 'VoltageBXDependence'
	if not NOISE: filename+='NoNoise'
	fig.savefig(folder_path+filename+'.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


# Deprecated (May or may not work)
	# ########################################################################################################################
	# ### CHARGE COMPARISONS
	# ########################################################################################################################
	# hs_to_plot = []

	# with root_open('input/171107_landau_lowPU.root') as f_data_PU0:
	# 	if region not in REGIONS:
	# 		print "Incorrect region, Please try again..."
	# 	h_data_PU0 = asrootpy(f_data_PU0.Get('landauPlot/landau_'+region.replace('_','')+'_stripCharge').Clone())
	# 	h_data_PU0.SetDirectory(0)
	# 	h_data_PU0.Scale(1 /h_data_PU0.Integral())
	# 	l_data_edges = list(h_data_PU0.xedges())

	# 	hs_to_plot.append({
	# 		'hist'		: h_data_PU0,
	# 		'label' 	: 'Charge Distribution in Data at low PU',
	# 		'color'		: 'black',
	# 		'type' 		: 'Data'
	# 	})

	# with root_open('input/landau_26042017.root') as f_data_PU30:
	# 	if region not in REGIONS:
	# 		print "Incorrect region, Please try again..."
	# 	h_data_PU30 = asrootpy(f_data_PU30.Get('landauPlot/landau_'+region.replace('_','')+'_stripCharge').Clone())
	# 	h_data_PU30.SetDirectory(0)
	# 	h_data_PU30.Scale(1 /h_data_PU30.Integral())

	# 	hs_to_plot.append({
	# 		'hist'		: h_data_PU30,
	# 		'label' 	: 'Charge Distribution in Data at PU30',
	# 		'color'		: 'red',
	# 		'type' 		: 'Data'
	# 	})

	# # SAMPLES ARE TO LARGE - NEED TO PLOT CUTOFF ONE?

	# hist = Hist(l_data_edges)
	# for v in d_mip_variables['q_dep_e']:
	# 	if v < 1000: continue
	# 	# Add in inclusive tail
	# 	if v >= 62000: v = 62000
	# 	hist.Fill(v)
	# hist.Scale(1 / hist.Integral() )

	# hs_to_plot.append({
	# 	'hist'		: hist,
	# 	'label' 	: 'APV Simulation Charge Input',
	# 	'color'		: 'green',
	# 	'type' 		: 'Simulation'
	# })


	# fig = plt.figure()
	# fig.suptitle("Charge Depostion Comparison Pre and Post APV", fontsize=14, fontweight='bold')
	# gs = gridspec.GridSpec( 2, 1, height_ratios = [5, 1], wspace=0.025, hspace=0.025 ) 

	# rs_to_plot=[]

	# ax = plt.subplot( gs[0] )
	# plt.title(title, loc='right')

	# for h_info in hs_to_plot:
	# 	if 'Data' in h_info['type']:
	# 		rplt.errorbar(
	# 			h_info['hist'], 
	# 			label= h_info['label'],
	# 			markerfacecolor= h_info['color'],
	# 			markersize=6,
	# 			xerr = False,
	# 			yerr = False,
	# 			elinewidth=0,
	# 			emptybins = False,
	# 		)

	# 		# Low and High PU Ratios
	# 		r=hist.Clone()
	# 		r.SetDirectory(0)
	# 		r.Divide(h_info['hist'])
	# 		rs_to_plot.append({
	# 			'hist'		: r,
	# 			'label' 	: '',
	# 			'color'		: h_info['color'],
	# 			'type' 		: 'Ratio'
	# 		})
	# 	if 'CMSSW' in h_info['type']:
	# 		rplt.step(
	# 			h_info['hist'], 
	# 			label= h_info['label'],
	# 			color= h_info['color'],
	# 		)
	# 	if 'Simulation' in h_info['type']:
	# 		rplt.hist(
	# 			h_info['hist'], 
	# 			histtype='step',
	# 			alpha=1,
	# 			fill = False,
	# 			label= h_info['label'],
	# 			color= h_info['color'],
	# 		)

	# ax.set_ylim([0.0001,1.])
	# # ax.set_xlim([0.0001,100000])
	# ax.set_xlim([10000,70000])
	# ax.set_yscale("log", nonposy='clip')
	# ax.set_ylabel('N')
	# plt.setp( ax.get_xticklabels(), visible = False )
	# leg = ax.legend(loc='best', numpoints=1)
	# leg.draw_frame(False)	

	# ax_ratio = plt.subplot( gs[1] )
	# for r_info in rs_to_plot:
	# 	rplt.errorbar(
	# 		r_info['hist'], 
	# 		label= r_info['label'],
	# 		markerfacecolor= r_info['color'],
	# 		markersize=3,
	# 		xerr = False,
	# 		yerr = False,
	# 		elinewidth=0,
	# 		emptybins = False,
	# 		axes = ax_ratio, 
	# 	)

	# ax_ratio.set_ylim([0,2])
	# # ax_ratio.set_xlim([0.0001,100000])
	# ax_ratio.set_xlim([10000,70000])
	# ax_ratio.set_xlabel('Charge deposited on APV in a bx(e) ')
	# ax_ratio.set_ylabel(r'$\frac{\mathrm{sim Charge}}{\mathrm{data Charge}}$')

	# # leg1 = ax_ratio.legend(loc='best', numpoints=1)
	# # leg1.draw_frame(False)	
	# gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  
	# filename = 'ChargeDepositionPreAndPostAPV'
	# fig.savefig(folder_path+filename+'.pdf', bbox_inches='tight')
	# fig.clf()
	# plt.close()
	# gc.collect()
	# return 


########################################################################################################################
### SIMULATION CHARGE COMPARISONS
########################################################################################################################

def plot_cmssw_charge_distributions(REGION):
	'''
	CMSSWSim stages. SCD vs SCD+Noise+ZS vs SCD+Noise+ZS+ClusterStripsOnly
	'''
	make_folder_if_not_exists('plots/InputChargeDistributionsCMSSW/')

	hs_to_plot = []
	with root_open('input/180207/landau_Sim_scd_070218.root') as f:
		h_scd = asrootpy( f.Get('demo/SCD/'+REGION).Clone() )
		h_scd = apply_max_cutoff(h_scd)
		h_scd.Scale(1 /h_scd.integral(xbin1=21,xbin2=200))
		h_scd.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_scd,
			'label' 	: 'SCD',
			'color'		: 'black',
			'type' 		: 'CMSSW'
		})

		h_zs = asrootpy( f.Get('demo/ZS/'+REGION).Clone() )
		h_zs = apply_max_cutoff(h_zs)
		h_zs.Scale(1 /h_zs.integral(xbin1=21,xbin2=200))
		h_zs.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_zs,
			'label' 	: 'SCD + Noise + ZS',
			'color'		: 'blue',
			'type' 		: 'CMSSW'
		})

		h_clus = asrootpy( f.Get('demo/Clusters/'+REGION).Clone() )
		h_clus.Scale(1 /h_clus.integral(xbin1=21,xbin2=200))
		h_clus.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_clus,
			'label' 	: 'Cluster Strip Charge',
			'color'		: 'red',
			'type' 		: 'CMSSW'
		})

	fig = plt.figure()
	fig.suptitle("Evolution of the SCD in CMSSW", fontsize=14, fontweight='bold')
	gs = gridspec.GridSpec( 1, 1, wspace=0.025, hspace=0.025 ) 
	ax = plt.subplot( gs[0] )
	plt.title(REGION.replace("_", " ")+" normalised between 10,000-70,000", loc='right')
	for h_info in hs_to_plot:
		if 'CMSSW' in h_info['type']:
			rplt.step(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
			)
	ax.set_ylim([0.0001,10.])
	ax.set_xlim([0,70000])
	ax.set_yscale("log", nonposy='clip')
	ax.set_ylabel('N')
	ax.set_xlabel('Charge (e)')

	leg = ax.legend(loc='best', numpoints=1, prop={'size': 10})
	leg.draw_frame(False)

	gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  
	filename = 'CMSSWSimChargeDepositionOrig'+REGION
	fig.savefig('plots/InputChargeDistributionsCMSSW/'+filename+'.png', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

def plot_cmssw_data_charge_comparisons(REGION):
	'''
	SCD vs CMSSWSimPostAPV lowOcc vs Data lowOcc vs Data highOcc
	'''
	make_folder_if_not_exists('plots/InputChargeComparisons/')

	hs_to_plot = []
	rs_to_plot = []
	with root_open('input/180207/landau_Sim_scd_070218.root') as f:
		h_scd = asrootpy( f.Get('demo/SCD/'+REGION).Clone() )
		h_scd = apply_max_cutoff(h_scd)
		h_scd.Scale(1 /h_scd.integral(xbin1=21,xbin2=200))
		h_scd.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_scd,
			'label' 	: 'SCD',
			'color'		: 'black',
			'type' 		: 'SCD'
		})

		h_clus = asrootpy( f.Get('demo/Clusters/'+REGION).Clone() )
		h_clus.Scale(1 /h_clus.integral(xbin1=21,xbin2=200))
		h_clus.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_clus,
			'label' 	: 'Cluster Strip Charge',
			'color'		: 'red',
			'line' 		: 'solid',
			'type' 		: 'CMSSW'
		})

	with root_open('input/180129_lowPU/landau_lowPUClusters_290118_orig.root') as f:
		h_data_lowOcc = asrootpy(f.Get(REGION).Clone())
		h_data_lowOcc.Scale(1 /h_data_lowOcc.integral(xbin1=21,xbin2=200))
		h_data_lowOcc.SetDirectory(0)
		hs_to_plot.append({
			'hist'		: h_data_lowOcc,
			'label' 	: 'Data lowOcc Strips from Clusters',
			'color'		: 'black',
			'type' 		: 'Data'
		})

	r=h_data_lowOcc.Clone()
	r.SetDirectory(0)
	r.Divide(h_scd)
	r2=h_data_lowOcc.Clone()
	r2.SetDirectory(0)
	r2.Divide(h_clus)

	rs_to_plot.append({
		'hist'		: r,
		'label' 	: '',
		'color'		: 'black',
		'type' 		: 'Ratio'
	})
	rs_to_plot.append({
		'hist'		: r2,
		'label' 	: '',
		'color'		: 'red',
		'type' 		: 'Ratio'
	})

	fig = plt.figure()
	fig.suptitle("Low PU: SCD vs CMSSW Cluster Strip Charge vs Data Cluster Strip Charge", fontsize=14, fontweight='bold')
	gs = gridspec.GridSpec( 2, 1, height_ratios = [5, 1], wspace=0.025, hspace=0.025 ) 
	ax = plt.subplot( gs[0] )
	plt.title(REGION.replace("_", " ")+" normalised 10,000-70,000", loc='right')

	for h_info in hs_to_plot:
		if 'Data' in h_info['type']:
			rplt.hist(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				alpha=0.35,
				fill = True,
				zorder=0,
			)
		if 'SCD' in h_info['type']:
			rplt.errorbar(
				h_info['hist'], 
				label= h_info['label'],
				markerfacecolor= h_info['color'],
				markersize=3,
				xerr = False,
				yerr = False,
				elinewidth=0,
				emptybins = False,
				zorder=len(hs_to_plot),
			)
		if 'CMSSW' in h_info['type']:
			rplt.step(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				linestyle=h_info['line']
			)

	ax.set_ylim([0.0001,1.])
	ax.set_xlim([0.1, 70000])
	ax.set_yscale("log", nonposy='clip')
	ax.set_ylabel('N')
	plt.setp( ax.get_xticklabels(), visible = False )

	leg = ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=1)
	leg.draw_frame(False)

	ax_ratio = plt.subplot( gs[1] )
	ax_ratio.axhline(1, color='black')
	for r_info in rs_to_plot:
		rplt.errorbar(
			r_info['hist'], 
			label=r_info['label'],
			markerfacecolor=r_info['color'],
			markersize=3,
			markeredgewidth=0,
			xerr = False,
			yerr = False,
			elinewidth=0,
			emptybins = False,
			axes = ax_ratio, 
		)

	ax_ratio.set_ylim([0,2])
	ax_ratio.set_xlim([0.1,70000])
	ax_ratio.set_xlabel('Charge deposited on APV in a bx(e) ')
	ax_ratio.set_ylabel(r'$\frac{\mathrm{Data}}{\mathrm{Sim}}$')

	gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  

	filename = 'CMSSWSimChargeDepositionVsData'+REGION
	fig.savefig('plots/InputChargeComparisons/'+filename+'.png', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


def plot_cmssw_charge_occupancy_variations(REGION, useFullDist=True):
	'''
	Data highOcc vs SCD vs SCD Po(N)
	'''
	make_folder_if_not_exists('plots/InputChargePoissonMatching/')
	OCC = REGION_DETAILS[REGION]['Occ_Data']

	hs_to_plot = []
	rs_to_plot = []
	occupancies_to_test = []
	colors = ['blue', 'red', 'darkgreen', 'magenta']

	if useFullDist:
		f_hist = 'input/landau_scd_290118_orig.root'
		occupancies_to_test = [OCC*10, OCC*20, OCC*50, OCC*100]
	else:
		f_hist = 'input/landau_scd_290118_cut.root'
		occupancies_to_test = [OCC*5, OCC*10, OCC*20, OCC*50]
	
	with root_open(f_hist) as f:
		h = asrootpy(f.Get(REGION).Clone())
		h.SetDirectory(0)
		l_edges = list(h.xedges())

	# with root_open('input/landau_lowPUTracks_290118_orig.root') as f:
	# 	h_data_PU0 = asrootpy(f.Get(REGION).Clone())
	# 	h_data_PU0.SetDirectory(0)
	# 	h_data_PU0.Scale(1 /h_data_PU0.integral(xbin1=21,xbin2=200))
	# 	hs_to_plot.append({
	# 		'hist'		: h_data_PU0,
	# 		'label' 	: 'lowPU Strips from Tracks',
	# 		# 'color'		: '0.5',
	# 		'color'		: 'grey',
	# 		'type' 		: 'Data'
	# 	})

	# with root_open('input/landau_lowPUClusters_290118_orig.root') as f:
	# 	h_data_lowOcc = asrootpy(f.Get(REGION).Clone())
	# 	h_data_lowOcc.SetDirectory(0)
	# 	h_data_lowOcc.Scale(1 /h_data_lowOcc.integral(xbin1=21,xbin2=200))
	# 	hs_to_plot.append({
	# 		'hist'		: h_data_lowOcc,
	# 		'label' 	: 'lowOcc Strips from Clusters',
	# 		# 'color'		: '0',
	# 		'color'		: 'brown',
	# 		'type' 		: 'Data'
	# 	})

	with root_open('input/landau_clusterData_010218_VFPFix_True_orig.root') as f:
		h_data_highOcc = asrootpy(f.Get(REGION).Clone())
		h_data_highOcc.SetDirectory(0)
		h_data_highOcc.Scale(1 /h_data_highOcc.integral(xbin1=21,xbin2=200))
		hs_to_plot.append({
			'hist'		: h_data_highOcc,
			'label' 	: 'highOcc Strips from Clusters',
			# 'color'		: '0',
			'color'		: 'black',
			'type' 		: 'Data'
		})

	hist_scd = Hist(l_edges)

	h_tests = []
	for occ, col in zip(occupancies_to_test, colors):
		h_tmp = {
			'occ' 	: occ,
			'hist' 	: Hist(l_edges),
			'color' : col,
		}
		h_tests.append(h_tmp)

	i=0
	while i<250000:
		v = return_strip_charge_from_Poisson(h, OCC, add_noise=False, add_truncation=True)
		hist_scd.Fill(v)
		for h_test in h_tests:
			v_occ = return_strip_charge_from_Poisson(h, h_test['occ'], add_noise=False, add_truncation=True, cut_charge=True)
			if not v_occ < 10000: h_test['hist'].Fill(v_occ)
		i=i+1

	# Normalising between 10000-100000
	hist_scd.Scale(1 /hist_scd.integral(xbin1=21,xbin2=200))
	for h_test in h_tests:
		h_test['hist'].Scale(1 /h_test['hist'].integral(xbin1=21,xbin2=200))

	scd=''
	if useFullDist:
		scd = 'SCD'
	else:
		scd = 'Cut SCD'

	r_scd=h_data_highOcc.Clone()
	r_scd.SetDirectory(0)
	r_scd.Divide(hist_scd)
	hs_to_plot.append({
		'hist'		: hist_scd,
		'label' 	: '{SCD} sampled Po({OCC})'.format(SCD=scd, OCC=OCC),
		'color'		: 'black',
		'type' 		: 'SCD'
	})
	rs_to_plot.append({
		'hist'		: r_scd,
		'label' 	: '',
		'color'		: 'black',
		'type' 		: 'Ratio'
	})
	for h_test in h_tests:
		r=h_data_highOcc.Clone()
		r.SetDirectory(0)
		r.Divide(h_test['hist'])
		hs_to_plot.append({
			'hist'		: h_test['hist'],
			'label' 	: '{SCD} sampled Po({OCC})'.format(SCD=scd, OCC=h_test['occ']),
			'color'		: h_test['color'],
			'line' 		: 'solid',
			'type' 		: 'CMSSW'
		})
		rs_to_plot.append({
			'hist'		: r,
			'label' 	: '',
			'color'		: h_test['color'],
			'type' 		: 'Ratio'
		})

	fig = plt.figure()
	fig.suptitle("Charge Deposition from Simulation using Sampling from {SCD} distribution".format(SCD=scd), fontsize=14, fontweight='bold')

	gs = gridspec.GridSpec( 2, 1, height_ratios = [5, 1], wspace=0.025, hspace=0.025 ) 
	ax = plt.subplot( gs[0] )
	plt.title(REGION.replace("_", " ")+" normalised 10,000-70,000", loc='right')

	for h_info in hs_to_plot:
		if 'Data' in h_info['type']:
			rplt.hist(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				alpha=0.35,
				fill = True,
				zorder=0,
			)
		if 'SCD' in h_info['type']:
			rplt.errorbar(
				h_info['hist'], 
				label= h_info['label'],
				markerfacecolor= h_info['color'],
				markersize=3,
				xerr = False,
				yerr = False,
				elinewidth=0,
				emptybins = False,
				zorder=len(hs_to_plot),
			)
		if 'CMSSW' in h_info['type']:
			rplt.step(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				linestyle=h_info['line']
			)

	ax.set_ylim([0.0001,1.])
	# ax.set_xlim([10000,70000])
	ax.set_xlim([0.1, 70000])
	ax.set_yscale("log", nonposy='clip')
	ax.set_ylabel('N')
	# ax.set_xlabel('Charge (e)')
	plt.setp( ax.get_xticklabels(), visible = False )

	leg = ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=2)
	leg.draw_frame(False)

	ax_ratio = plt.subplot( gs[1] )
	ax_ratio.axhline(1, color='black')
	for r_info in rs_to_plot:
		rplt.errorbar(
			r_info['hist'], 
			label=r_info['label'],
			markerfacecolor=r_info['color'],
			markersize=6,
			markeredgewidth=0,
			xerr = False,
			yerr = False,
			elinewidth=0,
			emptybins = False,
			axes = ax_ratio, 
		)

	ax_ratio.set_ylim([0,2])
	ax_ratio.set_xlim([0.1,70000])
	# ax_ratio.set_xlim([10000,70000])
	ax_ratio.set_xlabel('Charge deposited on APV in a bx(e) ')
	ax_ratio.set_ylabel(r'$\frac{\mathrm{Data\ High\ Occ}}{\mathrm{SCD\ Sampling}}$')

	gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  
	filename = 'CMSSWSimChargeFrom{SCD}_'.format(SCD=scd.replace(" ", ""))+REGION
	fig.savefig('plots/InputChargePoissonMatching/'+filename+'.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()




def plot_data_VFP_fixes(REGION):
	'''
	highOcc comparison Data pre/post APV fix
	'''
	make_folder_if_not_exists('plots/VFP_Fixes/')

	hs_to_plot = []

	with root_open('input/landau_clusterData_010218_VFPFix_True_orig.root') as f:
		h_data_VFPFix_True = asrootpy(f.Get(REGION).Clone())
		h_data_VFPFix_True.SetDirectory(0)
		h_data_VFPFix_True.Scale(1 /h_data_VFPFix_True.integral(xbin1=21,xbin2=200))
		hs_to_plot.append({
			'hist'		: h_data_VFPFix_True,
			'label' 	: 'VFP fixed (278808)',
			'color'		: 'brown',
			'type' 		: 'Data'
		})

	with root_open('input/landau_clusterData_010218_VFPFix_False_orig.root') as f:
		h_data_VFPFix_False = asrootpy(f.Get(REGION).Clone())
		h_data_VFPFix_False.SetDirectory(0)
		h_data_VFPFix_False.Scale(1 /h_data_VFPFix_False.integral(xbin1=21,xbin2=200))
		hs_to_plot.append({
			'hist'		: h_data_VFPFix_False,
			'label' 	: 'VFP issue (278770)',
			'color'		: 'black',
			'type' 		: 'Data'
		})

	fig = plt.figure()
	fig.suptitle("VFP comparison in highOcc strips from clusters", fontsize=14, fontweight='bold')
	gs = gridspec.GridSpec( 1, 1, wspace=0.025, hspace=0.025 ) 
	ax = plt.subplot( gs[0] )

	plt.title(REGION.replace("_", " ")+" normalised 10,000-70,000", loc='right')

	for h_info in hs_to_plot:
		if 'Data' in h_info['type']:
			rplt.hist(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				alpha=0.35,
				fill = True,
				zorder=0,
			)
	ax.set_ylim([0.0001,1.])
	ax.set_xlim([0.1, 70000])
	ax.set_yscale("log", nonposy='clip')
	ax.set_ylabel('N')
	ax.set_xlabel('Charge (e)')

	leg = ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=1)
	leg.draw_frame(False)

	gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  
	filename = 'VFPFix_'+REGION
	fig.savefig('plots/VFP_Fixes/'+filename+'.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()




def testing(REGION, useFullDist=True):
	'''
	Data highOcc vs SCD vs SCD Po(N)
	'''
	make_folder_if_not_exists('plots/TMPTEST/')
	OCC = REGION_DETAILS[REGION]['Occ_Data']
	nStrip = REGION_DETAILS[REGION]['nStrips_eta_lt1']

	hs_to_plot = []
	f_hist = 'input/180207/landau_scd_070218_orig.root'
	with root_open(f_hist) as f:
		nEvents = asrootpy(f.Get('nClusters')).integral()
		print REGION, nEvents, nStrip

		h = asrootpy(f.Get(REGION).Clone())
		h.SetDirectory(0)
		h.Scale(1 /(nEvents*nStrip))
		l_edges = list(h.xedges())

		hs_to_plot.append({
			'hist'		: h,
			'label' 	: 'highPU Strips from Clusters /',
			'color'		: 'grey',
			'type' 		: 'Data'
		})

	# Calculating the occupancy...
	# Aim for P(Strip Hit in Event with Charge)
	# h_data / (nEvent * nStrip)

	# hist_scd = Hist(l_edges)
	fig = plt.figure()
	fig.suptitle("TMPTEST", fontsize=14, fontweight='bold')
	gs = gridspec.GridSpec( 1, 1, wspace=0.025, hspace=0.025 ) 
	ax = plt.subplot( gs[0] )

	plt.title(REGION.replace("_", " ")+" TMPTEST", loc='right')

	for h_info in hs_to_plot:
		if 'Data' in h_info['type']:
			rplt.hist(
				h_info['hist'], 
				label= h_info['label'],
				color= h_info['color'],
				alpha=0.35,
				fill = True,
				zorder=0,
			)
	# ax.set_ylim([0.0001,1.])
	ax.set_xlim([0.1, 70000])
	# ax.set_yscale("log", nonposy='clip')
	ax.set_ylabel('N')
	ax.set_xlabel('Charge (e)')

	leg = ax.legend(loc='upper right', numpoints=1, prop={'size': 10}, ncol=1)
	leg.draw_frame(False)

	gs.tight_layout(fig, rect=[0, 0.03, 1, 0.95])  
	filename = 'TMPTEST_'+REGION
	fig.savefig('plots/TMPTEST/'+filename+'.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()



def apply_max_cutoff(h):
	'''
	Apply the max charge cutoff: 62,500 == bin 126
	'''
	qSum = 0
	bin_edges = list(h.xedges())
	for bin in h.bins_range():
		if bin >= 126: qSum+=h.GetBinContent(bin)
	h.SetBinContent(126, qSum)
	for bin in h.bins_range():
		if bin > 126: h.SetBinContent(bin, 0)
	return h
