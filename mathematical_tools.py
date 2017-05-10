'''
Any useful mathematical tool should go here
'''
from __future__ import division

import math
from ROOT import gRandom, TRandom3
from rootpy.plotting import Hist

import numpy as np
import global_vars as g
import bunch_structures as bs
gRandom = TRandom3()
gRandom.SetSeed(0)
# Cache for quicker running
landau = gRandom.Landau
poisson = gRandom.Poisson
uniform = gRandom.Uniform
gaussian = gRandom.Gaus

# from memory_profiler import profile
# fp=open('memory_profiler.log','w+')

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

def return_rnd_Uniform(low=None, high=None):
	'''
	Returning a random unform number in range 0-1
	'''
	rnd_uni = -99
	if low and high:
		rnd_uni = uniform(low, high)
	else:
   		rnd_uni = uniform()
	return rnd_uni

def return_rnd_Landau(mu, sigma, scale=None):
	'''
	Returning a random landau number

	mu 		: location value (Not most probable value)
	sigma 	: scale parameter (Not the standard deviation as this is not defined)
	scale 	: if scale then apply silicon width to signal production. Mu and sigma
			  are predefined in this case for a 300 um chip, therefore 
			  charge = charge deposited * (Silicon Width / 300)
	'''
	# if using silicon width adjust mu by SiWidth/300
	if scale: 
		mu 		= mu * scale
		sigma 	= sigma * scale
   	rnd_ld = landau( mu, sigma )
	return rnd_ld

def return_charge_weighting(clusterStripInfo):
	'''
	clusterStripInfo contains the stripCluster Distribution (+ Normalised)
	Throw uniform number [0-1]
	Integral up to random number gives charge weighting from cluster to strip
	'''
	x = return_rnd_Uniform()
	interval = np.array([0.])
	quantile = np.array([x])
	clusterStripInfo['hist_stripClusterFraction_normed'].GetQuantiles( 1, interval, quantile) 
	return interval[0]

def return_strip_charge(clusterStripInfo):
	'''
	Return strip charge harge deposited based on Data
	'''
	x = return_rnd_Uniform()
	interval = np.array([0.])
	quantile = np.array([x])
	clusterStripInfo['hist_inputCharge_normed'].GetQuantiles( 1, interval, quantile) 
	return interval[0]

def eta_to_scale(eta):
	'''
	scale the path of the silicon chip by the entry angle
	'''
	# eta to theta
	theta = 2*np.arctan(np.exp(-eta))
	# length scales as 1/sin(theta)
	scale = 1/np.sin(theta)
	return scale

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

def mv_to_e(mV):
	'''
	Transform mv to e in the linear regime (low occupancy regimes)
	'''
	return

def amplifier_response(new_q, baseline_v, noise=True):
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
	max_response 		= 717
	new_v 				= 0
	signal_q 			= 0
	bkg_electronic 		= 0
	gain_v				= 0
	gain_vq				= 0

	if noise: bkg_electronic = return_rnd_Gaussian(0, g.AVERAGE_ELECTRONIC_NOISE)

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
			new_v = max_response - 83.5*math.exp(-(signal_q-max_linear_range)/75.5)
		new_v += bkg_electronic
		# add noise
		if baseline_v > 0 and new_q > 0: 
			gain_v = (new_v - baseline_v)

	elif baseline_v<max_response:
		baseline_q = max_linear_range - 75.5*math.log((max_response-baseline_v) / 83.5)
		signal_q = baseline_q + new_q
		# again put back into response equation
		new_v = max_response - 83.5*math.exp(-(signal_q-max_linear_range)/75.5)
		new_v += bkg_electronic

		if baseline_v > 0 and new_q > 0: 
			gain_v = (new_v - baseline_v)
	else:
		# No gain for any signal with the baseline currently above the maximum
		gain_v = 0
		# if baseline is higher than max_response just got to wait until it decays lower...
		new_v = max_response

	# Stop -ve signals from noise
	if new_v < 0: 
		new_v = 0
	# Even with electonic noise max output is 717mV
	if new_v > max_response:
		new_v = max_response

	if new_q > 0:
		gain_vq = gain_v / new_q
	return gain_vq, gain_v, new_v, signal_q, bkg_electronic

# @profile(stream=fp)
def amplifier_response2(new_q, prebleed_baseline, tau, bleed_type='voltage', noise=True, calculate_preAPVCharge=False ):
	'''
	Return the response of the amplifier
	Response is ~ linear until 139fC
	Max linear voltage ~ 633mV at q=139 fC
	Max voltage readout ~ 717mV for q>>139 fC

	V[mV] = 5.02*q - 0.00333*pow(q,2)    		q<139 fC
	V[mV] = 717 - 83.5*math.exp(-(q-139)/75.5) 	q>139 fC

	Response as given by Geoff Hall and Mark Raymond
	'''
	max_response 		= 729
	response_v 			= 0
	signal_q 			= 0
	bkg_electronic 		= 0
	gain_v				= 0
	gain_vq				= 0
	rate 				= 66.2
	preAPV_q 			= 0

	if calculate_preAPVCharge:
		if prebleed_baseline < max_response:
			preAPV_q = -rate*math.log((2*max_response)/(prebleed_baseline+max_response)-1)
		else: 
			preAPV_q = -99
		return preAPV_q

	# prebleed = max?
	# Bleed by either voltage or charge
	if 'voltage' in bleed_type:
		baseline_v, _ 	= bleed_off(prebleed_baseline, 0.025, tau)
		if baseline_v < max_response:
			baseline_q = -rate*math.log((2*max_response)/(baseline_v+max_response)-1)
		else:
			gain_v = 0
			gain_vq = 0
			response_v = max_response
			return gain_vq, gain_v, response_v, baseline_v, 0, 0

	elif 'charge' in bleed_type:   
		baseline_q, _ = bleed_off(prebleed_baseline, 0.025, tau)
		# Recalculate baseline vottage based on baseline charge
		baseline_v = 2*max_response / ( 1 + math.exp( -baseline_q/rate ) ) - max_response

	signal_q = new_q + baseline_q

	# Apply noise if needed
	if noise: bkg_electronic = return_rnd_Gaussian(0, g.AVERAGE_ELECTRONIC_NOISE)

	response_v = 2*max_response / ( 1 + math.exp( -signal_q/rate ) ) - max_response
	response_v += bkg_electronic

	if response_v < 0: response_v = 0
	if response_v > max_response: response_v = max_response

	# if baseline_v > 0:
	gain_v = (response_v - baseline_v)
	if new_q > 0:
			gain_vq = gain_v / new_q
	# else:
	# 	gain_v = 0
	# 	gain_vq = 0
	# 	response_v = max_response

	return gain_vq, gain_v, response_v, baseline_v, signal_q, bkg_electronic



# @profile(stream=fp)
def is_beam_present(clock_cycle, bunch_structure):
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

	if bunch_structure == 0:
		is_beam = bs.is_default_beam(clock_cycle)

	if bunch_structure == 1:
		is_beam = bs.is_Run278770_beam(clock_cycle)

	if bunch_structure == 2:
		is_beam = bs.is_Run278770_beam(clock_cycle)

	if bunch_structure == 3:
		is_beam = bs.is_Run276226_beam(clock_cycle)

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
	# 3.6 eV needed to create an electron hole pair in silicon
	# eV -> e 	: / 3.6
	charge_HIP = energy_HIP * math.pow(10,6) / 3.6
	# print "Charge on HIP : ", charge_HIP
	return charge_HIP


