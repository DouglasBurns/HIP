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

from argparse import ArgumentParser

def testing_Poisson():
	'''
	Quick test of the poisson random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,100):
		rnd_array.append(mt.return_rnd_Poisson(100))
	count, bins, ignored = plt.hist(rnd_array, 200, normed=True)
	# plt.xlim(0, 200) 
	plt.show()
	return

def testing_Landau():
	'''
	Quick test of the poisson random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,100):
		rnd_array.append(mt.return_rnd_Landau(100, 10))
	count, bins, ignored = plt.hist(rnd_array, 200, normed=True)
	# plt.xlim(0, 200) 
	plt.show()
	return

def testing_Response():
	'''
	Quick test of the response
	MIP 		: 	0 -> 200fC
	Baseline V 	: 	0 mV
	'''
	array = []
	for i in range (0,500): 
		# if i == 139: continue
		array.append(mt.amplifier_response(i, 0))
	fig_resp = plt.figure()
	ax_resp = fig_resp.add_subplot(1, 1, 1)
	plt.plot(array)
	ax_resp.set_xlabel('Input signal [fC]')
	ax_resp.set_ylabel('$V_{out}$')
	fig_resp.savefig('plots/PreAmpResponse.pdf', bbox_inches='tight')
	return

def testing_Gain():
	'''
	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	1MIP 		:	3.75 fC
	'''
	array = []
	for i in range (0,1000): 
		array.append(mt.amplifier_response(3.75, i))
	fig_gain = plt.figure()
	ax_gain = fig_gain.add_subplot(1, 1, 1)
	plt.plot(array)
	ax_gain.set_xlabel('Baseline Voltage [mV]')
	ax_gain.set_ylabel('$V_{out}$ [1MIP]')
	fig_gain.savefig('plots/PreAmpGain.pdf', bbox_inches='tight')
	return



