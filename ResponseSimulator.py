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


# AVE_ENERGY_FOR_STRIP_HIT
# AVE_SIGMA_ENERGY_FOR_STRIP_HIT
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

	# Simulation starts at 0 time
	t = 0
	for i in range(0, g.N_MIPS):
		# The next successive strip hit is Poisson. (What is the mean of the poisson though? something to do with average time for interaction?)
		# In ms/ps/ns?
		time_to_strip_hit = mt.return_rnd_Poisson(g.AVE_TIME_FOR_STRIP_HIT)

		######################################

		# Calculate charge deposited      ####
		charge_deposited_in_APV = mt.return_rnd_Landau(g.AVE_ENERGY_FOR_STRIP_HIT, g.SIGMA_ENERGY_FOR_STRIP_HIT):

		######################################

		######################################

		# Calculate amount of charge bled ####
		charge_in_APV = old_charge_in_APV + charge_deposited_in_APV
		new_charge_in_APV = bleed_off_charge(charge_in_APV, )

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
    main()