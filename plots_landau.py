# import root
import ROOT
from rootpy.plotting import Hist
from rootpy.io import root_open
import rootpy.plotting.root2matplotlib as rplt

# import other externals
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import gc

mpl.rcParams['agg.path.chunksize'] = 50000

def run_landaus(title, folder_path, d_mip_variables, data_charge_inputs):
	'''
	Plot any landaus
	'''
	print "- - - - - - - - - - - - - - - - - - -"
	print "Plotting Data Simulation Comparisons"
	print "- - - - - - - - - - - - - - - - - - -"
	########################################################################################################################
	### Fill ROOTPY Hists
	########################################################################################################################
	charge_deposited_hist = Hist(data_charge_inputs['edges'])
	for v in d_mip_variables['q_Deposited_e']:
		charge_deposited_hist.Fill(v)
	charge_deposited_hist.Scale(1 / charge_deposited_hist.Integral() )

	unweighted_charge_deposited_hist = Hist(data_charge_inputs['edges'])
	for v in d_mip_variables['q_ClusterDeposited_e']:
		unweighted_charge_deposited_hist.Fill(v)
	unweighted_charge_deposited_hist.Scale(1 / unweighted_charge_deposited_hist.Integral() )

	charge_read_hist = Hist(data_charge_inputs['edges'])
	for v in d_mip_variables['q_Read_e']:
		charge_read_hist.Fill(v)
	charge_read_hist.Scale(1 / charge_read_hist.Integral() )

	charge_weight_hist = Hist(data_charge_inputs['edges_stripClusterFraction'])
	for v in d_mip_variables['q_Weight_e']:
		charge_weight_hist.Fill(v)
	charge_weight_hist.Scale(1 / charge_weight_hist.Integral() )

	########################################################################################################################
	### Charge Weighting
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		data_charge_inputs['hist_stripClusterFraction_normed'], 
		histtype='step',
		facecolor='red', 
		edgecolor='red',
		fill = True,
		alpha=0.5,
		label='Strip-Cluster Distribution',
	)
	rplt.hist(
		charge_weight_hist, 
		histtype='step',
		facecolor='blue', 
		edgecolor='blue',
		fill = True,
		alpha=0.5,
		label='Scaling Distribution applied to Simulated Charge Deposition ',
	)
	ax.set_ylim([0,0.1])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Strip-Cluster Charge Distribution', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_Data_ChargeWeighting_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	# ########################################################################################################################
	# ### Data STRIP vs Cluster Charge
	# ########################################################################################################################
	# fig = plt.figure()
	# ax = fig.add_subplot(1, 1, 1)
	# rplt.hist(
	# 	data_charge_inputs['hist_clusterCharge'], 
	# 	histtype='step',
	# 	facecolor='orange', 
	# 	edgecolor='orange',
	# 	fill = True,
	# 	alpha=0.5,
	# 	label='Cluster Charge Distribution in Data',
	# )
	# rplt.hist(
	# 	data_charge_inputs['hist_stripCharge'], 
	# 	histtype='step',
	# 	facecolor='red', 
	# 	edgecolor='red',
	# 	fill = True,
	# 	alpha=0.5,
	# 	label='Strip Charge Distribution in Data',
	# )
	# # ax.set_ylim([0,0.15])
	# ax.set_xlabel('Charge [e]')
	# ax.set_ylabel('N')
	# fig.suptitle('Strip v Cluster Charge Deposition in Data', fontsize=14, fontweight='bold')
	# plt.title(title, loc='right')
	# leg = plt.legend(loc='best')
	# leg.draw_frame(False)	
	# fig.savefig(folder_path+'Data_StripCluster.pdf', bbox_inches='tight')
	# fig.clf()
	# plt.close()
	# gc.collect()


	########################################################################################################################
	### Data STRIP vs Cluster Charge
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		data_charge_inputs['hist_clusterCharge_normed'], 
		histtype='step',
		facecolor='orange', 
		edgecolor='orange',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Data',
	)
	rplt.hist(
		data_charge_inputs['hist_stripCharge_normed'], 
		histtype='step',
		facecolor='red', 
		edgecolor='red',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Data',
	)
	ax.set_ylim([0,0.15])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Strip v Cluster Charge in Data', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'Data_StripCluster_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Simulation STRIP vs Cluster Charge
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		unweighted_charge_deposited_hist, 
		histtype='step',
		facecolor='green', 
		edgecolor='green',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Simulation',
	)
	rplt.hist(
		charge_deposited_hist, 
		histtype='step',
		facecolor='blue', 
		edgecolor='blue',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Simulation',
	)
	ax.set_ylim([0,0.1])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Strip v Cluster Charge Deposition in Simulation', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_ChargeDeposition_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Simulation STRIP vs Cluster Charge. Input vs Output Distirbutions
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		charge_deposited_hist, 
		histtype='step',
		facecolor='blue', 
		edgecolor='blue',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Simulation',
	)
	rplt.hist(
		charge_read_hist, 
		histtype='step',
		facecolor='purple', 
		edgecolor='purple',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Simulation from APV Gain',
	)
	ax.set_ylim([0,0.1])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Simulated Charge Deposition Comparison with Readout from Gain', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_ChargeDepositionFromGain_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Strip Charge Deposition From Data vs MC
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		charge_read_hist, 
		histtype='step',
		facecolor='blue', 
		edgecolor='blue',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Simulation',
	)
	rplt.hist(
		data_charge_inputs['hist_stripCharge_normed'], 
		histtype='step',
		facecolor='red', 
		edgecolor='red',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Data',
	)
	# plt.axvline(x=7500, linewidth=1, color='r', label = 'Min Threshold')
	# plt.axvline(x=1500, linewidth=1, color='g', label = 'Min Threshold')
	# plt.axvline(x=3000, linewidth=1, color='b', label = 'Min Threshold')
	# plt.axvline(x=2000, linewidth=1, color='orange', label = 'Min Threshold')

	ax.set_ylim([0,0.1])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Strip Charge Deposition Data vs Simulation', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_Data_StripChargeDeposition_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	########################################################################################################################
	### Cluster Charge Deposition From Data vs MC
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		data_charge_inputs['hist_clusterCharge_normed'], 
		histtype='step',
		facecolor='orange', 
		edgecolor='orange',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Data',
	)
	rplt.hist(
		unweighted_charge_deposited_hist, 
		histtype='step',
		facecolor='green', 
		edgecolor='green',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Simulation',
	)
	ax.set_ylim([0,0.1])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Cluster Charge Deposition Data vs Simulation', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_Data_ClusterChargeDeposition_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()


	# ########################################################################################################################
	# ### Cluster Charge Vs Charge Splitting
	# ########################################################################################################################
	# fig = plt.figure()
	# ax = fig.add_subplot(1, 1, 1)
	# plt.scatter(
	# 	d_mip_variables['q_ClusterDeposited_e'], 
	# 	d_mip_variables['q_Weight_e'], 
	# )
	# ax.set_xlim([0,8000000])
	# ax.set_ylim([0,1])
	# ax.set_xlabel('Cluster Charge [e]')
	# ax.set_ylabel('Strip Charge [e]')

	# # ax.set_ylabel('N')
	# fig.suptitle('Cluster Charge vs Strip Charge [Simulation]', fontsize=14, fontweight='bold')
	# plt.title(title, loc='right')
	# # leg = plt.legend(loc='best')
	# # leg.draw_frame(False)	
	# fig.savefig(folder_path+'TEST.pdf', bbox_inches='tight')
	# fig.clf()
	# plt.close()
	# gc.collect()

	########################################################################################################################
	### All Charge Distributions
	########################################################################################################################
	fig = plt.figure()
	ax = fig.add_subplot(1, 1, 1)
	rplt.hist(
		data_charge_inputs['hist_clusterCharge_normed'], 
		histtype='step',
		facecolor='orange', 
		edgecolor='orange',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Data',
	)
	rplt.hist(
		data_charge_inputs['hist_stripCharge_normed'], 
		histtype='step',
		facecolor='red',
		edgecolor='red',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Data',
	)
	rplt.hist(
		unweighted_charge_deposited_hist, 
		histtype='step',
		facecolor='blue',
		edgecolor='blue',
		fill = True,
		alpha=0.5,
		label='Cluster Charge Distribution in Simulation',
	)
	rplt.hist(
		charge_read_hist, 
		histtype='step',
		facecolor='purple',
		edgecolor='purple',
		fill = True,
		alpha=0.5,
		label='Strip Charge Distribution in Simulation from APV Gain',
	)

	ax.set_ylim([0,0.05])
	ax.set_xlabel('Charge [e]')
	ax.set_ylabel('N')
	fig.suptitle('Strip and Cluster Distributions in Simulation and Data', fontsize=14, fontweight='bold')
	plt.title(title, loc='right')
	leg = plt.legend(loc='best')
	leg.draw_frame(False)	
	fig.savefig(folder_path+'MC_Data_ChargeComparison_Norm.pdf', bbox_inches='tight')
	fig.clf()
	plt.close()
	gc.collect()

	return