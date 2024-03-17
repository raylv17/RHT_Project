from libraries.preproc import *
from inputparams import *

# from inputs.py  
# lst_theta = [2, 4, 6, 8]
# lst_phi = [4, 8, 12, 16]
# lst_tau = [0.0001, 0.05, 0.1, 1, 10]  # optical thickness
# lst_refining = [1,2,4,8] # doubled refining every four steps
# total_cases = len(lst_theta)*len(lst_tau)*len(lst_refining)
# print(f"number of cases: {total_cases}")

# def_cells = [48, 48, 6]  # default cells per dimensions
# tau_to_abs = lambda x: 1 - exp(-x)
# absorp = [f"{tau_to_abs(i):0.6f}" for i in lst_tau]
# ----------------------------------------------------------#

# user defined custom params
lst_refining = [1]

### MAIN PROGRAM ###

# remove_cases(lst_theta, lst_phi, sure=True)
remove_ref_cases(lst_theta, lst_phi, lst_tau, lst_refining, sure=False)
