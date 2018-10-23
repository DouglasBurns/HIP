from modules.read_charge_inputs import input_charge_distributions
from modules.pandas_utils import make_folder_if_not_exists
from modules.mathematical_tools import return_rnd_Poisson, return_rnd_Gaussian, return_rnd_Landau, return_strip_charge, is_beam_present, amplifier_response
from modules.global_vars import REGIONS
import matplotlib.pyplot as plt
import gc

def testing_Poisson():
	'''
	Quick test of the poisson random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(return_rnd_Poisson(10))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 30, range=[0, 30], normed=True)
	ax.set_xlabel('Po()')
	ax.set_ylabel('N')
	fig.savefig('plots/Testing/PoissonRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return

def testing_Gaussian():
	'''
	Quick test of the Gaussian random number generation
	Mean = 0
	Sigma = 1
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(return_rnd_Gaussian(0,1))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 30, range=[-5, 5], normed=True)
	ax.set_xlabel('Gaussian()')
	ax.set_ylabel('N')
	fig.savefig('plots/Testing/GaussianRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return

def testing_Landau():
	'''
	Quick test of the Landau random number generation
	Mean = 100
	'''
	rnd_array = []
	for i in range (0,10000):
		rnd_array.append(return_rnd_Landau(100, 10))
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	count, bins, ignored = plt.hist(rnd_array, 125, range=[0, 500], normed=True)
	ax.set_xlabel('Landau()')
	ax.set_ylabel('N')
	fig.savefig('plots/Testing/LandauRNG.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return

def testing_ChargeDistribution():
	'''
	Quick test of the poisson random number generation
	Mean = 100
	'''
	for region in REGIONS:
		Q_DIST 	= input_charge_distributions('input/180207/landau_scd_070218_orig.root', region)

		rnd_array = []
		for i in range (0,10000):
			rnd_array.append(return_strip_charge(Q_DIST))
		fig = plt.figure()
		ax = fig.add_subplot(1, 1, 1)
		count, bins, ignored = plt.hist(rnd_array, 200, range=[0, 100000], normed=True)
		ax.set_xlabel('Charge')
		ax.set_ylabel('N')
		fig.savefig('plots/Testing/ChargeDistribution_{}_RNG.pdf'.format(region), bbox_inches='tight')
		plt.show()
		fig.clf()
		plt.close()
		gc.collect()
	return

def testing_Response():
	'''
	Quick test of the response
	MIP 		: 	0 -> 200fC
	Baseline V 	: 	0 mV

	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	1MIP 		:	3.75 fC
	'''
	array_v = []
	for i in range (0,400): 
		_, _, v, _, _ = amplifier_response(i, 0, noise=False)
		array_v.append(v)
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(array_v)
	ax.set_xlabel('Input signal [fC]')
	ax.set_ylabel('$V_{out}$')
	fig.savefig('plots/Testing/NewPreAmpResponse.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()

	array_g = []
	for i in range (0,1000): 
		gain_vq, gain_v, _, _, _ = amplifier_response(3.75, i, noise=False)
		array_g.append(gain_vq)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(array_g)
	ax.set_xlabel('Baseline Voltage [mV]')
	ax.set_ylabel('(Signal Response - Baseline) / Signal Charge [mV/fC]')
	fig.savefig('plots/Testing/NewPreAmpGain.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def testing_BeamStructure():
	'''
	Quick test of the response
	Baseline V 	:	0 -> 1000mV
	1MIP 		:	3.75 fC
	'''
	print "May need to manually change which beam structure you want here (plots_test.testing_BeamStructure)"
	array_bx = []
	array_beam = []
	for i in range (1,3564):
		array_bx.append(i)
		if is_beam_present(i, 3):
			array_beam.append(1)
		else: 
			array_beam.append(0)

	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	plt.plot(
		array_bx, 
		array_beam,
		color='green',
		lw=0,
	)
	ax.set_ylim([0,1.1])
	ax.set_xlim([0,3564])
	ax.fill_between(array_bx, 0, array_beam, facecolor='green')
	ax.set_xlabel('Bunch Crossing')
	ax.set_ylabel('Beam Present')
	fig.savefig('plots/Testing/BeamStructure.pdf', bbox_inches='tight')
	plt.show()
	fig.clf()
	plt.close()
	gc.collect()
	return


def run_tests():
	'''
	Run various tests
	'''
	make_folder_if_not_exists('plots/Testing/')

	# # Test Poisson RNG
	# testing_Poisson()
	# # Test Gaussian RNG
	# testing_Gaussian()
	# # Test Landau RNG
	# testing_Landau()
	# # Test gain using MIP of 3.75fC
	# testing_Response()
	# # Show the LHC beam structure in use
	# testing_BeamStructure()
	# # Test the charge distributions
	testing_ChargeDistribution()
	return
