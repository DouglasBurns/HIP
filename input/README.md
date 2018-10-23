landau.root
Cluster Charge?

simLandau.root:
From simulated MinBias Events
Number of electrons per strip after the the sim hit is split up over strips
Before APV gain, zero supression, addition of noise
Large peak at zero due to no zero supression.
No cutoff at 60,000e caused by ADC truncation https://github.com/cms-sw/cmssw/blob/09c3fce6626f70fd04223e7dacebf0b485f73f54/SimTracker/SiStripDigitizer/src/SiTrivialDigitalConverter.cc#L80-L81

landau_OneStripClusters.root
Charge deposition from strips forming a single cluster

landau_Sim_eta_lt1_allStrips.root
Charge deposition from all strips for |eta| < 1

landau_Sim_eta_lt1_noisy_allStrips.root
Charge deposition from all strips for |eta| < 1 + noise + ZS

landau_Sim_eta_lt1_allTrackStrips.root
Charge deposition from all strips associated to tracks for |eta| < 1 

landau_26042017.root
Recalculated occupancies and charge sharing for |eta| < 1
Landau for charge on each strip in cluster, as opposed to total cluster charge 

171107_landau_lowPU.root
Charge deposition from strips associated to tracks in a low PU data run.

charge_distribution.root == landau_21042017.root

landau_Data_290118.root
LowPU charge distribution in data. Tracks or Clusters

landau_Sim_290118.root
SCD, ZS, Clusters and Tracks

landau_highPU_highTau.root
HighPU charge distribution data. Taken from VR before HIP fix

landau_highPU_highTau.root
HighPU charge distribution data. Taken from ALCARECO after HIP fix (Alignment and Calibration Reconstructed files: AlcaReco data is the special RECO data for the alignment and calibration tasks.)
