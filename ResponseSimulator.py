'''
Why is the HIP problem not a problem?
1) Chip contains a charge sensitive capacitor. i.e. some charge in, some voltage out.
2) A shaper reduces signal forming a pulse.
3) For a small pulse this is linear response. At some point the input charge maximises the out voltage
	and it becomes non linear. Uh Oh.
4) To get rid of the charge in the capacitor fully, a current is passed through capacitor. Reduces this
	by an exponential decay with time constant. Previously time constant too large, so charge built up
	in capacitor leading to non linear response, leading to smaller and smaller pulses.
5) HIP fix introduced (basically a parameter giving this time constant) allowed much more efficient
	bleeding

Simulate whether this is actually whats happening
1) For a given bunch, what is the probability that a strip is hit
	Poisson distribution
2) Given that the strip is hit, what is the charge deposited?
	Landau distribution
3) Charge arriving vs amount of charge bled
	Expontential decay with time constant
4) Is the charge split over multiple strips?
5) Dependent on bunch intensity?
6) Output of shaper?
7) Preamplifier response
	V vs Q
'''
from __future__ import division

import global_vars as g
import mathematical_tools as mt
import matplotlib.pyplot as plt
import numpy as np
import pandas_utils as pu
import file_utils as fu
import gc

from argparse import ArgumentParser


def arg_parser():
	parser = ArgumentParser(description='Calculates the charge on a APV')
	parser.add_argument( "-d", "--debug", 
		dest = "debug",
		action = "store_true", 
		# default = False, 
		help = "For debugging" )
	parser.add_argument( "-t", "--tests", 
		dest = "tests",
		action = "store_true", 
		# default = False, 
		help = "For debugging" )
	args = parser.parse_args()
	return args


