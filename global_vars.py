'''
Any global variables can go here
	import global_vars as g
	g.GLOBAL_VARIABLE

e.g. 
Number simulated events
Beam intensity etc
'''
# Number of iterations i.e. length of simulation
N_MIPS								= 10000

# ~20 collisions per bunch crossing

# Length of simulation
N_MAX_BUNCH_CROSSINGS				= 100000

# Order 100 charged particles
AVE_NUMBER_OF_PARTICLES_IN_BX		= 2000

# 
OCCUPANCY							= 0.02
HIP_OCCUPANCY						= 0.0015 # (*OCCUPANCY)
N_BUNCHES							= 2808 

# bunches per beam
AVE_PROTON_IN_BUNCH					= 1.15e11
AVE_TIME_FOR_STRIP_HIT				= 100

# in terms of electron charge e (used to be 25000) 21500 good fit
AVE_CHARGE_DEPOSITED				= 23500
SIGMA_CHARGE_DEPOSITED				= 3000

# May need to change to bleed off current for capacitor
# Then compute lifetime for bleedoff, tau
BLEEDOFF_LIFETIME 					= 5 #(us)

# sigma of 1.2mV in electronics (1500e)
AVERAGE_ELECTRONIC_NOISE			= 1.2

SILICON_THICKNESS					= 500

# 5 times noise? (mV)
# EFFECTIVE_THRESHOLD					= 46
EFFECTIVE_THRESHOLD					= 5*AVERAGE_ELECTRONIC_NOISE

tracker_deets = {
	'TIB1' : {'Occ' : 0.028,	'Occ_Data' : 0.028, 	'SiWidth' : 300 },
	'TIB2' : {'Occ' : 0.018,	'Occ_Data' : 0.020, 	'SiWidth' : 300 },
	'TIB3' : {'Occ' : 0.017,	'Occ_Data' : 0.019, 	'SiWidth' : 300 },
	'TIB4' : {'Occ' : 0.013,	'Occ_Data' : 0.015, 	'SiWidth' : 300 },
	# 'TOB1' : {'Occ' : 0.019,	'Occ_Data' : 0.050, 	'SiWidth' : 500 },
	'TOB1' : {'Occ' : 0.019,	'Occ_Data' : 0.026, 	'SiWidth' : 500 },


	'TOB2' : {'Occ' : 0.014,	'Occ_Data' : 0.023, 	'SiWidth' : 500 },
	'TOB3' : {'Occ' : 0.011,	'Occ_Data' : 0.019, 	'SiWidth' : 500 },
	'TOB4' : {'Occ' : 0.008,	'Occ_Data' : 0.015, 	'SiWidth' : 500 },
	'TOB5' : {'Occ' : 0.005,	'Occ_Data' : 0.009, 	'SiWidth' : 500 },
	'TOB6' : {'Occ' : 0.006,	'Occ_Data' : 0.006, 	'SiWidth' : 500 },
}
