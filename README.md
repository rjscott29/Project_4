# Project_4

This project is used to simulate insulators and predict which dielectric material was used in an experiment. DielectricSim.py utilizes data from dielectric_table.txt to create a list of dielectric materials and dielectric constants that could have been included in the experiment. The simulation will take data of Nmeas measurements for Nexp experiments and record that in a text file.

DielectricAnalysis.py takes that text file of data, calculates some likelihoods, and shows a distribution of which dielectric material maximizes the likelihood function for the distribution of data given. All data is taken from gaussian distributions.
