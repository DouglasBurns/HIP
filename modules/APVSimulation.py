# import my scripts
from modules.mathematical_tools import is_beam_present, charge_transformation, amplifier_response, \
return_strip_charge_from_Poisson, return_strip_charge_from_Samples, bleed_input, mv_to_e
from modules.pandas_utils import dict_to_df, df_to_file, make_folder_if_not_exists
from modules.read_charge_inputs import input_charge_distributions
from modules.plots_simulation import plot_simulation
from modules.plots_distribution import run_distributions, plot_cmssw_charge_distributions, \
plot_cmssw_data_charge_comparisons, plot_cmssw_charge_occupancy_variations, plot_data_VFP_fixes
from modules.plots_landau import run_landaus
from modules.plots_profile import run_profiles

from memory_profiler import profile
import time
import numpy as np

class APVSim(object):
	"""
	A class to model the response of the APV Simulation for a given set of input parameters
	"""
	def __init__(
		self,
		region='TIB_1',
		tau=5,
		bleedtype='Charge',
		scdpath='input/180406/landau_Sim_scd_060418_all.root',
		scdcut=False,
		bs=3,
		nBX=10000,
		add_noise=False,
		qtype='Poisson',
		occ=0
		):
		
		self.region 		= region
		self.occ 			= occ
		self.tau 			= tau
		self.bleedtype 		= bleedtype
		self.scdpath 		= scdpath
		self.scdcut 		= scdcut

		self.beamStructure 	= bs
		self.nBX 			= nBX
		self.qtype 			= qtype

		self._get_charge_distribution()
		self.d_all_bx 		= self._intialise_bx() # All BX Info
		self.d_on_bx 		= None
		self.d_mip_bx 		= None

		self.beam_present 	= None
		self.add_noise 		= add_noise

		self.q_apv_fC 		= 0
		self.q_apv_e 		= 0
		self.v_apv_mV 		= 0
		self.q_eff_e 		= 0
		self.v_response_mV 	= 0
		self.v_gain_mV_fC 	= 0

		self.sim_details 	= {
			"region" : region,
			"occupancy" : occ,
			"tau" : tau,
			"noise" : add_noise,
		}

	# Run the Simulation!
	def __call__(self):
		print "Simulating {} with Occupancy {} and Tau {} (Bleeding by {})".format(
			self.region, 
			self.occ, 
			self.tau, 
			self.bleedtype
		)

		self.bx = 0
		start_time = time.time()
		while (self.bx < self.nBX):
			if (self.bx % int(0.1*self.nBX) == 0):
				print "Bunch Crossing Number : {} in time {}".format(self.bx, time.time()-start_time)
				start_time = time.time()

			self.q_dep_e 		= 0
			self.q_dep_fC 		= 0

			self.beam_present 	= is_beam_present(self.bx, self.beamStructure)

			self._get_charge_deposited()
			self._bleed_baselines()
			self._get_amplifier_response()
			self._fill_bx(self.d_all_bx)

			self.bx += 1
		
		self._print_bx()
		self._generate_folder()
		self._generate_plots()
		# print "Size of Full dataframe {}MB".format(get_size(self.d_all_bx)/1000000)
		# print "Size of ON dataframe {}MB".format(get_size(self.d_on_bx)/1000000)
		# print "Size of Depositions {}MB".format(get_size(self.d_mip_bx)/1000000)
		return

	# @profile
	def _intialise_bx(self):
		'''
		Intialise Information Dictionaries
		'''
		d = {
			"bunchCrossing" : np.empty(self.nBX),
			"isBeam" : np.empty(self.nBX),
			"V_baseline_mV" : np.empty(self.nBX),
			"V_apv_mV" : np.empty(self.nBX),
			"V_response_mV" : np.empty(self.nBX),
			"V_gain_mV_fC" : np.empty(self.nBX),
			"q_noise_fC" : np.empty(self.nBX),
			"q_apv_e" : np.empty(self.nBX),
			"q_dep_e" : np.empty(self.nBX),
			"q_eff_e" : np.empty(self.nBX),
			"q_dep_fC" : np.empty(self.nBX),
		}	
		return d

	# @profile
	def _get_charge_distribution(self):
		'''
		Set the strip charge distribution to use
		'''
		# Setup both options
		icd = input_charge_distributions(
			self.region, 
			fName=self.scdpath
		)
		# Choose one
		if self.scdcut:
			self.scd = icd.scdCut
		else:
			self.scd = icd.scdFull
		return

	# @profile
	def _get_charge_deposited(self):
		if self.scdcut:
			self.q_dep_e 	= return_strip_charge_from_Poisson(self.scd, self.occ, beam_present=self.beam_present)
		else:
			self.q_dep_e 	= return_strip_charge_from_Samples(self.scd, beam_present=self.beam_present, n_samples=1)
		self.q_dep_fC 		= charge_transformation(self.q_dep_e, to_fC=True)
		return

	# @profile
	def _bleed_baselines(self):
		if self.bleedtype == 'Charge':
			self.v_baseline_mV, self.q_baseline_fC = bleed_input(self.q_apv_fC, self.tau, bleedby=self.bleedtype)
		else:
			self.v_baseline_mV, self.q_baseline_fC = bleed_input(self.v_apv_mV, self.tau, bleedby=self.bleedtype)
		return

	# @profile
	def _get_amplifier_response(self):
		self.v_apv_mV, self.v_response_mV, self.v_gain_mV_fC, self.q_apv_fC, self.q_noise_fC = amplifier_response(self.q_baseline_fC, self.q_dep_fC, noise=False )
		self.q_apv_e = charge_transformation(self.q_apv_fC, to_e=True)
		self.q_eff_e = mv_to_e(self.v_response_mV)
		return

	# @profile
	def _fill_bx(self, d):
		'''
		Fill Information Dictionaries
		'''
		d["bunchCrossing"][self.bx] = self.bx
		d["isBeam"][self.bx] = self.beam_present
		d["V_baseline_mV"][self.bx] = self.v_baseline_mV
		d["V_apv_mV"][self.bx] = self.v_apv_mV
		d["V_response_mV"][self.bx] = self.v_response_mV
		d["V_gain_mV_fC"][self.bx] = self.v_gain_mV_fC
		d["q_noise_fC"][self.bx] = self.q_noise_fC
		d["q_apv_e"][self.bx] = self.q_apv_e
		d["q_dep_e"][self.bx] = self.q_dep_e
		d["q_dep_fC"][self.bx] = self.q_dep_fC
		d["q_eff_e"][self.bx] = self.q_eff_e
		return d

	# @profile
	def _print_bx(self):
		self.d_all_bx 	= dict_to_df(d=self.d_all_bx)

		cols_to_print 	= ["isBeam","V_baseline_mV","V_apv_mV","V_response_mV","V_gain_mV_fC","q_noise_fC","q_dep_e","q_dep_fC","q_apv_e", "q_eff_e"]
		print self.d_all_bx[cols_to_print]
		return

	# @profile
	def _generate_folder(self):
		q_type = ''
		self.title = ''

		if self.scdcut:
			c_type='Cut'
		else:
			c_type='Full'

		q_type = '{}_Occ_'.format(c_type)+str(self.occ).replace('.', '_')
		self.title = "$\\tau = $ {}, occ = {}, {}".format(
			self.tau, 
			self.occ,  
			self.region.replace('_',''), 
		)

		folder_segments = [
			q_type, 
			'Tau_'+str(int(self.tau)), 
			'BleedBy'+self.bleedtype
		]
		self.folder_path = 'plots_Summer18/'+self.region+'/'+"_".join(folder_segments)+'/'
		make_folder_if_not_exists(self.folder_path)
		print "Results output to {}".format(self.folder_path)
		return

	# @profile
	def _runNumber(self):
		d_beam = {
			0 	:  	'default',
			1 	: 	'278770',
			2 	: 	'278345',
			3 	: 	'276226',
			-1 	: 	'Off',
		}
		return d_beam[self.beamStructure]

	# @profile
	def _generate_plots(self):
		# deprecated. To Fix
		# run_landaus(title_comp, folder_path, d_trimmed_variables, data_charge_inputs)
		# run_profiles(title, folder_path, simulation_all)

		# Main plots
		plot_simulation(
			self.title, 
			self.folder_path, 
			self.d_all_bx, 
			self.sim_details
		)

		# Plotting some other distributions (Gain, profile etc)
		run_distributions(
			self.title, 
			self.folder_path, 
			self.d_on_bx, 
			self.d_all_bx, 
			self.add_noise, 
			self.region, 
		)

		# Deprecated (May or may not work)
		# plot_cmssw_charge_distributions(self.region)
		# plot_cmssw_data_charge_comparisons(self.region)
		# plot_data_VFP_fixes(self.region)
		# plot_cmssw_charge_occupancy_variations(self.region)
		# plot_cmssw_charge_occupancy_variations(self.region, useFullDist=False)

		self.d_all_bx = None
		return