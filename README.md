# APV Simulation

## Setup simulation
```
git clone https://github.com/DouglasBurns/HIP
cd ChipSimulaton/
source bin/env.sh
```

## Prepare charge distributions
```
python ResponseSimulator.py -r
```
- Take file from local input/* and collate all possible distributions:
-- Original 	```REGION+_Original'''
-- Normalised to 1 	```REGION+_NormTo1'''
-- Cumulative Dist 	```REGION+_CDF'''
-- Cut at 10 000e 	```REGION+_Cut'''
-- Normalised cut at 10 000e 	```REGION+_CutNormTo1'''
-- Cut CDF 	```REGION+_CutCDF'''
- Load this file for future simulations

## Run Simulation
```
python ResponseSimulator.py
```
- Run simulation using inputs based in modules.global_vars.py
- Produces plots in plots_Summer18 (defined in modules.APVSimulation.py)

## Most inputs to simulation
```
modules.global_vars.py
'''
- N_BX = Length of simulation in BX
- SCD_CUTS = Which cut charge distribution to use. Charge deposition from cut distribution via N samples and via full distribution from Landau throw
- REGIONS = Region of tracker to simulate
- TAUS = decay constant for charge sensitive amplifier
- BEAMS = Choose which beam filling scheme to use
- BLEEDTYPES = Decay by charge or voltage (voltage nottested in a long time)
- REGION_DETAILS = Occupancies for each layer under different conditions
- NOISE = Noise parameters (Not implemented in APVSimulation class yet, but should be present in all used functions [Present in modules.mathematical_tools.py])

## Most worker functions
```
modules.mathematical_tools.py
'''
- Contains all the functions for modelling the charge and response of the APV

