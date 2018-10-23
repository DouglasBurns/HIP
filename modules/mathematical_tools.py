'''
Any useful mathematical tool should go here
'''
from __future__ import division

import math
from ROOT import gRandom, TRandom3
from rootpy.plotting import Hist

import numpy as np
from modules.global_vars import AVERAGE_ELECTRONIC_NOISE, AVERAGE_ELECTRONIC_NOISE_e
from modules.bunch_structures import is_default_beam, is_Run278770_beam, is_Run278345_beam, is_Run276226_beam
from memory_profiler import profile

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

# @profile
def return_rnd_number_from_dist(dist):
	'''
	dist contains the stripCluster Distribution (+ Normalised)
	Throw uniform number [0-1]
	Integral up to random number gives charge weighting from cluster to strip
	'''
	x = return_rnd_Uniform()
	interval = np.array([0.])
	quantile = np.array([x])
	dist.GetQuantiles( 1, interval, quantile) 
	if interval[0] < 500:
		interval[0] = 0
	return interval[0]

def return_strip_charge(dataChargeDist, n_samples=1):
	'''
	Return strip charge deposited based on Data
	'''
	q=0
	for n in range(0,n_samples):
		q+=return_rnd_number_from_dist(dataChargeDist)
	return q

def return_strip_charge_from_Poisson(dataChargeDist, occupancy, beam_present=True, add_noise=False, add_truncation=False):
	'''
	Return the charge based on Poisson
	Charge distribution should be cut to reduce effects from noise
	Skip Beam
	'''
	if not beam_present: return 0
	q = return_strip_charge(dataChargeDist, n_samples=return_rnd_Poisson(occupancy))
	if add_noise: q+=add_q_noise()
	if add_truncation: q=add_q_truncation(q)
	return q

def return_strip_charge_per_BX(dataChargeDist, beam_present=True):
	'''
	Return the charge based on noisy simulated strip charge. 
	Once every BX
	'''
	if not beam_present: return 0
	else: return return_strip_charge(dataChargeDist)

def return_strip_charge_from_Samples(dataChargeDist, n_samples=1, beam_present=True, add_noise=False, add_truncation=False):
	'''
	Return the charge by sampling noisy simulated strip charge
	'''
	if not beam_present: return 0
	q = return_strip_charge(dataChargeDist, n_samples=n_samples)
	if add_noise: q+=add_q_noise()
	if add_truncation: q = add_q_truncation(q)
	return q

def return_strip_charge_from_data_fit(fit):
	'''
	Return strip charge based on fit to data charge distribution
	'''
	q = fit.GetRandom()
	return q

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
	5.5 mV/fC at 0mV baseline
	'''
	return charge_transformation(mV/5.5, to_e=True)

def bleed_input(prebleed_baseline, tau, bleedby='Charge'):
	'''
	Bleed the current voltage/charge in/on the apv
	'''
	if bleedby == 'Charge':   
		baseline_q, _ = bleed_off(prebleed_baseline, 0.025, tau)
		baseline_v = response(baseline_q, q_to_v=True)

	if bleedby == 'Voltage':
		baseline_v, _ 	= bleed_off(prebleed_baseline, 0.025, tau)
		baseline_q = response(baseline_v, v_to_q=True)

	return baseline_v, baseline_q

def response(val, q_to_v=False, v_to_q=False):
	'''
	Return the response of the amplifier
	Response is ~ linear until 139fC
	Max linear voltage ~ 633mV at q=139 fC
	Max voltage readout ~ 717mV for q>>139 fC

	V[mV] = 5.02*q - 0.00333*pow(q,2)    		q<139 fC
	V[mV] = 717 - 83.5*math.exp(-(q-139)/75.5) 	q>139 fC

	Response as given by Geoff Hall and Mark Raymond
	'''
	if q_to_v == v_to_q:
		print "Set either q_to_v or v_to_q to True"
		return

	max_response 		= 729
	rate 				= 66.2

	if v_to_q:
		if val < max_response:
			return -rate*math.log((2*max_response)/(val+max_response)-1)
		else: 
			return max_response
	elif q_to_v:
		return 2*max_response / ( 1 + math.exp( -val/rate ) ) - max_response
	else:
		print "If you got here, I'm impressed"

# @profile(stream=fp)
def amplifier_response(baseline_q, new_q, noise=True ):
	'''
	Return the response of the amplifier
	Response is ~ linear until 139fC
	Max linear voltage ~ 633mV at q=139 fC
	Max voltage readout ~ 717mV for q>>139 fC

	V[mV] = 5.02*q - 0.00333*pow(q,2)    		q<139 fC
	V[mV] = 717 - 83.5*math.exp(-(q-139)/75.5) 	q>139 fC

	Response as given by Geoff Hall and Mark Raymond
	'''
	noise_q, gain_mV, gain_mV_fC = 0, 0, 0

	if noise: 
		noise_q = return_rnd_Gaussian(0, AVERAGE_ELECTRONIC_NOISE)

	signal_q = new_q + baseline_q + noise_q

	baseline_v = response(baseline_q, q_to_v=True)
	readout_v = response(signal_q, q_to_v=True)
	
	if readout_v < 0: 
		readout_v = 0

	if new_q > 0: 
		gain_mV = (readout_v - baseline_v)
		gain_mV_fC = gain_mV / new_q

	return readout_v, gain_mV, gain_mV_fC, signal_q, noise_q

def add_q_noise():
	'''
	Add some noise
	'''
	n = return_rnd_Gaussian(0, AVERAGE_ELECTRONIC_NOISE_e)
	return n

def add_q_truncation(q):
	'''
	Add Charge Truncation
	'''
	if q > 62500: q=62500
	return q

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
		is_beam = is_default_beam(clock_cycle)

	if bunch_structure == 1:
		is_beam = is_Run278770_beam(clock_cycle)

	if bunch_structure == 2:
		is_beam = is_Run278345_beam(clock_cycle)

	if bunch_structure == 3:
		is_beam = is_Run276226_beam(clock_cycle)

	if bunch_structure == -1:
		is_beam = is_on_beam(clock_cycle)

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


