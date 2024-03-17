import os
import time
from numpy import exp

def remove_cases(lst_theta, lst_phi, sure=False):
    # locate directories
    for theta,phi in zip(lst_theta, lst_phi):
        name = f"th_{theta}-ph_{phi}"
        if not (os.path.isdir(name)):
            print(f"already removed: {name}")
            continue
        else:
            # second confirmation
            if sure:
                os.system(f"rm -r {name}")
                print(f"removed: {name}")
            else:
                print(f"not removed: {name}")

def remove_ref_cases(lst_theta, lst_phi, lst_tau, lst_refining, sure=False):
    # locate directories
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                if not (os.path.isdir(name)):
                    print(f"already removed: {name}")
                    continue
                else:
                    # second confirmation
                    if sure:
                        os.system(f"rm -r {name}")
                        print(f"removed: {name}")
                    else:
                        print(f"not removed: {name}")

# create folders
    # check if folder already exists, don't create or modify
def create_cases(lst_theta, lst_phi, lst_tau, lst_refining, overwrite=False):
    # locate directories
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name)

                # create case
                if os.path.isdir(path) and not(overwrite):
                    # print("exists")
                    continue
                else:
                    # print(path)
                    os.system(f"mkdir -p {path}")
                    os.system(f"cp -r base/* {path}")

# modify parameters: optical thickness (tau), theta, and phi
def mod_param(lst_theta, lst_phi, lst_tau, lst_refining):
    # locate case
    tau_to_abs = lambda x : x/1.2 # Kappa
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")

                # locate and open radiationProperties file
                path = os.path.join(os.getcwd(),name,"constant","radiationProperties")
                with open(path, 'r') as file:
                    filedata = file.read()
                
                # writing modifications in parameter
                filedata = filedata.replace("_tau",str(tau_to_abs(tau))) \
                                   .replace("_phi",str(phi)) \
                                   .replace("_theta",str(theta))


                with open(path, 'w') as file:
                    file.write(filedata)

                file.close()


# modify resolution
def mod_resolution(lst_theta, lst_phi, lst_tau, lst_refining, def_cells):
    # locate directories
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for ref in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{ref}")
                # locate and open blockMeshDict file
                path = os.path.join(os.getcwd(),name,"system","blockMeshDict")

                with open(path, 'r') as file:
                    filedata = file.read()

                # writing modifications in cell boxes per dimension (grid resolution)
                filedata = filedata.replace("_x_cells",str(def_cells[0]*ref)) \
                                   .replace("_y_cells",str(def_cells[1]*ref)) \
                                   .replace("_z_cells",str(def_cells[2]*ref))

                with open(path, 'w') as file:
                    file.write(filedata)


                file.close()

def add_more_ILambdas(lst_theta, lst_phi, lst_tau, lst_refining):
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name,"system","controlDict")
                new_text = " ".join([f"ILambda_{i}_0" for i in range(4*theta*phi)])
                # print(new_text)
                with open(path,"r") as file:
                    filedata = file.read()
                    # print(read)
                    old_text = "ILambda_0_0 ILambda_1_0 )"
                    filedata = filedata.replace(old_text, new_text+")")

                with open(path,"w") as file:
                    file.write(filedata)
                    # index = read.find(old_text)
                    # print(f"{read[index:index + len(old_text)]} | {theta} {phi} {tau} {res}, i {index}")

def run_cases(lst_theta, lst_phi, lst_tau, lst_refining):
    # locate directories
    count = 0
    total_cases = len(lst_theta)*len(lst_tau)*len(lst_refining)
    tot_start = time.time()
    print("starting simulation:")
    print(f"total cases: {total_cases}")
    print(f"refinement multipliers: {lst_refining}\n...")
    for ref in lst_refining:
        for theta,phi in zip(lst_theta, lst_phi):
            for tau in lst_tau:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{ref}")
                path = os.path.join(os.getcwd(),name)
                count = count + 1
                start = time.time()
                display_time = lambda : print(f"{count:2}/{total_cases}, {(count/total_cases)*100:>5.1f}% {time.time() - start:6.2f}s ||", end=" ", flush=True)
                clean_sim = lambda : os.system(f"cd {path} && rm -r 0")
                run_sim = lambda : os.system(f"cd {path} && bash runOPF.sh")
                # display_time()
                # check if already simulated to completion
                if os.path.isfile(os.path.join(path,"08_log.rad")):
                    with open(os.path.join(path,"08_log.rad")) as file:
                        read = file.read()
                        # print(f"th_{theta}-ph_{phi}-tau_{tau}-res_{res}.csv: {read[-5:].strip()}")

                    # restart if incomplete
                    if not(read[-5:].strip() == "End"):
                        # print(f"th_{theta}-ph_{phi}-tau_{tau}-res_{ref}")
                        clean_sim() # restart if incomplete
                        run_sim()
                        display_time()
                    else:
                        display_time()
                else:
                    # restart if not simulated
                    if os.path.isdir(os.path.join(path,"0")):
                        clean_sim()
                    run_sim()
                    display_time()
            print(f"\ndone theta-{theta}, phi-{phi}")
        print(f"done ref-{ref}/\n")

    sim_time = time.time() - tot_start
    print(f"{sim_time:6.3f}")
    return sim_time

def run_postProcess(lst_theta, lst_phi, lst_tau, lst_refining):
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for ref in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{ref}")
                path = os.path.join(os.getcwd(),name)
                run_pp = lambda : os.system(f"cd {path} && bash runonlyPostProcess.sh")
                # check if already simulated to completion
                if os.path.isfile(os.path.join(path,"08_log.rad")):
                    with open(os.path.join(path,"08_log.rad")) as file:
                        read = file.read()
                        # print(f"th_{theta}-ph_{phi}-tau_{tau}-res_{res}.csv: {read[-5:].strip()}")

                    # restart if incomplete
                    if not(read[-5:].strip() == "End"):
                        print("case not complete")
                    else:
                        run_pp()

    
    


if __name__ == "__main__":
    print(os.getcwd())