def main():
	'''
	Iterate over time (how long?)
	See if hit in strip
	See what charge is
	See how much charge has bled off in the readout capacitor
	'''
	# Initialisations
	d_sim_variables = {}
	d_sim_variables['bunchCrossing'] = []
	d_sim_variables['isBeam'] = []
	d_sim_variables['nParticleInBX'] = []
	d_sim_variables['V_baseline_mv'] = []
	# d_sim_variables['bledVoltage'] = []
	d_sim_variables['chargeDeposited_e'] = []
	d_sim_variables['chargeDeposited_fC'] = []
	d_sim_variables['chargeCurrent_fC'] = []
	d_sim_variables['V_signal_mv'] = []
	d_sim_variables['timeLastMIP_bx'] = []
	d_sim_variables['timeLastMIP_us'] = []
	d_sim_variables['nMIPS'] = []
	d_sim_variables['V_gain_mv'] = []

	# Testing Distributions
	# testing_Poisson()
	# testing_Landau()
	# testing_Response()
	# testing_Gain()

	n_bx = g.N_MAX_BUNCH_CROSSINGS
	n_particle_in_bx_ave = g.AVE_NUMBER_OF_PARTICLES_IN_BX
	old_baseline_mV = 0
	time_since_last_MIP = 0
	bx = 0
	time_since_last_bx = 1
	n_MIPS = 0

	while (n_MIPS < g.N_MIPS):
		bx += 1

		# if beam is present
		n_particle_in_bx = 0
		n_MIP = 0
		V_gain_mv = 0
		charge_deposited_e = 0
		charge_deposited_fC = 0
		time_since_last_MIP += 1

		if mt.is_beam_present(bx):

			# Calculate number of MIPS in bx  ####
			n_particle_in_bx = mt.return_rnd_Poisson(n_particle_in_bx_ave)
			n_MIP = mt.tracker_hits(g.OCCUPANCY, n_particle_in_bx, n_particle_in_bx_ave)
			n_MIPS += n_MIP
			######################################
			
		# there are MIPs present
		if n_MIP > 0:
			# Calculate charge deposited (e)  ####
			for i in range(0, n_MIP):
				if DEBUG:
					print "-"*50
					print "{} charged particles found in bunch crossing {}".format( n_MIP, bx )
					print "- "*25

				# this depends on the thickness of the chip...
				charge_deposited_e += mt.return_rnd_Landau(g.AVE_CHARGE_DEPOSITED, g.SIGMA_CHARGE_DEPOSITED)
			if DEBUG:
				print "Charge deposited {}e".format(charge_deposited_e)
			######################################


		# Calculate charge deposited (fC) ####
		charge_deposited_fC = mt.charge_transformation(charge_deposited_e, to_fC=True)
		if DEBUG:
			print "Charge deposited {}fC".format(charge_deposited_fC)
		######################################


		# Calculate bleedage (mV)  	 	  ####
		time_since_last_MIP_us = mt.time_transformation(time_since_last_MIP, to_us=True)
		time_since_last_bx_us = mt.time_transformation(time_since_last_bx, to_us=True)
		current_baseline_mV, bled_voltage = mt.bleed_off(old_baseline_mV, time_since_last_bx_us, g.BLEEDOFF_LIFETIME)
		if DEBUG:
			print"Signal voltage at last MIP {}mV".format(old_baseline_mV)
			print"Baseline voltage bled off {}mV".format(bled_voltage)
			print"Current baseline voltage {}mV".format(current_baseline_mV)
		######################################
		

			
		# Voltage response (mV)		 	  ####
		# charge deposited in fC, baseline voltage in mV
		signal_gain, signal_response, total_charge_fC = mt.amplifier_response(charge_deposited_fC, current_baseline_mV)
		if DEBUG:
			print "Signal response {}mV".format(signal_response)
			print "Signal gain {}mV".format(signal_gain)
			print "- "*30
		######################################



		# Add variables to dictionary 	  ####
		d_sim_variables['bunchCrossing'].append(bx)
		d_sim_variables['isBeam'].append(mt.is_beam_present(bx))
		d_sim_variables['nParticleInBX'].append(n_particle_in_bx)
		d_sim_variables['nMIPS'].append(n_MIP)
		d_sim_variables['timeLastMIP_bx'].append(time_since_last_MIP)
		d_sim_variables['timeLastMIP_us'].append(time_since_last_MIP_us)
		d_sim_variables['chargeDeposited_e'].append(charge_deposited_e)
		d_sim_variables['chargeDeposited_fC'].append(charge_deposited_fC)
		d_sim_variables['chargeCurrent_fC'].append(total_charge_fC)
		d_sim_variables['V_baseline_mv'].append(current_baseline_mV)
		# d_sim_variables['bledVoltage'].append(bled_voltage)
		d_sim_variables['V_signal_mv'].append(signal_response)
		d_sim_variables['V_gain_mv'].append(signal_gain)

		######################################

		# Reset some variables 	  		  ####
		old_baseline_mV = signal_response
		if n_MIP > 0: time_since_last_MIP = 0
 		######################################


	sim = pu.dict_to_df(d_sim_variables)
	print sim

	fu.make_folder_if_not_exists('plots/')

	# # PLOT NUMBER OF PARTICLES IN BX
	# fig1 = plt.figure()
	# ax1 = fig1.add_subplot(1, 1, 1)
	# ax1.set_xlim([n_particle_in_bx_ave-3*mt.math.sqrt(n_particle_in_bx_ave),n_particle_in_bx_ave+3*mt.math.sqrt(n_particle_in_bx_ave)])
	# ax1.set_ylim([0, 40000])
	# plt.hist(
	# 	sim['nParticleInBX'], 
	# 	bins=range(min(sim['nParticleInBX']), max(sim['nParticleInBX']) + 1, 1), # For Ints set binsize to 1
	# 	# bins=np.arange(min(data), max(data) + binwidth, binwidth), # For Floats
	# 	facecolor='green', 
	# 	alpha=0.75
	# )
	# ax1.set_xlabel('Number of charged particles in bx')
	# ax1.set_ylabel('N')
	# fig1.savefig('plots/nChargePtcl.pdf', bbox_inches='tight')


	# # PLOT CHARGE DEPOSITED DISTRIBUTION
	# fig2 = plt.figure()
	# ax2 = fig2.add_subplot(1, 1, 1)
	# ax2.set_xlim([0,1*pow(10,5)])
	# ax2.set_ylim([0,1*pow(10,3)])
	# plt.hist(
	# 	sim['chargeDeposited_e'], 
	# 	10000, 
	# 	facecolor='green', 
	# 	alpha=0.75
	# )
	# ax2.set_xlabel('Charge deposited on chip in a bx(fC) ')
	# ax2.set_ylabel('N')
	# fig2.savefig('plots/chargeDeposited.pdf', bbox_inches='tight')

	# PLOT VOUT ###
	fig3 = plt.figure()
	ax3 = fig3.add_subplot(1, 1, 1)
	plt.plot(
		# kind='line',
		sim['bunchCrossing'], 
		sim['V_signal_mv'],
	)
	ax3.set_xlim([0,15000])
	ax3.set_ylim([0,1000])
	ax3.set_xlabel('Bunch Crossing ')
	ax3.set_ylabel('Signal Voltage')
	fig3.savefig('plots/VoutTau'+str(g.BLEEDOFF_LIFETIME)+'.pdf', bbox_inches='tight')


	# PLOT BEAM STRUCTURE ###
	fig4 = plt.figure()
	ax4 = fig4.add_subplot(1, 1, 1)
	plt.plot(
		sim['bunchCrossing'], 
		sim['isBeam'],
		color='green',
		lw=0,
	)
	# Line signalling structure bound
	for i in sim['bunchCrossing']:
		if (i % 3564) == 0:
			ax4.axvline(i, color='blue', lw=2, alpha=0.5)
	ax4.set_xlim([0,10000])
	ax4.set_ylim([0,2])
	ax4.fill_between(sim['bunchCrossing'], 0, sim['isBeam'], facecolor='green')
	ax4.set_xlabel('Bunch Crossing ')
	ax4.set_ylabel('Beam Present')
	fig4.savefig('plots/BeamStructure.pdf', bbox_inches='tight')

	# # PLOT Charge v bx ###
	# fig5 = plt.figure()
	# ax5 = fig5.add_subplot(1, 1, 1)
	# plt.plot(
	# 	# kind='line',
	# 	sim['bunchCrossing'], 
	# 	sim['chargeCurrent_fC'],
	# )
	# ax5.set_xlim([0, 10000])
	# ax5.set_ylim([0,300])
	# ax5.set_xlabel('Bunch Crossing ')
	# ax5.set_ylabel('Charge in Strip [fC]')
	# fig5.savefig('plots/qTau'+str(g.BLEEDOFF_LIFETIME)+'.pdf', bbox_inches='tight')

# 	# sim.plot(kind='line', x='time', y='charge')
# 	# sim.plot(kind='line', x='time', y='charge', ylim=(0,500))
# 	# sim.plot(kind='line', x='time', y='charge', xlim=(0,2000), ylim=(0,500))

	plt.show()


if __name__ == "__main__":
	# https://docs.python.org/2/library/argparse.html#module-argparse
	parser = ArgumentParser(description='Calculates the charge on a APV')
	parser.add_argument( "-d", "--debug", 
		dest = "debug",
		action = "store_true", 
		# default = False, 
		help = "For debugging" )
	args = parser.parse_args()
	DEBUG = args.debug

	main()