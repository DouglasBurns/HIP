'''
Any global variables can go here
	import global_vars as g
	g.GLOBAL_VARIABLE

e.g. 
Number simulated events
Beam intensity etc
'''
# Number of iterations i.e. length of simulation
N_MIPS=10000

# ~20 collisions per bunch crossing

# Length of simulation
N_MAX_BUNCH_CROSSINGS=100000

# Order 100 charged particles
AVE_NUMBER_OF_PARTICLES_IN_BX=100 

# 
OCCUPANCY=0.02
N_BUNCHES=2808 

# bunches per beam
AVE_PROTON_IN_BUNCH=1.15e11
AVE_TIME_FOR_STRIP_HIT=100

# in terms of electron charge e
AVE_CHARGE_DEPOSITED=25000
SIGMA_CHARGE_DEPOSITED=3000

# May need to change to bleed off current for capacitor
# Then compute lifetime for bleedoff, tau
BLEEDOFF_LIFETIME=50 #(us)