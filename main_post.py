from libraries.postproc import *
from inputparams import *


# from inputs.py  
# lst_theta = [2, 4, 6, 8]
# lst_phi = [4, 8, 12, 16]
# lst_tau = [0.0001, 0.05, 0.1, 1, 10]  # optical thickness
# lst_refining = [1,2,4,8] # doubled refining every four steps
# total_cases = len(lst_theta)*len(lst_tau)*len(lst_refining)
# print(f"number of cases: {total_cases}")

# def_cells = [24, 24, 3]  # default cells per dimensions
# tau_to_abs = lambda x: 1 - exp(-x)
# absorp = [f"{tau_to_abs(i):0.6f}" for i in lst_tau]
# ----------------------------------------------------------#

# user defined custom params
# lst_refining = [1,2,4]


### MAIN PROGRAM ###
# creates subfolder for DATA and copies linesample_RAD files
gather_linesample_RAD(lst_theta, lst_phi, lst_tau, lst_refining)
# copies all Probe folders into DATA
gather_DO_P_dir(lst_theta, lst_phi, lst_tau, lst_refining)
# copies the entire postProcessing folder for each case into DATA
gather_postProcessing_dir(lst_theta, lst_phi, lst_tau, lst_refining) 
# copies 08_log.rad files into DATA
gather_directions(lst_theta, lst_phi, lst_tau, lst_refining) 


##################
# DISPLAY SIMULATION TIMES
sim_time = sim_times(lst_theta, lst_phi, lst_tau, lst_refining, show=False)
print(f"total: {sum(sim_time)} s ~ {sum(sim_time)/3600} hrs")

##################
# PLOTS
lst_theta=[2,4,6,8]
lst_phi = [2*i for i in lst_theta]
lst_tau = [10]
lst_refining = [8]
plot_all_G(lst_theta, lst_phi, lst_tau, lst_refining)


lst_theta=[2,4,6,8]
lst_phi = [2*i for i in lst_theta]
lst_tau = [1]
lst_refining = [8]
plot_all_ILambda(lst_theta, lst_phi, lst_tau, lst_refining)