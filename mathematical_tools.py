'''
Any useful mathematical tool should go here
'''
from __future__ import division

import math
from ROOT import gRandom, TRandom3
import global_vars as g
gRandom = TRandom3()
gRandom.SetSeed(0)
# Cache for quicker running
landau = gRandom.Landau
poisson = gRandom.Poisson
uniform = gRandom.Uniform
gaussian = gRandom.Gaus


def return_rnd_Poisson(mu):
	'''
	Returning a random poisson number
			lambda^{k} . e^{-lambda}
	Po() =	------------------------
					   k!

	k 		: events
	lambda 	: expected separation
	'''
   	rnd_po = poisson( mu )
	return rnd_po

def return_rnd_Gaussian(mu, sigma):
	'''
	Returning a random gaussian number

	mu 		: average
	sigma 	: dtandard deviation
	'''
   	rnd_gs = gaussian( mu, sigma )
	return rnd_gs

def return_rnd_Landau(mu, sigma):
	'''
	Returning a random landau number

	mu 		: location value (Not most probable value)
	sigma 	: scale parameter (Not the standard deviation as this is not defined)
	'''
   	rnd_ld = landau( mu, sigma )
	return rnd_ld

def bleed_off(v0, t, tau):
	'''
	v = voltage after bleed off
	v0 = voltage in APV
	t = time since last MIP
	tau = bleedoff lifetime

			   -t/tau
	v = v0 . e

	V ~ Q ~ I
	'''
	v = v0 * math.exp(-t/tau)
	return v, v0-v

def charge_transformation(charge_deposited, to_fC=False, to_e=False):
	'''
	e = 1.602e-4 fC
	Transform a given charge
		e 	->	fC
		fC 	->	e
	'''
	# set default
	if charge_deposited == 0: return 0
	e_charge_in_fC = 1.602e-4
	if not to_fC and not to_e: to_fC = True

	if to_fC: return charge_deposited*e_charge_in_fC
	elif to_e: return charge_deposited/e_charge_in_fC
	else: return 0

def time_transformation(time, to_clock_cycle=False, to_us=False):
	'''
	1bx = 25 ns = 0.025us
	Transform a given time
		bx 	->	us
		us 	->	bx
	'''
	time_between_bx = 0.025 # 25ns
	# set default
	if not to_clock_cycle and not to_us: to_us = True

	if to_us: return time*time_between_bx
	elif to_clock_cycle: return time/time_between_bx
	else: return 0

def amplifier_response(new_q, baseline_v):
	'''
	Return the response of the amplifier
	Response is ~ linear until 139fC
	Max linear voltage ~ 633mV at q=139 fC
	Max voltage readout ~ 717mV for q>>139 fC

	V[mV] = 5.02*q - 0.00333*pow(q,2)    		q<139 fC
	V[mV] = 717 - 83.5*math.exp(-(q-139)/75.5) 	q>139 fC

	Response as given by Geoff Hall and Mark Raymond
	'''
	max_linear_range 	= 139
	new_v 				= 0
	signal_q 			= 0
	bkg_electronic 		= 0
	# Finding the baseline charge in chip in fC
	# Solution to the response equation
	if baseline_v < 633:
		baseline_q = (-5.02+math.sqrt(pow(5.02,2)-4*0.00333*baseline_v)) / (-2*0.00333)
		signal_q = baseline_q + new_q
		# Add electronic noise

		# Now put back into response equation
		# linear
		# This can be -ve for very verylarge q
		new_v = 5.02*signal_q - 0.00333*(pow(signal_q,2))

		# nonlinear
		if signal_q > 139:
			new_v = 717 - 83.5*math.exp(-(signal_q-max_linear_range)/75.5)

		bkg_electronic = return_rnd_Gaussian(0, g.AVERAGE_ELECTRONIC_NOISE)
		new_v += bkg_electronic
		# add noise
		gain_v = new_v - baseline_v

	elif baseline_v<717:
		baseline_q = max_linear_range - 75.5*math.log((717-baseline_v) / 83.5)
		signal_q = baseline_q + new_q
		# again put back into response equation
		new_v = 717 - 83.5*math.exp(-(signal_q-max_linear_range)/75.5)
		bkg_electronic = return_rnd_Gaussian(0, g.AVERAGE_ELECTRONIC_NOISE)
		new_v += bkg_electronic

		gain_v = new_v - baseline_v
	else:
		# No gain for any signal with the baseline currently above the maximum
		gain_v = 0
		# if baseline is higher than 717 just got to wait until it decays lower...
		new_v = 717

	# Stop -ve signals
	if new_v < 0: 
		gain_v = 0
		new_v = 0
	return gain_v, new_v, signal_q, bkg_electronic

