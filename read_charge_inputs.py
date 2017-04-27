import ROOT
from rootpy.io import root_open

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
		data_landau['edges'] = list(data_landau['hist_stripCharge'].xedges())

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
		
		# print list(data_landau['hist_stripClusterFraction_normed'].value())

	return data_landau
