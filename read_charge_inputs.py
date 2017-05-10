import ROOT
import numpy as np
from rootpy.io import root_open
from rootpy.plotting import Hist

def charge_inputs(tracker_region):
	'''
	Read all relevent information for the charge distributions in data
	'''
	print "Reading Data Charge Distributions for {}".format(tracker_region)

	data_landau = {}
	with root_open('input/landau_26042017.root') as f:
		data_landau['det']   = tracker_region

		# CLUSTER CHARGE
		input_hist = 'landauPlot/landau_{}_clusterCharge'.format(tracker_region)
		data_landau['hist_clusterCharge']  = f.Get(input_hist).Clone()
		data_landau['hist_clusterCharge'].SetDirectory(0)
		data_landau['edges'] = list(data_landau['hist_clusterCharge'].xedges())

		# NORMALISED CLUSTER CHARGE
		normalised_hist = data_landau['hist_clusterCharge'].Clone()
		normalised_hist.Scale(1 / data_landau['hist_clusterCharge'].Integral())
		data_landau['hist_clusterCharge_normed'] = normalised_hist
		data_landau['hist_clusterCharge_normed'].SetDirectory(0)


		# STRIP CHARGE
		input_hist = 'landauPlot/landau_{}_stripCharge'.format(tracker_region)
		data_landau['hist_stripCharge']  = f.Get(input_hist).Clone()
		data_landau['hist_stripCharge'].SetDirectory(0)

		# NORMALISED STRIP CHARGE
		normalised_hist = data_landau['hist_stripCharge'].Clone()
		normalised_hist.Scale(1 / data_landau['hist_stripCharge'].Integral())
		data_landau['hist_stripCharge_normed'] = normalised_hist
		data_landau['hist_stripCharge_normed'].SetDirectory(0)


		# STRIP CHARGE
		input_hist = 'landauPlot/stripClusterFractionHist_{}'.format(tracker_region)
		data_landau['hist_stripClusterFraction']  = f.Get(input_hist).Clone()
		data_landau['hist_stripClusterFraction'].SetDirectory(0)

		# NORMALISED STRIP CHARGE
		normalised_hist = data_landau['hist_stripClusterFraction'].Clone()
		normalised_hist.Scale(1 / data_landau['hist_stripClusterFraction'].Integral())
		data_landau['hist_stripClusterFraction_normed'] = normalised_hist
		data_landau['hist_stripClusterFraction_normed'].SetDirectory(0)
		data_landau['edges_stripClusterFraction'] = list(data_landau['hist_stripClusterFraction'].xedges())


		# STRIP CHARGE
		input_hist = 'landauPlot/landau_TOB6_stripCharge'
		data_landau['hist_inputCharge']  = f.Get(input_hist).Clone()
		data_landau['hist_inputCharge'].SetDirectory(0)
		data_landau['edges'] = list(data_landau['hist_inputCharge'].xedges())

		# NORMALISED STRIP CHARGE
		normalised_hist = data_landau['hist_inputCharge'].Clone()
		normalised_hist.Scale(1 / data_landau['hist_inputCharge'].Integral())
		data_landau['hist_inputCharge_normed'] = normalised_hist
		data_landau['hist_inputCharge_normed'].SetDirectory(0)
		# print list(data_landau['hist_stripClusterFraction_normed'].value())

	return data_landau


def preAPV_charge_from_data(q_to_mv):
	'''
	Transform charge distribution in data post-APV to pre-APV to use in simulation
	'''
	# from global_vars import tracker_deets
	from mathematical_tools import return_rnd_Uniform, amplifier_response2, charge_transformation
	import rootpy.plotting.root2matplotlib as rplt

	# import other externals
	import matplotlib as mpl
	import matplotlib.pyplot as plt
	import numpy as np
	import gc
	stripChargePreAPV = {}
	stripChargePostAPV = {}

	with root_open('input/landau_26042017.root') as f:

		for region in ['TIB1','TIB2','TIB3','TIB4','TOB1','TOB2','TOB3','TOB4','TOB5','TOB6']:
			print 'Doig region {}'.format(region)

			# Get Normalised Strip Charge Distribution from Region in Tracker
			input_hist = 'landauPlot/landau_{}_stripCharge'.format(region)
			h = f.Get(input_hist).Clone()
			edges = list(h.xedges())
			h.Scale(1 /h.Integral())

			# Initialise Histogram to Contain preAPV Charge Distribution
			stripChargePreAPV[region] = Hist(edges, name=region)
			stripChargePostAPV[region] = h

			# Simulatet postAPV Charge Distribution
			n=0
			while n < 100000:
				x = return_rnd_Uniform()
				interval = np.array([0.])
				quantile = np.array([x])
				h.GetQuantiles( 1, interval, quantile)


				# Has e->fC built in
				response = interval[0]*q_to_mv

				# Calculate preAPV charge
				preAPV_q = amplifier_response2(0, response, 0, noise=False, calculate_preAPVCharge=True )
				stripChargePreAPV[region].Fill(charge_transformation(preAPV_q, to_e=True))

				# print "Charge Post APV (e): {}".format(interval[0])
				# # print "Charge Post APV {fC}: {}".format(postAPVcharge)
				# print "Transformation Factor : {}".format(q_to_mv)
				# print "Response from Charge : {}".format(response)
				# print "Input Charge for response [fc]: {}".format(preAPV_q)
				# print "Input Charge for response [e]: {}".format(charge_transformation(preAPV_q, to_e=True))
				# raw_input('Enter')

				n+=1

			stripChargePreAPV[region].Scale(1 / stripChargePreAPV[region].Integral())
			stripChargePreAPV[region].SetDirectory(0)
			stripChargePostAPV[region].SetDirectory(0)

	with root_open('input/preAPVCharge.root', 'recreate') as f2:
		for region in ['TIB1','TIB2','TIB3','TIB4','TOB1','TOB2','TOB3','TOB4','TOB5','TOB6']:
			stripChargePreAPV[region].Write()
		
			fig = plt.figure()
			ax = fig.add_subplot(1, 1, 1)
			rplt.hist(
				stripChargePostAPV[region], 
				histtype='step',
				facecolor='red', 
				edgecolor='red',
				fill = True,
				alpha=0.5,
				label='PostAPV',
			)
			rplt.hist(
				stripChargePreAPV[region], 
				histtype='step',
				facecolor='blue', 
				edgecolor='blue',
				fill = True,
				alpha=0.5,
				label='PreAPV',
			)
			ax.set_ylim([0,0.1])
			ax.set_xlabel('Charge [e]')
			ax.set_ylabel('N')
			fig.suptitle('Strip-Cluster Charge Distribution', fontsize=14, fontweight='bold')
			plt.title('Title', loc='right')
			leg = plt.legend(loc='best')
			leg.draw_frame(False)	
			fig.savefig('Test{}.pdf'.format(region), bbox_inches='tight')
			fig.clf()
			plt.close()
			gc.collect()
	return






