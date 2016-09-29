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
	plt.plot(array)
	# plt.xlim(0, 200) 
	plt.show()

def testing_Response2():
	'''
	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	MIP 		:	3.75 fC
	'''
	array = []
	for i in range (0,500): 
		array.append(mt.amplifier_response(3.75, i*2))
	plt.plot(array)
	# plt.xlim(0, 200) 
	plt.show()

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
	d_sim_variables['nParticleInBX'] = []
	d_sim_variables['baselineVoltage'] = []
	d_sim_variables['bledVoltage'] = []
	d_sim_variables['chargeDeposited'] = []
	d_sim_variables['signalVoltage'] = []
	d_sim_variables['lastMIP_bx'] = []
	d_sim_variables['nMIPS'] = []

	# Testing Distributions
	# testing_Poisson()
	# testing_Landau()
	# testing_Response()
	# testing_Response2()

	n_bx = g.N_MAX_BUNCH_CROSSINGS
	n_particle_in_bx_ave = g.AVE_NUMBER_OF_PARTICLES_IN_BX
	old_baseline_mV = 0
	time_since_last_MIP = 0
	charge_deposited = 0

	for bx in range(0, n_bx):

		time_since_last_MIP += 1
		if not mt.is_beam_present(bx): continue

		# Calculate number of MIPS in bx  ####
		n_particle_in_bx = mt.return_rnd_Poisson(n_particle_in_bx_ave)
		n_MIP = mt.tracker_hits(g.OCCUPANCY, n_particle_in_bx, n_particle_in_bx_ave)
		if n_MIP == 0: continue
		######################################


		# Calculate charge deposited (e)  ####
		for i in range(0, n_MIP):
			if DEBUG:
				print "-"*50
				print "{} charged particles found in bunch crossing {}".format( n_MIP, bx+1)
				print "- "*25

			# this depends on the thickness of the chip...
			charge_deposited += mt.return_rnd_Landau(g.AVE_CHARGE_DEPOSITED, g.SIGMA_CHARGE_DEPOSITED)
		if DEBUG:
			print "Charge deposited {}e".format(charge_deposited)
		######################################

		# Calculate charge deposited (fC) ####
		charge_deposited = mt.charge_transformation(charge_deposited, to_fC=True)
		if DEBUG:
			print "Charge deposited {}fC".format(charge_deposited)
		######################################

		# Calculate bleedage (mV)  	 	  ####
		time_since_last_MIP_us = mt.time_transformation(time_since_last_MIP, to_us=True)
		current_baseline_mV, bled_voltage = mt.bleed_off(old_baseline_mV, time_since_last_MIP_us, g.BLEEDOFF_LIFETIME)
		if DEBUG:
			print"Signal voltage at last MIP {}mV".format(old_baseline_mV)
			print"Baseline voltage bled off {}mV".format(bled_voltage)
			print"Current baseline voltage {}mV".format(current_baseline_mV)
		######################################
	

		
		# Voltage response (mV)		 	  ####
		# charge deposited in fC, baseline voltage in mV
		signal_response = mt.amplifier_response(charge_deposited, current_baseline_mV)
		if DEBUG:
			print "Signal response {}mV".format(signal_response)
		######################################



		# Add variables to dictionary 	  ####
		d_sim_variables['bunchCrossing'].append(bx+1)
		d_sim_variables['baselineVoltage'].append(current_baseline_mV)
		d_sim_variables['bledVoltage'].append(bled_voltage)
		d_sim_variables['chargeDeposited'].append(charge_deposited)
		d_sim_variables['signalVoltage'].append(signal_response)
		d_sim_variables['lastMIP_bx'].append(time_since_last_MIP)
		d_sim_variables['nMIPS'].append(n_MIP)
		d_sim_variables['nParticleInBX'].append(n_particle_in_bx)

		######################################

		# Reset some variables 	  		  ####
		old_baseline_mV = signal_response
		charge_deposited = 0
		time_since_last_MIP = 0
 		######################################


	sim = pu.dict_to_df(d_sim_variables)
	if DEBUG:
		print sim

	fu.make_folder_if_not_exists('plots/')


	fig1 = plt.figure()
	ax1 = fig1.add_subplot(1, 1, 1)
	plt.hist(
		sim['nParticleInBX'], 
		bins=range(min(sim['nParticleInBX']), max(sim['nParticleInBX']) + 1, 1), # For Ints set binsize to 1
		# bins=np.arange(min(data), max(data) + binwidth, binwidth), # For Floats
		facecolor='green', 
		alpha=0.75
	)
	ax1.set_xlabel('Number of charged particles in bx')
	ax1.set_ylabel('N')
	fig1.savefig('plots/bChargePtcl.pdf', bbox_inches='tight')

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1, 1, 1)
	# ax2.set_xlim([0,0.5*pow(10,6)])
	plt.hist(
		sim['chargeDeposited'], 
		10000, 
		facecolor='green', 
		alpha=0.75
	)
	ax2.set_xlabel('Charge deposited on chip in bx(fC) ')
	ax2.set_ylabel('N')
	fig2.savefig('plots/e.pdf', bbox_inches='tight')


# 	# sim.plot(kind='line', x='time', y='charge')
# 	# sim.plot(kind='line', x='time', y='charge', ylim=(0,500))
# 	# sim.plot(kind='line', x='time', y='charge', xlim=(0,2000), ylim=(0,500))

	plt.show()
# 		# Total charge in capacitor		  ####

# 		######################################

# 		######################################

# 		# Capacitor Readout     		  ####

# 		######################################

# 		######################################

# 		# Testing 						  ####
# 		# small charges
# 		# large charges
# 		# small timescale
# 		# large timescale
# 		# dampening tau (us)
# 		######################################

# 		# number of signals... not iterations.




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