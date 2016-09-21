'''
Why is the HIP problem not a problem?
1) Chip contains a charge sensitive capacitor. i.e. some charge in, some voltage out.
2) A shaper reduces signal forming a pulse.
3) For a small pulse this is linear response. At some point the input charge maximises the out voltage
	and it becomes non linear. Uh Oh.
4) To get rid of the charge in the capacitor fully a current is passed through capacitor. Reduces this
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

from argparse import ArgumentParser

def return_is_strip_hit():
	'''
	Is the strip hit in this iteration of time?
	Return depending on Poisson random number
	'''
	is_Hit(False)
	return is_Hit

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

	# Initialisations
	time_to_strip_hit = 0			# Initialise to t=0
	charge_in_APV = 0				# Initialise to no charge in APV
	reduced_charge_in_APV = 0			# Initialise to no left over charge in APV

	for i in range(0, g.N_MIPS):
		if DEBUG:
			print "-"*50
			print "Charge Particle {} ".format(i+1)
			print "- "*25
		# The next successive strip hit is Poisson. (What is the mean of the poisson though? something to do with average time for interaction?)
		# In ms/ps/ns?
		time_to_strip_hit = mt.return_rnd_Poisson(g.AVE_TIME_FOR_STRIP_HIT)

		if DEBUG:
			print"Time taken for next particle to hit strip {} ".format(time_to_strip_hit)

		######################################
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



		######################################

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