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

mpl.rcParams['agg.path.chunksize'] = 200000

def run_profiles(title, folder_path, sim, HIPInBX):
	'''
	Plot any projections
	'''
	print "- - - - - - - - - - - - - - - - - - -"
	print "Plotting Simulation Profiles"
	print "- - - - - - - - - - - - - - - - - - -"
	########################################################################################################################
	### APV RESPONSE PROJECTION
	########################################################################################################################
	fig = plt.figure(figsize = ( 20, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		sim['bunchCrossing'], 
		sim['V_signal_mv'],
		label='V_Out',
	)
	ax.set_xlim([0,200000])
	ax.set_ylim([0,730])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('V_{out} in APV [mV]')
	fig.suptitle('Amplifier Response Projection', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'VoltageProjectionInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### APV SIGNAL CHARGE PROJECTION
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		sim['bunchCrossing'], 
		sim['q_baseline_fC'],
		label='q current',
	)
	ax.set_xlim([0, 200000])
	ax.set_ylim([0, 250])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Charge in APV [fC]')
	fig.suptitle('Amplifier Signal Charge Projection', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'ChargeProjectionInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### APV GAIN PROJECTION
	########################################################################################################################
	fig = plt.figure(figsize = ( 20, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		sim['bunchCrossing'], 
		sim['V_gain_mv'], 
		label='Gain',
	)
	fig.suptitle('Amplifier Gain Projection', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	ax.set_xlim([0,200000])
	ax.set_ylim([0,6])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Gain [mV/fC]')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'GainProjectionInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	#########################################################################################################################
	### APV ELECTRONIC NOISE PROJECTION
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(
		sim['bunchCrossing'], 
		sim['V_noise_mv'],
		label='Electronic Noise',
	)
	ax.set_xlim([0, 200000])
	ax.set_ylim([-20, 20])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Electronic Noise in APV [mV]')
	fig.suptitle('Amplifier Noise Projection', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')	
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'electronicNoise.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	return