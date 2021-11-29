# A TU Delft 3rd Year Student Project (WB3575)
## Design of an A-CAES system as part of the ELECS minor programme
This repository is dedicated to a thermodynamic calculator for an A-CAES (Adiabatic Compressed Air Energy Storage) system. This project is part of the ELECS (Engineering for Large-Scale Energy Conversion and Storage) minor programme at TU Delft.

## Scripts and Files
The data files are collected in the 'data' folder.

There are five scripts, structured as follows:
* "tools.py" contains the functions that are used within the two aforementioned scripts
* "specific_heat.py" uses a high-accuracy model to calculate the mean value of cp and kappa
* "theory_calc.py" is a theoretical model of the compressor, plotting the temperature after the compressor as a function of efficiency
* "experiment_compressor.py" contains experimental values from the compressor test, plotting the raw data and calculating the efficiency and power
* "experiment_turbine.py" contains experimental values from the turbine test, plotting the raw data and calculating the efficiency and power

## Use
The main importance is the layout of the '.xls' files. Firstly, the decimal point should be used, not the decimal comma. Secondly, a header row should be present, where the following names are separated by tabs, in this exact order:
"time	torqv	rpmv	temp1	temp2	temp3	temp4	volt	curr	flow	torqnm	rpm	pressure	runtime"
