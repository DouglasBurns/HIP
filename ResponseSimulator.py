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

# import my scripts
import global_vars as g
import mathematical_tools as mt
import pandas_utils as pu

from read_charge_inputs import charge_inputs

from plots_test import run_tests
from plots_profile import run_profiles
from plots_distribution import run_distributions
from plots_landau import run_landaus


from argparse import ArgumentParser

def arg_parser():
	parser = ArgumentParser(description='Calculates the charge on a APV')
	parser.add_argument( "-d", "--debug", 
		dest = "debug",
		action = "store_true", 
		help = "For debugging" 
	)
	parser.add_argument( "-t", "--tests", 
		dest = "tests",
		action = "store_true", 
		help = "For debugging" 
	)
	parser.add_argument( "-n", "--noise", 
		dest = "noise",
		action = "store_true", 
		help = "Add noise to simulation" 
	)
	parser.add_argument( "-T", "--tau",
		dest = "tau",
		default = None, 
		type = float,
		help = "tau parameter" 
	)
	parser.add_argument( "-O", "--occ", 
		dest = "occ",
		default = None, 
		type = float,
		help = "occupancy parameter" 
	)
	parser.add_argument( "-S", "--width",
		dest = "SiWith",
		default = None, 
		type = float,
		help = "Width of silicon chip" 
	)
	parser.add_argument( "-B",  "--beam",
		dest = "beam",
		default = 3, 
		type = int,
		help = "Beam structure. 0 for default, 1 for Run 278770, 2 for 278345, 3 for 276226" 
	)
	parser.add_argument( "-N", "--mips",
		dest = "nmips",
		default = None, 
		type = float,
		help = "Number of MIPS in sim" 
	)
	parser.add_argument( "-b", "--bleedtype",
		dest = "bleedBy",
		default = 'voltage', 
		type = str,
		help = "options: [charge/voltage] default voltage" 
	)
	parser.add_argument( "-R", "--tracker_region",
		dest = "tracker_region",
		default = None, 
		type = str,
		help = "Specific part of the tracker" 
	)
	args = parser.parse_args()
	return args


