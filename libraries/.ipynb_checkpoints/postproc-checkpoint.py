import os
import scipy.integrate as integrate
import numpy as np 
import matplotlib.pyplot as plt

def gather_linesample_RAD(lst_theta, lst_phi, lst_tau, lst_refining):
    # lst_theta, lst_phi, lst_tau, lst_refining
    folder_name = "DATA/all_data_linesample_RAD"
    dest = os.path.join(os.getcwd(),folder_name)
    if os.path.isdir(dest):
        print(f"{folder_name} already exists, not modified")
    else:
        os.system(f"mkdir -p {folder_name}")
    # print(dest)

    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name,"postProcessing","DO_linesample_RAD.sets","1")
                file_name = f"Line_th_{theta}-ph_{phi}-tau_{tau}-res_{res}.csv"
                if os.path.isdir(path):
                    # os.system(f"cd {path} && rm {phi}-{tau}-{res}")
                    os.system(f"cd {path} && cp * {file_name} && mv {file_name} {dest}")
                    # print(f"{file_name} transferred")
                else:
                    print(f"does not exist, skipping {file_name}")

def gather_postProcessing_dir(lst_theta, lst_phi, lst_tau, lst_refining):
    # lst_theta, lst_phi, lst_tau, lst_refining
    folder_name = "DATA/all_postProcessing"
    dest = os.path.join(os.getcwd(),folder_name)
    if os.path.isdir(dest):
        print(f"{folder_name} already exists, not modified")
    else:
        os.system(f"mkdir -p {folder_name}")
    # print(dest)

    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name,"postProcessing")
                dir_name = f"PostProc_th_{theta}-ph_{phi}-tau_{tau}-res_{res}"
                if os.path.isdir(path):
                    if os.path.isdir(os.path.join(os.getcwd(),folder_name,dir_name)): 
                        continue
                    else:
                        os.system(f"cd {os.path.join(os.getcwd(),folder_name)} && mkdir {dir_name}")
                        # os.system(f"cd {path} && rm {phi}-{tau}-{res}")
                        os.system(f"cd {path} && cp -r * {os.path.join(dest,dir_name)}")
                        print(f"{dir_name} transferred")
                else:
                    print(f"does not exist, skipping {dir_name}")

def gather_DO_P_dir(lst_theta, lst_phi, lst_tau, lst_refining):
    # lst_theta, lst_phi, lst_tau, lst_refining
    folder_name = "DATA/all_DO_P"
    dest = os.path.join(os.getcwd(),folder_name)
    if os.path.isdir(dest):
        print(f"{folder_name} already exists, not modified")
    else:
        os.system(f"mkdir -p {folder_name}")
    # print(dest)

    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name,"postProcessing","DO_P.probes","0")
                dir_name = f"Probe_th_{theta}-ph_{phi}-tau_{tau}-res_{res}"
                if os.path.isdir(path):
                    if os.path.isdir(os.path.join(os.getcwd(),folder_name,dir_name)): 
                        continue
                    else:
                        os.system(f"cd {os.path.join(os.getcwd(),folder_name)} && mkdir {dir_name}")
                        # os.system(f"cd {path} && rm {phi}-{tau}-{res}")
                        os.system(f"cd {path} && cp -r * {os.path.join(dest,dir_name)}")
                        print(f"{dir_name} transferred")
                else:
                    print(f"does not exist, skipping {dir_name}")


def sim_times(lst_theta, lst_phi, lst_tau, lst_refining, show=False):
    # returns an array of all simulation times
    sim_time = []
    for res in lst_refining:
        if show:
            print(f"## res: {res}")
        for theta,phi in zip(lst_theta, lst_phi):
            for tau in lst_tau:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name)
                # display_time = lambda t : print(f"{count:2}/{total_cases}, {(count/total_cases)*100:>5.1f}% {t:6.2f}s ||",end=" ")
                if os.path.isfile(os.path.join(path,"08_log.rad")):
                    with open(os.path.join(path,"08_log.rad")) as file:
                        read = file.read()
                        index = read.find("ExecutionTime")
                        if (index != -1):
                            exec_time_per_case = float(read[index+15:].split()[0])
                            if show:
                                # with open("sim_times_ref1-4.txt","w+") as f:
                                #     print(f"{exec_time_per_case:<10}:th_{theta}-ph_{phi}-tau_{tau}-res_{res}",file=f)
                                print(f"{exec_time_per_case:<10}:th_{theta}-ph_{phi}-tau_{tau}-res_{res}")
                            sim_time.append(exec_time_per_case)
                        else:
                            print(f":th_{theta}-ph_{phi}-tau_{tau}-res_{res}")

                            
        if show:
            # print(f"## cummulated time: {sum(sim_time): 0.3f} s ~ {sum(sim_time)/3600} hrs")
            print()
    return sim_time


def modest_I(tau, theta):
    tau_l = 11
    if (0 <= theta <= np.pi/2):
        return 1 - (np.e)**((-tau)/np.cos(theta))
    elif (np.pi/2 < theta <= np.pi):
        return 1 - (np.e)**((-tau + tau_l)/np.cos(theta))

def modest_G(tau, theta):
    fn = lambda tau,theta : 1 - np.e**(-tau/np.cos(theta))
    return integrate.quad(fn, np.pi/2, 0,  args=tau)[1] # w.r.t theta
    

def plot_data(lst_tau, lst_theta):
    I = {}
    G = {}
    for theta in lst_theta:
        I[theta] = []
        G[theta] = []

    for tau in lst_theta:
        for theta in lst_theta:
            I[theta].append(modest_I(tau, theta))
            # G[theta].append(modest_G(tau, theta))
    return I,G


def plot_analytical(lst_tau):
    lst_theta = np.linspace(0,np.pi,100)


    # fig, ax = plt.subplots(subplot_kw={'projection': 'polar'})
    
    for tau in lst_tau:
        an_I = []
        an_G = []
        for theta in lst_theta:
            an_I.append(modest_I(tau, theta))
            an_G.append(modest_G(tau, theta))

            print(f"{an_I[-1]:.4f}::{theta}::{tau}")
        # print(len(lst_theta), len(an_I))
        # ax.plot(lst_theta, an_I)
        # plt.scatter(lst_theta, an_I, s=5, label=f"n_{tau:0.3f}")
        plt.scatter(lst_theta, an_G, s=5, label=f"n_{tau:0.3f}")
    plt.grid()
    plt.legend()
    plt.xlabel(r"$\theta$")
    plt.ylabel(r"$I_\lambda$")
    plt.savefig("analytical_I_pi",dpi=300)
    plt.show()






if __name__ == "__main__":

	print(os.getcwd())
