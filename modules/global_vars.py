'''
Any global variables can go here
	import global_vars as g
	g.GLOBAL_VARIABLE

e.g. 
Number simulated events
Beam intensity etc
'''
# Number of iterations i.e. length of simulation
N_BX			= 1000
# N_BX			= 10000000
TESTING 		= False
CHARGE_CUTOFF 	= 10000

# Which input strip charge distribution shall we use?
# True = SCD > 10 000e
# False = Full SCD
SCD_CUTS = [
	True,
	False
]

# Which strip tracker layer is being used?
# Tracker Inner Barrel 1 -> Tracker Outer Barrel 6
REGIONS = [
	'TIB_1',
	# 'TIB_2',
	# 'TIB_3',
	# 'TIB_4',
	# 'TOB_1',
	# 'TOB_2',
	# 'TOB_3',
	# 'TOB_4',
	# 'TOB_5',
	# 'TOB_6',
]

# How fast does charge bleed away? (us)
# Proxy for VFP parameter
TAUS = [
	5,
	25,
	65,
]

# Which beam filling scheme is being used?
# Find in bunch_structures.py
BEAMS = [
	# 0, # default
	# 1, # Run 278770
	# 2, # Run 278345
	3, # Run 276226
]

# How is the charge sensitive capacitor bled?
# By charge 
# 	- No upper limit on charge deposited
# 	- Assumed to be correct method
# By voltage 
# 	- Upper limit imposed by maximum response of APV
BLEEDTYPES = [
	'Charge',
	# 'Voltage',
]

# Dictionary of details
# 	- Occ = Occupancy as taken from paper.
# 	- Occ_Data = Occupancy as measured from data (Emyr provided Run ???)
# 	- Occ_LowOcc_Data = Occupancy as measured from low occupancy data (Emyr provided Run ???)
# 	- Occ_HighOcc_VFPNoFix_Data = Occupancy as measured from high occupancy data before the VFP fix (Emyr provided Run 278770)
# 	- Occ_HighOcc_VFPFix_Data = Occupancy as measured from high occupancy data after the VFP fix (Emyr provided Run 278808)
# 	- Occ_Sim = Occupancy as measured from simulation (Emyr provided Simulation)
# 	- SiWidth = Width of silicon
# 	- nStrips = Total strips in tracker layer
# 	- nStrips_eta_lt1 = Total strips in tracker layer with pseudorapidity less than 1
REGION_DETAILS = {
	'TIB_1' : {
		'Occ' 						: 0.028, 
		'Occ_Data' 					: 0.028, 
		'Occ_LowOcc_Data' 			: 0.000367257, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0297871, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.0197638, 
		'Occ_Sim' 					: 0.000828637, 
		'SiWidth' 					: 300, 
		'nStrips' 					: 475392,
		'nStrips_eta_lt1' 			: 475392 * 0.42, 
	},
	'TIB_2' : {
		'Occ' 						: 0.018, 
		'Occ_Data' 					: 0.020, 
		'Occ_LowOcc_Data' 			: 0.000232327, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0213905, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.0130307, 
		'Occ_Sim' 					: 0.000560352, 
		'SiWidth' 					: 300, 
		'nStrips' 					: 626688,
		'nStrips_eta_lt1' 			: 626688 * 0.63, 
	},
	'TIB_3' : {
		'Occ' 						: 0.017, 
		'Occ_Data' 					: 0.019, 
		'Occ_LowOcc_Data' 			: 0.000186896, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0191855, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.0112444, 
		'Occ_Sim' 					: 0.000450277, 
		'SiWidth' 					: 300, 
		'nStrips' 					: 246784,
		'nStrips_eta_lt1' 			: 246784 * 0.7, 
	},
	'TIB_4' : {
		'Occ' 						: 0.013, 
		'Occ_Data' 					: 0.015, 
		'Occ_LowOcc_Data' 			: 0.000138794, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0141037, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.00814419, 
		'Occ_Sim' 					: 0.000313819, 
		'SiWidth' 					: 300, 
		'nStrips' 					: 297984,
		'nStrips_eta_lt1' 			: 297984 * 0.93, 
	},
	'TOB_1' : {
		'Occ' 						: 0.019, 
		'Occ_Data' 					: 0.026, 
		'Occ_LowOcc_Data' 			: 0.000296125, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.025178, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.0179228, 
		'Occ_Sim' 					: 0.000671616, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 513536,
		'nStrips_eta_lt1' 			: 513536 * 0.63, 
	},
	'TOB_2' : {
		'Occ' 						: 0.014, 
		'Occ_Data' 					: 0.023, 
		'Occ_LowOcc_Data' 			: 0.000217645, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0211739, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.01345, 
		'Occ_Sim' 					: 0.000489276, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 580352,
		'nStrips_eta_lt1' 			: 580352 * 0.75, 
	},
	'TOB_3' : {
		'Occ' 						: 0.011, 
		'Occ_Data' 					: 0.019, 
		'Occ_LowOcc_Data' 			: 0.000149476, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.0164513, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.00965363, 
		'Occ_Sim' 					: 0.000338817, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 318464,
		'nStrips_eta_lt1' 			: 318464 * 0.83, 
	},
	'TOB_4' : {
		'Occ' 						: 0.008, 
		'Occ_Data'					: 0.015, 
		'Occ_LowOcc_Data'			: 0.000122572, 
		'Occ_HighOcc_VFPNoFix_Data'	: 0.0125723, 
		'Occ_HighOcc_VFPFix_Data'	: 0.00731446, 
		'Occ_Sim'					: 0.000265365, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 344064,
		'nStrips_eta_lt1' 			: 344064 * 0.93, 
	},
	'TOB_5' : {
		'Occ' 						: 0.005, 
		'Occ_Data' 					: 0.009, 
		'Occ_LowOcc_Data' 			: 0.0000766174, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.00741836, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.00450217, 
		'Occ_Sim' 					: 0.000165749, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 597760,
		'nStrips_eta_lt1' 			: 597760 * 1, 
	},
	'TOB_6' : {
		'Occ' 						: 0.006, 
		'Occ_Data' 					: 0.006, 
		'Occ_LowOcc_Data' 			: 0.0000550702, 
		'Occ_HighOcc_VFPNoFix_Data' : 0.00534622, 
		'Occ_HighOcc_VFPFix_Data' 	: 0.00327399, 
		'Occ_Sim' 					: 0.000121633, 
		'SiWidth' 					: 500, 
		'nStrips' 					: 676352,
		'nStrips_eta_lt1' 			: 676352 * 1, 
	},
}

NOISE = False
CHARGE_FROM_DATA = True

# Adding in Noise to simulation
# 	- Currently set to off
# sigma of 1.2mV in electronics (1500e)
AVERAGE_ELECTRONIC_NOISE			= 1.2
AVERAGE_ELECTRONIC_NOISE_e			= 1500


### Deprecated
# 5 times noise? (mV)
# EFFECTIVE_THRESHOLD					= 46
EFFECTIVE_THRESHOLD					= 5*AVERAGE_ELECTRONIC_NOISE

# TODO DEPRECATED
HIP_OCCUPANCY						= 0.0015 # (*OCCUPANCY)
N_BUNCHES							= 2808 

# in terms of electron charge e (used to be 25000) 21500 good fit
AVE_CHARGE_DEPOSITED				= 23500
SIGMA_CHARGE_DEPOSITED				= 3000

# N to go from OCC of min bias charge distribution (from data) to high OCC run.
EFFECTIVE_OCCUPANCY_RATIO 			= 10
