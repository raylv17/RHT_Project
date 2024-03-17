from numpy import exp

# domain length: [-4.5 4.5 -4.5 4.5 -0.6 0.6]
lst_theta = [2, 4, 6, 8]
lst_phi = [2*i for i in lst_theta] # [4, 8, 12, 16]
lst_tau = [0.0001, 0.05, 0.1, 1, 10]  # optical thickness
lst_refining = [1,2,4,8]  # doubled each time
total_cases = len(lst_theta)*len(lst_tau)*len(lst_refining)

def_cells = [24, 24, 3]  # default cells per dimensions
tau_to_abs = lambda x: x/1.2; #1.2 length z-dimension
absorp = [f"{tau_to_abs(i):.6f}" for i in lst_tau]

if __name__ == "__main__":
    print()
    print(f"## PARAMETERS")
    print(f"number of cases: {total_cases}")
    print(f"theta:           {lst_theta}")
    print(f"phi:             {lst_phi}")
    print(f"tau:             {lst_tau}")
    print(f"absorptivity:    {absorp}")
    print()
    print(f"## GEOMETRY:")
    print(f"default cells per dim: {def_cells}")
    print(f"refinement multipliers: {lst_refining}")