def main(args):
	'''
	Iterate over time (how long?)
	See if hit in strip
	See what charge is
	See how much charge has bled off in the readout capacitor
	'''

	DEBUG 			= args.debug
	TESTS 			= args.tests
	NOISE 			= args.noise
	TAU   			= args.tau
	OCC   			= args.occ
	WIDTH 			= args.SiWith
	BEAM  			= args.beam
	NMIP  			= args.nmips
	BLEED 			= args.bleedBy
	REGION			= args.tracker_region
	REGION_DETAILS 	= g.tracker_deets

	# Testing Distributions
	if TESTS: 
		print "Running Tests"
		run_tests(args)
		return

	########################################################################################################################
	### mV to e @ Baseline = 0mV, 1MIP = 3.75fC = 23500e
	########################################################################################################################
	gain_vq, gain_v, _, _, _, _ = mt.amplifier_response2(3.75, 0, TAU, noise=False)

	########################################################################################################################
	### Initialisations
	########################################################################################################################
	# Stored every bunch crossing
	d_full_variables 							= {}
	d_full_variables['bunchCrossing'] 			= []
	d_full_variables['isBeam'] 					= []
	d_full_variables['timeLastMIP_bx'] 			= []

	d_full_variables['V_baseline_mv'] 			= []
	d_full_variables['V_signal_mv'] 			= []
	d_full_variables['V_gain_mv']				= []
	d_full_variables['V_noise_mv'] 				= []

	d_full_variables['q_baseline_fC'] 			= []
	d_full_variables['q_Deposited_e'] 			= []
	d_full_variables['q_Deposited_fC']	 		= []
	d_full_variables['q_HIP_e'] 				= []

	d_full_variables['n_MIP_total'] 			= []
	d_full_variables['n_MIP_bx'] 				= []
	d_full_variables['n_HIP_total'] 			= []
	d_full_variables['n_HIP_bx'] 				= []

	# Stored every MIP
	d_mip_variables 							= {}
	d_mip_variables["V_diff_mv"]				= []
	d_mip_variables["V_gain_mv"]				= []
	d_mip_variables["V_baseline_mv"]			= []
	d_mip_variables['q_Deposited_fC']			= []
	d_mip_variables['q_Deposited_e']			= []
	d_mip_variables['q_ClusterDeposited_e']		= []
	d_mip_variables['q_Read_e']					= []
	d_mip_variables['q_Weight_e']				= []
	d_mip_variables['track_eta']				= []
	d_mip_variables['track_length']				= []

	HIPInBX										= []

	baseline 									= 0
	baseline_mV 								= 0
	baseline_fC 								= 0
	time_since_last_MIP 						= 0
	bx 											= 0
	n_MIP_total 								= 0
	n_MIP_counted								= 0
	n_HIP_total									= 0

	# Setting defaults if not specified by command line
	if not OCC: 	OCC 	= g.OCCUPANCY
	if not TAU: 	TAU 	= g.BLEEDOFF_LIFETIME
	if not WIDTH: 	WIDTH 	= g.SILICON_THICKNESS
	if not NMIP: 	NMIP 	= g.N_MIPS
	if REGION: 		
		OCC 	= REGION_DETAILS[REGION]['Occ_Data']
		WIDTH 	= REGION_DETAILS[REGION]['SiWidth']

	if REGION:
		data_charge_inputs = charge_inputs(REGION)


	########################################################################################################################
	### START OF SIMULATION
	########################################################################################################################
	while (n_MIP_total < NMIP):
		bx += 1

		n_MIP_bx, n_HIP_bx						= 0, 0
		charge_MIP_e, charge_HIP_e				= 0, 0
		charge_deposited_e, charge_deposited_fC	= 0, 0
		cluster_charge_deposited_e 				= 0
		electronic_noise_mV						= 0

		########################################################################################################################
		### Calculate number of MIPS in bx (if bx present)
		########################################################################################################################
		if mt.is_beam_present(bx, BEAM):
			n_MIP_bx 			= mt.return_rnd_Poisson(OCC)
			n_MIP_total 		+= n_MIP_bx
			
		########################################################################################################################
		### Calculate charge (e) of MIPS (if MIPS present)
		########################################################################################################################
		if n_MIP_bx > 0:
			for i in range(0, n_MIP_bx):

				# restrict eta dependence [-1, 1] (Uniform)
				eta = mt.return_rnd_Uniform(low = -1, high = 1 )
				length_scale = mt.eta_to_scale(eta)
				silicon_pathlength = length_scale * WIDTH/300

				d_mip_variables['track_eta'].append(eta)
				d_mip_variables['track_length'].append(length_scale*WIDTH)

				# Is the MIP a HIP
				isHIP = mt.is_HIP(g.HIP_OCCUPANCY)
				if isHIP:
					# Where are the HIPs
					HIPInBX.append(bx)
					n_HIP_bx 						+= 1
					n_HIP_total 					+= 1
					charge_HIP_e 					= mt.return_HIP_charge()
					cluster_charge_deposited_e 		+= charge_HIP_e

				else:
					# this depends on the thickness of the chip...
					charge_MIP_e 		= mt.return_rnd_Landau(g.AVE_CHARGE_DEPOSITED, g.SIGMA_CHARGE_DEPOSITED, scale=silicon_pathlength)
					cluster_charge_deposited_e 	+= charge_MIP_e


			charge_deposited_e = cluster_charge_deposited_e
			if REGION:
				stripClusterFraction 	= mt.return_charge_weighting(data_charge_inputs)
				charge_deposited_e 		= cluster_charge_deposited_e * stripClusterFraction

			if DEBUG:
				print "-"*50
				print "{} charged particles found in bunch crossing {}".format( n_MIP_bx, bx )
				print "{} charged particles were HIPs".format( n_HIP_bx )
				print "- "*25
				print "Total Charge deposited {}e".format(charge_deposited_e)

		########################################################################################################################
		### Calculate charge (fc) of MIPS
		########################################################################################################################
		charge_deposited_fC = mt.charge_transformation(charge_deposited_e, to_fC=True)

		########################################################################################################################
		### New Response (mV) (charge in fC, voltage in mV)
		########################################################################################################################			
		if 'charge' in BLEED: 	baseline = baseline_fC
		else: 					baseline = baseline_mV

		signal_gain_vq, signal_gain_v, signal_response, current_baseline_mV, total_charge_fC, electronic_noise_mV = mt.amplifier_response2(
			charge_deposited_fC, 
			baseline, 
			TAU, 
			noise=NOISE, 
			bleed_type=BLEED
		)
		
		if signal_gain_v > g.EFFECTIVE_THRESHOLD:
			n_MIP_counted += 1

		if DEBUG:
			print "Baseline Voltage {}mV".format(baseline_mV)
			print "Baseline Charge {}fC".format(baseline_fC)
			print "Signal response {}mV".format(signal_response)
			print "Signal gain {}mV".format(signal_gain_v)
			print "Signal gain {}mV/fC".format(signal_gain_vq)
			print "- "*30
			raw_input("Press ENTER to continue.")


		########################################################################################################################
		### Store Parameters for all BX (Useful for projections)
		########################################################################################################################
		d_full_variables['bunchCrossing'].append(bx)
		d_full_variables['isBeam'].append(mt.is_beam_present(bx, BEAM))
		d_full_variables['timeLastMIP_bx'].append(time_since_last_MIP)

		d_full_variables['V_baseline_mv'].append(current_baseline_mV)
		d_full_variables['V_signal_mv'].append(signal_response)
		d_full_variables['V_gain_mv'].append(signal_gain_vq)
		d_full_variables['V_noise_mv'].append(electronic_noise_mV)

		d_full_variables['q_Deposited_e'].append(charge_deposited_e)
		d_full_variables['q_Deposited_fC'].append(charge_deposited_fC)
		d_full_variables['q_HIP_e'].append(charge_HIP_e)
		d_full_variables['q_baseline_fC'].append(total_charge_fC)

		d_full_variables['n_MIP_bx'].append(n_MIP_bx)
		d_full_variables['n_HIP_bx'].append(n_HIP_bx)
		d_full_variables['n_MIP_total'].append(n_MIP_total)
		d_full_variables['n_HIP_total'].append(n_HIP_total)

		########################################################################################################################
		### Store Parameters when a MIP Occurs (Useful for distributions)
		########################################################################################################################		
		if n_MIP_bx > 0: 
			d_mip_variables["V_baseline_mv"].append(current_baseline_mV)
			d_mip_variables["V_diff_mv"].append(signal_gain_v)
			d_mip_variables['V_gain_mv'].append(signal_gain_vq)

			d_mip_variables['q_Deposited_fC'].append(charge_deposited_fC)
			d_mip_variables['q_Deposited_e'].append(charge_deposited_e)
			d_mip_variables['q_ClusterDeposited_e'].append(cluster_charge_deposited_e)
			d_mip_variables['q_Read_e'].append(signal_gain_v*g.AVE_CHARGE_DEPOSITED/gain_v)
			d_mip_variables['q_Weight_e'].append(stripClusterFraction)

		########################################################################################################################
		### Reintitialise for next MIP
		########################################################################################################################
		baseline_mV = signal_response
		baseline_fC = total_charge_fC
		if n_MIP_bx > 0: 
			time_since_last_MIP = 0
		else:
			time_since_last_MIP += 1

	########################################################################################################################
	### END OF SIMULATION
	########################################################################################################################


	########################################################################################################################
	########################################################################################################################
	### CREATE DATAFRAME, OUTPUT FOLDER (AND WRITE DF TO FILE)
	########################################################################################################################
	########################################################################################################################
	full_simulation = pu.dict_to_df(d_full_variables)
	print full_simulation
	print "The hit efficiency (fraction tracks above {}mV threshold) is {}".format(g.EFFECTIVE_THRESHOLD, n_MIP_counted/n_MIP_total)

	base_path = 'plots/'

	if   BEAM == 0 : 	BS = 'default'
	elif BEAM == 1 : 	BS = '278770'
	elif BEAM == 2 : 	BS = '278345'
	elif BEAM == 3 : 	BS = '276226'

	bs_dir		= 'Bunch_Structure_'+BS+'/'

	if REGION: 	tk_dir = REGION+'/'
	else:		tk_dir = ''	

	tau_dir 	= 'Tau_'+str(int(TAU))+'/'
	occ_dir 	= 'Occ_'+str(OCC).replace('.', '_')+'/'

	if not REGION:
		if WIDTH == 300: 	chip_dir = 'TIB/'
		elif WIDTH == 500: 	chip_dir = 'TOB/'
		else: 				chip_dir = ''
	else:					chip_dir = ''

	bleedtype_dir = BLEED+'_bleeding/'
	folder_path = base_path + tk_dir + bs_dir + tau_dir + occ_dir + chip_dir + bleedtype_dir

	pu.make_folder_if_not_exists(folder_path)
	title = "$\\tau = $ {}, occ = {}, beam structure = {}, bleed by {}, {}".format(TAU, OCC, BS, BLEED, chip_dir.replace('/',''))
	# pu.df_to_file(folder_path, 'DF.txt', full_simulation)


	########################################################################################################################
	########################################################################################################################
	### PLOTTING
	########################################################################################################################
	########################################################################################################################
	
	########################################################################################################################
	### SIMULATION DATA COMPARISON
	########################################################################################################################
	if REGION:
		print "Comparing charge distribution for ", REGION
		title_comp = "$\\tau = $ {}, occ = {}, bleed by {}, {}".format(TAU, OCC, BLEED, REGION)
		run_landaus(title_comp, folder_path, d_mip_variables, data_charge_inputs)

	########################################################################################################################
	### PROJECTIONS
	########################################################################################################################
	run_profiles(title, folder_path, full_simulation, HIPInBX)

	########################################################################################################################
	### DISTRIBUTIONS
	########################################################################################################################
	run_distributions(title, folder_path, d_mip_variables, full_simulation, NOISE)

if __name__ == "__main__":
	args = arg_parser()
	main(args)