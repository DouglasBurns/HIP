'''
Any useful mathematical tool should go here
'''
from __future__ import division

import math
from ROOT import gRandom
gRandom.SetSeed()
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
	'''
	q = q0 * math.exp(-t/tau)
	return q, q0-q
