import global_vars as g

# import root
import ROOT
from rootpy.plotting import Hist
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import gc

mpl.rcParams['agg.path.chunksize'] = 50000

def run_distributions(title, folder_path, d_mip_variables, sim, NOISE):
	'''
	Plot any ditributions
	'''
	print "- - - - - - - - - - - - - - - - - - -"
	print "Plotting Simulation Distributions"
	print "- - - - - - - - - - - - - - - - - - -"
	########################################################################################################################
	### N STRIP HITS
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['n_MIP_bx'], 
		bins=np.arange(-0.5, 3.5, 1),
		facecolor='green', 
		alpha=1
	)
	ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('$N_{Hit}$')
	ax.set_ylabel('N')
	fig.suptitle('Number of Charged Hits on Strip in BX', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	fig.savefig(folder_path+'nMIP.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### SIGNAL CHARGE DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	# plt.hist(
	# 	[sim['q_Deposited_fC'],sim['q_HIP_fC']], 
	# 	np.arange(0.5, 50.5, 1),
	# 	histtype='step',
	# 	label=['MIP Charge','HIP Charge'],
	# 	# edgecolor='black',
	# 	alpha=1,
	# 	fill = True,
	# 	stacked=True
	# )
	plt.hist(
		d_mip_variables['q_Deposited_fC'], 
		np.arange(0, 50, 1),
		histtype='step',
		label='MIP Charge',
		edgecolor='black',
		alpha=1,
		fill = True,
		# stacked=True
	)
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlim([0,50])
	fig.suptitle('Charge Distribution Deposited on Strip', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	ax.set_xlabel('Charge deposited on APV in a bx(fC) ')
	ax.set_ylabel('N')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'ChargeDepositedInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### AMPLIFIER GAIN DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		d_mip_variables['V_gain_mv'], 
		bins=np.arange(0.05, 6.05, 0.05), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
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

	########################################################################################################################
	### AMPLIFIER BASELINE DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		d_mip_variables['V_baseline_mv'], 
		bins=np.arange(min(sim['V_baseline_mv']), 740, 10), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	ax.set_xlim([0, 720])
	fig.suptitle('Amplifier Baseline Voltage Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('Voltage Baseline [mV]')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'BaselineInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### AMPLIFIER V_OUT - V_0 DISTRIBUTION
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		d_mip_variables['V_diff_mv'], 
		bins=np.arange(0, 100, 1), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	plt.axvline(x=g.EFFECTIVE_THRESHOLD, linewidth=4, color='r', label = 'Min Threshold')
	# ax.set_xlim([0, 720])
	fig.suptitle('Amplifier $V_{out}-V_{0}$ Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('$V_{out}-V_{0}$ [mV]')
	ax.set_ylabel('N')

	# leg = plt.legend(loc='best')
	# leg.draw_frame(False)	

	fig.savefig(folder_path+'ResponseInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Track Eta Distribution
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		d_mip_variables['track_eta'], 
		bins=np.arange(-1., 1., 0.01), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	fig.suptitle('Track $\eta$ Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('$\eta$')
	ax.set_ylabel('N')

	fig.savefig(folder_path+'TrackEta.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### Track Length Distribution
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		d_mip_variables['track_length'], 
		bins=np.arange(200, 800, 10), # For Floats
		histtype='step',	
		color='black',
		facecolor='green', 
		alpha=1,
		fill=True,
	)
	fig.suptitle('Silicon Track Length Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('Track Length')
	ax.set_ylabel('N')

	fig.savefig(folder_path+'TrackLength.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### SPECIALIST PLOTS
	########################################################################################################################

	########################################################################################################################
	### SIGNAL DEPENDENCE ON BUNCH PRESENCE
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ))
	ax = fig.add_subplot(1, 1, 1)
	ax.set_xlim([0,10000])
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
		sim['V_signal_mv'],
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
	return
