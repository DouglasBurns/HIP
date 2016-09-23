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
	# Testing Distributions
	# testing_Poisson()
	# testing_Landau()
	# testing_Response()
	# testing_Response2()

	# Initialisations
	time_to_strip_hit = 0			# Initialise to t=0
	time_of_simulation = 0			# Initialise to t=0
	charge_in_APV = 0				# Initialise to no charge in APV
	reduced_charge_in_APV = 0		# Initialise to no left over charge in APV
	d_sim_variables = {}			# At t=0, there is no charge
	d_sim_variables['time'] = []
	d_sim_variables['timeAve'] = []
	d_sim_variables['charge'] = []
	d_sim_variables['chargeDepos'] = []

	for i in range(0, g.N_MIPS):
		if DEBUG:
			print "-"*50
			print "Charge Particle {} ".format(i+1)
			print "- "*25

		# The next successive strip hit is Poisson. (What is the mean of the poisson though? something to do with average time for interaction?)
		# In ms/ps/ns?

		# Calculate time to next hit      ####
		time_to_strip_hit = mt.return_rnd_Poisson(g.AVE_TIME_FOR_STRIP_HIT)
		time_of_simulation += time_to_strip_hit

		if DEBUG:
			print"Time taken for next particle to hit strip {} ".format(time_to_strip_hit)
		######################################
	
	
		# Calculate amount of charge bled ####
		reduced_charge_in_APV, charge_bled_off = mt.bleed_off_charge(charge_in_APV, time_to_strip_hit, g.BLEEDOFF_LIFETIME)

		if DEBUG:
			print"Old charge in APV {} ".format(charge_in_APV)
			print"Charge bled off {} ".format(charge_bled_off)
			print"Charge after bleedoff {} ".format(reduced_charge_in_APV)
		######################################
	

		# Calculate charge deposited      ####
		charge_deposited_in_APV = mt.return_rnd_Landau(g.AVE_ENERGY_FOR_STRIP_HIT, g.SIGMA_ENERGY_FOR_STRIP_HIT)
		charge_in_APV = reduced_charge_in_APV + charge_deposited_in_APV

		if DEBUG:
			print"New charge deposited in APV {} ".format(charge_deposited_in_APV)
			print"Current charge in APV {} ".format(charge_in_APV)
		######################################




		# Charge to Voltage Signal        ####

'''
x0 = max linear range (139)
x = signal (4*sig/25000??)

mV vs fC signal

V = 5.02*x-0.00333*x^2 x<139
V = 717 - 83.5*exp(-(x-139)/75.5) x>139



'''






		######################################


		# Add charge in APV at this time  ####
		d_sim_variables['charge'].append(charge_in_APV)
		d_sim_variables['chargeDepos'].append(charge_deposited_in_APV)
		d_sim_variables['timeAve'].append(time_to_strip_hit)
		d_sim_variables['time'].append(time_of_simulation)
		######################################

	sim = pu.dict_to_df(d_sim_variables)
	if DEBUG:
		print sim
	print sim

	fu.make_folder_if_not_exists('plots/')


	fig1 = plt.figure()
	ax1 = fig1.add_subplot(1, 1, 1)
	plt.hist(
		sim['timeAve'], 
		bins=range(min(sim['timeAve']), max(sim['timeAve']) + 1, 1), # For Ints set binsize to 1
		# bins=np.arange(min(data), max(data) + binwidth, binwidth), # For Floats
		facecolor='green', 
		alpha=0.75
	)
	ax1.set_xlabel('Time between incoming particles')
	ax1.set_ylabel('N')
	fig1.savefig('plots/t.pdf', bbox_inches='tight')

	fig2 = plt.figure()
	ax2 = fig2.add_subplot(1, 1, 1)
	ax2.set_xlim([0,0.5*pow(10,6)])
	plt.hist(
		sim['chargeDepos'], 
		10000, 
		facecolor='green', 
		alpha=0.75
	)
	ax2.set_xlabel('Charge on incoming particle (fC) ')
	ax2.set_ylabel('N')
	fig2.savefig('plots/e.pdf', bbox_inches='tight')


	# sim.plot(kind='line', x='time', y='charge')
	# sim.plot(kind='line', x='time', y='charge', ylim=(0,500))
	# sim.plot(kind='line', x='time', y='charge', xlim=(0,2000), ylim=(0,500))

	plt.show()
		# Total charge in capacitor		  ####

		######################################

		######################################

		# Capacitor Readout     		  ####

		######################################

		######################################

		# Testing 						  ####
		# small charges
		# large charges
		# small timescale
		# large timescale
		# dampening tau (us)
		######################################

		# number of signals... not iterations.




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