def testing_Poisson():
	'''
	Quick test of the poisson random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(mt.return_rnd_Poisson(10))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 30, range=[0, 30], normed=True)
	ax.set_xlabel('Po()')
	ax.set_ylabel('N')
	fig.savefig('plots/PoissonRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return

def testing_Gaussian():
	'''
	Quick test of the Gaussian random number generation
	Mean = 0
	Sigma = 1
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(mt.return_rnd_Gaussian(0,1))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 30, range=[-5, 5], normed=True)
	ax.set_xlabel('Gaussian()')
	ax.set_ylabel('N')
	fig.savefig('plots/GaussianRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return

def testing_Landau():
	'''
	Quick test of the Landau random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(mt.return_rnd_Landau(100, 10))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 125, range=[0, 500], normed=True)
	ax.set_xlabel('Landau()')
	ax.set_ylabel('N')
	fig.savefig('plots/LandauRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def testing_Response():
	'''
	Quick test of the response
	MIP 		: 	0 -> 200fC
	Baseline V 	: 	0 mV
	'''
	array = []
	for i in range (0,400): 
		gain, v, signal_q = mt.amplifier_response(i, 0)
		array.append(gain)
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(array)
	ax.set_xlabel('Input signal [fC]')
	ax.set_ylabel('$V_{out}$')
	fig.savefig('plots/PreAmpResponse.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def testing_Gain():
	'''
	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	1MIP 		:	3.75 fC
	'''
	array = []
	for i in range (0,1000): 
		gain, v, signal_q = mt.amplifier_response(3.75, i)
		array.append(gain)
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(array)
	ax.set_xlabel('Baseline Voltage [mV]')
	ax.set_ylabel('$Gain$ [1MIP]')
	fig.savefig('plots/PreAmpGain.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def testing_BeamStructure():
	'''
	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	1MIP 		:	3.75 fC
	'''
	array_bx = []
	array_beam = []
	for i in range (1,3564):
		array_bx.append(i)
		if mt.is_beam_present(i):
			array_beam.append(1)
		else: 
			array_beam.append(0)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(
		array_bx, 
		array_beam,
		color='green',
		lw=0,
	)
	ax.set_ylim([0,1.1])
	ax.set_xlim([0,3564])
	ax.fill_between(array_bx, 0, array_beam, facecolor='green')
	ax.set_xlabel('Bunch Crossing')
	ax.set_ylabel('Beam Present')
	fig.savefig('plots/BeamStructure.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def run_tests():
	'''
	Run various tests
	'''
	# Test Poisson RNG
	testing_Poisson()
	# Test Gaussian RNG
	testing_Gaussian()
	# Test Landau RNG
	testing_Landau()
	# Test response for MIP using 0 baseline voltage
	testing_Response()
	# Test gain using MIP of 3.75fC
	testing_Gain()
	# Show the LHC beam structure in use
	testing_BeamStructure()
	return


def main(args):
	'''
	Iterate over time (how long?)
	See if hit in strip
	See what charge is
	See how much charge has bled off in the readout capacitor
	'''
	DEBUG = args.debug
	TESTS = args.tests

	# Initialisations
	d_sim_variables 						= {}
	d_sim_variables['bunchCrossing'] 		= []
	d_sim_variables['isBeam'] 				= []
	d_sim_variables['timeLastMIP_bx'] 		= []
	# d_sim_variables['timeLastMIP_us'] 		= []
	d_sim_variables['nParticleInBX']		= []
	d_sim_variables['V_baseline_mv'] 		= []
	d_sim_variables['V_bleed_mv'] 			= []
	d_sim_variables['V_signal_mv'] 			= []
	d_sim_variables['V_gain_mv']			= []
	d_sim_variables['V_Noise_mv'] 			= []
	d_sim_variables['q_Deposited_e'] 		= []
	d_sim_variables['q_Deposited_fC']	 	= []
	d_sim_variables['q_HIP_fC'] 			= []
	d_sim_variables['q_Current_fC'] 		= []
	d_sim_variables['n_MIPS'] 				= []
	d_sim_variables['n_MIP'] 				= []
	d_sim_variables['n_HIPS'] 				= []
	d_sim_variables['n_HIP'] 				= []
	MIPInBX									= []
	HIPInBX									= []
	multiMIPInBX							= []
	highMIPInBX								= []

	# Testing Distributions
	if TESTS: 
		print "Running Tests"
		run_tests()
		return

	# n_bx 									= g.N_MAX_BUNCH_CROSSINGS
	n_particle_in_bx_ave 					= g.AVE_NUMBER_OF_PARTICLES_IN_BX
	old_baseline_mV 						= 0
	time_since_last_MIP 					= 0
	bx 										= 0
	time_since_last_bx 						= 1
	n_MIPS 									= 0
	n_HIPS									= 0


	while (n_MIPS < g.N_MIPS):
		bx += 1

		n_particle_in_bx 		= 0
		n_MIP 					= 0
		n_HIP 					= 0
		V_gain_mv 				= 0
		charge_deposited_e 		= 0
		charge_deposited_fC 	= 0
		charge_MIP_e			= 0
		charge_MIP_fC			= 0
		charge_HIP_e			= 0
		charge_HIP_fC			= 0
		electronic_noise_mV		= 0

		time_since_last_MIP 	+= 1
		isHIP					= False

		########################################################################################################################
		### Calculate number of MIPS in bx (if bx present)
		########################################################################################################################
		if mt.is_beam_present(bx):
			n_particle_in_bx 	= mt.return_rnd_Poisson(n_particle_in_bx_ave)
			n_MIP 				= mt.tracker_hits(g.OCCUPANCY, n_particle_in_bx, n_particle_in_bx_ave)
			n_MIPS 				+= n_MIP
			
		########################################################################################################################
		### Calculate charge (e) of MIPS (if MIPS present)
		########################################################################################################################
		if n_MIP > 0:
			MIPInBX.append(bx)
			if n_MIP > 1: multiMIPInBX.append(bx)
			for i in range(0, n_MIP):
				# Is the MIP a HIP
				isHIP = mt.is_HIP(g.HIP_OCCUPANCY)
				if isHIP:
					# Where are the HIPs
					HIPInBX.append(bx)
					n_HIP 				+= 1
					n_HIPS 				+= 1
					charge_HIP_e 		= mt.return_HIP_charge()
					charge_deposited_e 	+= charge_HIP_e
				else:
					# this depends on the thickness of the chip...
					charge_MIP_e 		= mt.return_rnd_Landau(g.AVE_CHARGE_DEPOSITED, g.SIGMA_CHARGE_DEPOSITED)
					charge_deposited_e 	+= charge_MIP_e

			if DEBUG:
				print "-"*50
				print "{} charged particles found in bunch crossing {}".format( n_MIP, bx )
				print "{} charged particles were HIPs".format( n_HIP )
				print "- "*25
				print "Total Charge deposited {}e".format(charge_deposited_e)

		########################################################################################################################
		### Calculate charge (fc) of MIPS
		########################################################################################################################
		charge_deposited_fC = mt.charge_transformation(charge_deposited_e, to_fC=True)
		if DEBUG:
			print "Charge deposited {}fC".format(charge_deposited_fC)

		# Where are the highy charged MIPS
		charge_MIP_fC = mt.charge_transformation(charge_MIP_e, to_fC=True)
		if charge_MIP_fC > 50:
			highMIPInBX.append(bx)

		if isHIP:
			charge_HIP_fC = mt.charge_transformation(charge_HIP_e, to_fC=True)
			if DEBUG:
				print "Charge HIP deposited {}fC".format(charge_HIP_fC)

		########################################################################################################################
		### Calculate bleedage (mV) since last MIP
		########################################################################################################################
		time_since_last_MIP_us 				= mt.time_transformation(time_since_last_MIP, to_us=True)
		time_since_last_bx_us  				= mt.time_transformation(time_since_last_bx, to_us=True)
		current_baseline_mV, bled_voltage 	= mt.bleed_off(old_baseline_mV, time_since_last_bx_us, g.BLEEDOFF_LIFETIME)
		if DEBUG:
			print "Signal voltage at last MIP {}mV".format(old_baseline_mV)
			print "Baseline voltage bled off {}mV".format(bled_voltage)
			print "Current baseline voltage {}mV".format(current_baseline_mV)
		

		########################################################################################################################
		### New Response (mV) (charge in fC, voltage in mV)
		########################################################################################################################			
		signal_gain, signal_response, total_charge_fC, electronic_noise_mV = mt.amplifier_response(charge_deposited_fC, current_baseline_mV)
		if signal_response < 0:
			print "Signal voltage at last MIP {}mV".format(old_baseline_mV)
			print "Baseline voltage bled off {}mV".format(bled_voltage)
			print "Current baseline voltage {}mV".format(current_baseline_mV)
			print "Total Charge deposited {}e".format(charge_deposited_e)
			print "Charge deposited {}fC".format(charge_deposited_fC)
			print "Signal response {}mV".format(signal_response)
			print "Signal gain {}mV".format(signal_gain)
			print "{} charged particles found in bunch crossing {}".format( n_MIP, bx )
			print "{} charged particles were HIPs".format( n_HIP )
			raw_input("Press ENTER to continue.")

		if DEBUG:
			print "Signal response {}mV".format(signal_response)
			print "Signal gain {}mV".format(signal_gain)
			print "- "*30


		########################################################################################################################
		### Add parameters to dictionary
		########################################################################################################################
		d_sim_variables['bunchCrossing'].append(bx)
		d_sim_variables['isBeam'].append(mt.is_beam_present(bx))
		d_sim_variables['nParticleInBX'].append(n_particle_in_bx)
		d_sim_variables['n_MIPS'].append(n_MIPS)
		d_sim_variables['n_MIP'].append(n_MIP)
		d_sim_variables['n_HIPS'].append(n_HIPS)
		d_sim_variables['n_HIP'].append(n_HIP)
		d_sim_variables['timeLastMIP_bx'].append(time_since_last_MIP)
		# d_sim_variables['timeLastMIP_us'].append(time_since_last_MIP_us)
		d_sim_variables['q_Deposited_e'].append(charge_deposited_e)
		d_sim_variables['q_Deposited_fC'].append(charge_deposited_fC)
		d_sim_variables['q_HIP_fC'].append(charge_HIP_fC)
		d_sim_variables['q_Current_fC'].append(total_charge_fC)
		d_sim_variables['V_Noise_mv'].append(electronic_noise_mV)
		d_sim_variables['V_baseline_mv'].append(current_baseline_mV)
		d_sim_variables['V_bleed_mv'].append(bled_voltage)
		d_sim_variables['V_signal_mv'].append(signal_response)
		d_sim_variables['V_gain_mv'].append(signal_gain)

		########################################################################################################################
		### Reintitialise for next MIP
		########################################################################################################################
		old_baseline_mV = signal_response
		if n_MIP > 0: time_since_last_MIP = 0

	########################################################################################################################
	### Pandasify the dictionary (All MIPS over time)
	########################################################################################################################
	sim = pu.dict_to_df(d_sim_variables)
	print sim

	########################################################################################################################
	### Plots
	########################################################################################################################
	folder_path = 'plots/Tau'+str(g.BLEEDOFF_LIFETIME)+'/'
	fu.make_folder_if_not_exists(folder_path)

	########################################################################################################################
	### Number Of Particles In BX
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['nParticleInBX'], 
		bins=range(min(sim['nParticleInBX']), max(sim['nParticleInBX']) + 1, 1), # For Ints set binsize to 1
		# bins=np.arange(min(data), max(data) + binwidth, binwidth), # For Floats
		facecolor='green', 
		alpha=1
	)
	ax.set_yscale("log", nonposy='clip')
	ax.set_xlim([n_particle_in_bx_ave-4*mt.math.sqrt(n_particle_in_bx_ave),n_particle_in_bx_ave+4*mt.math.sqrt(n_particle_in_bx_ave)])
	# ax.set_ylim([0, sim['nParticleInBX'].max()])
	ax.set_xlabel('Number of charged particles in bx')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'nChargePtcl.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### Number Of Hits In Tracker
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['n_MIP'], 
		bins=range(0, 6, 1), # For Ints set binsize to 1
		facecolor='green', 
		alpha=1
	)
	ax.set_yscale("log", nonposy='clip')
	ax.set_xlabel('Number of charged particles hitting strip')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'nMIP.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### Total Charge Deposited On Chip
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['q_Deposited_fC'], 
		bins=range(1, 100, 1), # For Ints set binsize to 1
		facecolor='green', 
		alpha=1
	)
	# ax.set_yscale("log", nonposy='clip')
	ax.set_xlim([0,100])
	# ax.set_ylim([0,sim['chargeDeposited_fC'].max()])
	ax.set_xlabel('Charge deposited on APV in a bx(fC) ')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'chargeDeposited.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Charge Deposited On Chip by HIPs
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.hist(
		sim['q_HIP_fC'], 
		bins=range(1, 1000, 50), # For Ints set binsize to 1
		facecolor='green', 
		alpha=1
	)
	# ax.set_yscale("log", nonposy='clip')
	# ax.set_xlim([0,100])
	# ax.set_ylim([0,sim['chargeDeposited_fC'].max()])
	ax.set_xlabel('Charge deposited by HIP on APV in a bx(fC) ')
	ax.set_ylabel('N')
	fig.savefig(folder_path+'chargeDepositedByHIP.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### Voltage Out On APV
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )
	for highMIP in highMIPInBX:
		label = ''
		if highMIP == highMIPInBX[0]: label = 'Highly Charged MIP (>50fC)'
		plt.axvline( x = highMIP, color = 'black', linewidth=1, alpha = 1, label=label )
	for multiMIP in multiMIPInBX:
		label = ''
		if multiMIP == multiMIPInBX[0]: label = 'Multiple MIPs'
		plt.axvline( x = multiMIP, color = 'green', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		# kind='line',
		sim['bunchCrossing'], 
		sim['V_signal_mv'],
		label='V_Out',
	)
	ax.set_xlim([0,g.N_MAX_BUNCH_CROSSINGS])
	ax.set_ylim([0,720])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('V_{out} in APV [mV]')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'VoltageInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	########################################################################################################################
	### Gain On APV
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	# for MIP in MIPInBX:
	# 	label = ''
	# 	if MIP == MIPInBX[0]: label = 'MIP'
	# 	plt.axvline( x = MIP, color = 'black', linewidth = 1, alpha = 0.25, label=label )
	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )
	for highMIP in highMIPInBX:
		label = ''
		if highMIP == highMIPInBX[0]: label = 'Highly Charged MIP (>50fC)'
		plt.axvline( x = highMIP, color = 'black', linewidth=1, alpha = 1, label=label )
	for multiMIP in multiMIPInBX:
		label = ''
		if multiMIP == multiMIPInBX[0]: label = 'Multiple MIPs'
		plt.axvline( x = multiMIP, color = 'green', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		sim['bunchCrossing'], 
		sim['V_gain_mv'], 
		label='Gain',
	)
	ax.set_xlim([0,g.N_MAX_BUNCH_CROSSINGS])
	ax.set_ylim([0,720])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Gain [mV]')

	leg = plt.legend(loc='upper right')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'GainInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Total Charge On APV
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)

	for HIP in HIPInBX:
		label = ''
		if HIP == HIPInBX[0]: label = 'HIP'
		plt.axvline( x = HIP, color = 'red', linewidth = 1, alpha = 1, label=label )
	for highMIP in highMIPInBX:
		label = ''
		if highMIP == highMIPInBX[0]: label = 'Highly Charged MIP (>50fC)'
		plt.axvline( x = highMIP, color = 'black', linewidth=1, alpha = 1, label=label )
	for multiMIP in multiMIPInBX:
		label = ''
		if multiMIP == multiMIPInBX[0]: label = 'Multiple MIPs'
		plt.axvline( x = multiMIP, color = 'green', linewidth = 1, alpha = 1, label=label )

	plt.plot(
		sim['bunchCrossing'], 
		sim['q_Current_fC'],
		label='q current',
	)
	ax.set_xlim([0, g.N_MAX_BUNCH_CROSSINGS])
	ax.set_ylim([0, 250])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Charge in APV [fC]')

	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'ChargeInAPV.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	#########################################################################################################################
	### Electronic Noise
	########################################################################################################################
	fig = plt.figure(figsize = ( 40, 10 ), dpi = 400)
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(
		sim['bunchCrossing'], 
		sim['V_Noise_mv'],
		label='Electronic Noise',
	)
	ax.set_xlim([0, g.N_MAX_BUNCH_CROSSINGS])
	ax.set_ylim([-20, 20])
	ax.set_xlabel('Bunch Crossing ')
	ax.set_ylabel('Electronic Noise in APV [mV]')
	
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	

	fig.savefig(folder_path+'electronicNoise.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

if __name__ == "__main__":
	args = arg_parser()
	main(args)