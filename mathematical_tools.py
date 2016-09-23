'''
Any useful mathematical tool should go here
'''
from __future__ import division

import math
from ROOT import gRandom, TRandom3
gRandom = TRandom3()
gRandom.SetSeed(1)
# Cache for quicker running
landau = gRandom.Landau
poisson = gRandom.Poisson


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


def return_rnd_Landau(mu, sigma):
	'''
	Returning a random landau number

	mu 		: location value (Not most probable value)
	sigma 	: scale parameter (Not the standard deviation as this is not defined)
	'''
   	rnd_ld = landau( mu, sigma )
	return rnd_ld

def bleed_off_charge(q0, t, tau):
	'''
	q = charge after bleed off
	q0 = charge in APV
	t = time since last collision
	tau = bleedoff lifetime

			   -t/tau
	q = q0 . e

	V ~ Q ~ I
	'''
	q = q0 * math.exp(-t/tau)
	return q, q0-q



def amplifier_response(new_q, baseline_v):
	'''
	Return the response of the amplifier
	Response is ~ linear until 139fC
	Baseline voltage ~ 633mV for q=139 fC
	Max voltage readout ~ 717mV for q=139 fC

	V[mV] = 5.02*q - 0.00333*pow(q,2)    		q<139 fC
	V[mV] = 717 - 83.5*math.exp(-(q-139)/75.5) 	q>139 fC

	Response as given by Geoff Hall and Mark Raymond
	'''
	max_linear_range = 139

	# Finding the baseline charge in chip in fC
	# Solution to the response equation
	if baseline_v < 633:
		baseline_q = (-5.02+math.sqrt(pow(5.02,2)-4*0.00333*baseline_v)) / (-2*0.00333)
		signal_q = baseline_q + new_q
		# Now put back into response equation
		# linear
		new_v = 5.02*signal_q - 0.00333*pow(signal_q,2)
		# baseline_v = 5.02*signal_q - 0.00333*pow(baseline_q,2)
		gain_v = new_v - baseline_v
		# nonlinear
		if gain_v > 633:
			gain_v = 717 - 83.5*math.exp(-(signal_q-139)/75.5)
	else:
		if baseline_v<717:
			baseline_q = max_linear_range - 75.5*math.log((717-baseline_v) / 83.5)
			signal_q = baseline_q + new_q
			# again put back into response equation
			new_v = 717 - 83.5*math.exp(-(signal_q-max_linear_range)/75.5)
			# baseline_v = 717 - 83.5*math.exp(-(baseline_q-max_linear_range)/75.5))
			gain_v = new_v - baseline_v
		else:
			# No gain for any signal with the baseline currently above the maximum
			gain_v = 0
	return gain_v


