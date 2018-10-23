from __future__ import division

# import my scripts
from modules.global_vars import REGIONS, REGION_DETAILS, N_BX, TAUS, BLEEDTYPES, BEAMS, SCD_CUTS
from modules.APVSimulation import APVSim
from modules.read_charge_inputs import ChargePreparation

from modules.plots_test import run_tests

import itertools
import sys
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
	parser.add_argument( "-r", "--remake-charge-inputs", 
		action = "store_true", 
		help = "For debugging" 
	)
	args = parser.parse_args()
	return args

def main(args):
	'''
	'''
	# Run some old tests (May not work)
	if args.tests: 
		print "Running Tests"
		run_tests()
		return

	DEBUG 				= args.debug
	DO_CHARGE_PER_BX 	= False
	CHARGE_DEP_TYPE 	= 'Poisson'
	SCD_PATH 			= 'input/180406/landau_Sim_scd_060418_all.root'
	SCD_CUT 			= False
	nBX 				= N_BX

	# Remodel the charge inputs (Adding in the cut distributions to the files)
	# Output fName+'_all'
	if args.remake_charge_inputs:
		fNames = [
			'input/180406/landau_Data_278808_060418_VFPFix_True.root',
			'input/180406/landau_Data_278770_060418_VFPFix_False.root',
			'input/180406/landau_Sim_scd_060418.root',
			'input/180406/landau_Sim_060418.root',
			'input/180406/landau_Data_060418.root',
		]
		for fName in fNames:
			c = ChargePreparation(fName)
			c()		
		sys.exit("Remade charge files")


	########################################################################################################################
	### mV to e @ Baseline = 0mV, 1MIP = 3.75fC = 23500e
	########################################################################################################################
	for REGION, TAU, SCD_CUT, BLEEDTYPE, BEAM in itertools.product(REGIONS, TAUS, SCD_CUTS, BLEEDTYPES, BEAMS):

		# Which Occupancy?
		OCCS = [
			REGION_DETAILS[REGION]['Occ_Data'],
			REGION_DETAILS[REGION]['Occ_LowOcc_Data'],
			REGION_DETAILS[REGION]['Occ_HighOcc_VFPNoFix_Data'],
			REGION_DETAILS[REGION]['Occ_HighOcc_VFPFix_Data'],
			REGION_DETAILS[REGION]['Occ_Sim'],
		]

		for OCC in OCCS:
			s = APVSim(
				region 		= REGION,
				tau 		= TAU,
				bleedtype 	= BLEEDTYPE,
				scdpath 	= SCD_PATH,
				scdcut 		= SCD_CUT,
				bs 			= BEAM,
				nBX 		= nBX,
				qtype 		= CHARGE_DEP_TYPE,
				add_noise 	= False,
				occ 		= OCC,
			)
			s()
			del s

if __name__ == "__main__":
	args = arg_parser()
	main(args)