def is_beam_present(clock_cycle):
	'''
	Takes the current clock cycle relative to the first bunch

	#LHC beam structure
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] + 
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +(72b + 8e) +31 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] + 
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +(72b + 8e) +31 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] + 
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +(72b + 8e) +31 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] + 
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] +
	[(72b + 8e) +(72b +8e) +(72b+8e) +30 e] + 81e
	Total = 3564 bunches and empties
	'''
	is_beam = True
	# Cycle using the modulus, +1 as LHC bunch scheming starts at one, our loop starts at 0
	# modulo 17 % 3 = 2 (goes in 5 times (17 - 15) = 2 left)
	mod_clock_cycle = (clock_cycle % 3564)

	# Check if current clock cycle has a colliding bunch
	if( (mod_clock_cycle > 72) and (mod_clock_cycle <= 80) ) : is_beam =  False
	if( (mod_clock_cycle > 152) and (mod_clock_cycle <= 160) ) : is_beam = False
	if( (mod_clock_cycle > 232) and (mod_clock_cycle <= 270) ) : is_beam = False
	if( (mod_clock_cycle > 342) and (mod_clock_cycle <= 350) ) : is_beam = False
	if( (mod_clock_cycle > 422) and (mod_clock_cycle <= 430) ) : is_beam = False
	if( (mod_clock_cycle > 502) and (mod_clock_cycle <= 540) ) : is_beam = False
	if( (mod_clock_cycle > 612) and (mod_clock_cycle <= 620) ) : is_beam = False
	if( (mod_clock_cycle > 692) and (mod_clock_cycle <= 700) ) : is_beam = False
	if( (mod_clock_cycle > 772) and (mod_clock_cycle <= 780) ) : is_beam = False
	if( (mod_clock_cycle > 852) and (mod_clock_cycle <= 891) ) : is_beam = False
	if( (mod_clock_cycle > 963) and (mod_clock_cycle <= 971) ) : is_beam = False
	if( (mod_clock_cycle > 1043) and (mod_clock_cycle <= 1051) ) : is_beam = False
	if( (mod_clock_cycle > 1123) and (mod_clock_cycle <= 1161) ) : is_beam = False
	if( (mod_clock_cycle > 1233) and (mod_clock_cycle <= 1241) ) : is_beam = False
	if( (mod_clock_cycle > 1313) and (mod_clock_cycle <= 1321) ) : is_beam = False
	if( (mod_clock_cycle > 1393) and (mod_clock_cycle <= 1431) ) : is_beam = False
	if( (mod_clock_cycle > 1503) and (mod_clock_cycle <= 1511) ) : is_beam = False
	if( (mod_clock_cycle > 1583) and (mod_clock_cycle <= 1591) ) : is_beam = False
	if( (mod_clock_cycle > 1663) and (mod_clock_cycle <= 1671) ) : is_beam = False
	if( (mod_clock_cycle > 1742) and (mod_clock_cycle <= 1782) ) : is_beam = False
	if( (mod_clock_cycle > 1854) and (mod_clock_cycle <= 1862) ) : is_beam = False
	if( (mod_clock_cycle > 1934) and (mod_clock_cycle <= 1942) ) : is_beam = False
	if( (mod_clock_cycle > 2014) and (mod_clock_cycle <= 2052) ) : is_beam = False
	if( (mod_clock_cycle > 2124) and (mod_clock_cycle <= 2132) ) : is_beam = False
	if( (mod_clock_cycle > 2204) and (mod_clock_cycle <= 2212) ) : is_beam = False
	if( (mod_clock_cycle > 2284) and (mod_clock_cycle <= 2322) ) : is_beam = False
	if( (mod_clock_cycle > 2394) and (mod_clock_cycle <= 2402) ) : is_beam = False
	if( (mod_clock_cycle > 2474) and (mod_clock_cycle <= 2482) ) : is_beam = False
	if( (mod_clock_cycle > 2554) and (mod_clock_cycle <= 2562) ) : is_beam = False
	if( (mod_clock_cycle > 2634) and (mod_clock_cycle <= 2673) ) : is_beam = False
	if( (mod_clock_cycle > 2745) and (mod_clock_cycle <= 2753) ) : is_beam = False
	if( (mod_clock_cycle > 2825) and (mod_clock_cycle <= 2833) ) : is_beam = False
	if( (mod_clock_cycle > 2905) and (mod_clock_cycle <= 2943) ) : is_beam = False
	if( (mod_clock_cycle > 3015) and (mod_clock_cycle <= 3023) ) : is_beam = False
	if( (mod_clock_cycle > 3095) and (mod_clock_cycle <= 3103) ) : is_beam = False
	if( (mod_clock_cycle > 3175) and (mod_clock_cycle <= 3213) ) : is_beam = False
	if( (mod_clock_cycle > 3285) and (mod_clock_cycle <= 3293) ) : is_beam = False
	if( (mod_clock_cycle > 3365) and (mod_clock_cycle <= 3373) ) : is_beam = False
	if( (mod_clock_cycle > 3445) and (mod_clock_cycle <= 3564) ) : is_beam = False
	# if( mod_clock_cycle > 800 ) : is_beam = False

	return is_beam

def tracker_hits(occupancy, particles_in_bx, ave_particles_in_bx ):
	'''
	Return number of hits on a strip in the tracker

								 N_p
	P(Strip hit) = Occupancy * --------
								<N_p>

	N_p   	  	 = Number of particles produced in bunch crossing
	<N_p> 		 = Average number of particles produced in bunch crossing

				  		 N_p
				 = SUM -------
				 		 N_bx

	N_bx 		 = Number of bunch crossings

	Occupancy 	 = P(strip has charge deposited per bunch crossing)
				   f(N_bx, d_pv)
	d_pv 		 = Distance to the primary vertex

	N_particles produced in bx ~ N_particles in bunch 1 and 2 

	'''
	# Not hit very often...
	p_strip_hit = occupancy * particles_in_bx / ave_particles_in_bx

	n_tracker_hits = return_rnd_Poisson( p_strip_hit )
	return n_tracker_hits

def is_HIP(HIPocc):
	'''
	Is a MIP hit a HIP?
	'''
	if (uniform(0,1) < HIPocc):
		return True
	else:
		return False

def return_HIP_charge():
	'''
	Assign energy of 0.1-20 MeV randomly
	'''
	energy_HIP = uniform(0.1,20)

	# MeV -> eV : * math.pow(10,6)
	# eV -> e 	: / 3.6 ?????
	charge_HIP = energy_HIP * math.pow(10,6) / 3.6
	# print "Charge on HIP : ", charge_HIP
	return charge_HIP


