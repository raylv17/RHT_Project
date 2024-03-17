import os
import scipy.integrate as integrate
import numpy as np 
import matplotlib.pyplot as plt
import re
import pandas as pd

### CONSTANTS
from scipy.constants import sigma, pi 
LENGTH = 1.2
TEMP = 1000 # kelvin
I_b = sigma*(TEMP**4)

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

def gather_directions(lst_theta, lst_phi, lst_tau, lst_refining):
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                name = os.path.join(f"th_{theta}-ph_{phi}",f"tau_{tau}",f"res_{res}")
                path = os.path.join(os.getcwd(),name)
                dir_name = f"th_{theta}-ph_{phi}-tau_{tau}-res_{res}"
                new_file = f"log_{dir_name}"
                old_file = "08_log.rad"
                os.system(f"cd {path} && cp {old_file} {new_file}")
                os.system(f"mv {os.path.join(path,new_file)} DATA/all_DO_P/Probe_{dir_name}/")


def read_directions(theta, phi, tau, res):
    dir_name = f"th_{theta}-ph_{phi}-tau_{tau}-res_{res}"
    new_file = f"log_{dir_name}"
    # DATA_dir = "DATA"
    name = os.path.join(os.getcwd(),"DATA","all_DO_P",f"Probe_{dir_name}")
    path = os.path.join(name,new_file)
    with open(path, "r+") as file:
        filedata = file.read()
        all_vec = re.findall(": d : \t\((.*)\)", filedata)
    return all_vec

def read_ILambdas(theta, phi, tau, res):
    dir_name = f"th_{theta}-ph_{phi}-tau_{tau}-res_{res}"
    path = os.path.join(os.getcwd(),"DATA","all_DO_P",f"Probe_{dir_name}")
    num = 4*theta*phi
    ILambdas = []
    for i in range(num):
        with open(os.path.join(path,f"ILambda_{i}_0")) as file:
            filedata = file.read()
            ILambdas.append(filedata.split()[-1])
    # print(len(ILambdas))
    return np.array(ILambdas).astype(float)


def vec_to_theta(all_vec):
    rho = []
    theta = []
    phi = []
    for vec in all_vec:
        vec = np.array([np.double(i) for i in vec.split()])
        rho.append(np.sqrt(sum(vec**2)))
        theta.append(np.arctan(vec[1]/vec[0]))
        phi.append(np.arccos(vec[2]/rho[-1]))
        # print(f"{len(all_vec)}: {vec} : {rho[-1]}, {theta[-1]}, {phi[-1]}")

    return rho, theta, phi

def extend_theta(theta_old):
    theta_new = []
    theta_new = theta_new + theta_old
    for theta in theta_old:
        c = np.exp(1j * theta)
        c = -np.real(c) + np.imag(c)*1j
        theta_new.append(np.angle(c))
    return theta_new

def plot_ILambda(theta_dir, phi_dir, tau_dir, res_dir, show=True):
    all_vec = read_directions(theta_dir, phi_dir, tau_dir, res_dir)
    all_ILambdas = read_ILambdas(theta_dir, phi_dir, tau_dir, res_dir)
    [rho, thetas, phi] = vec_to_theta(all_vec)
    clip = theta_dir*4
    thetas = thetas[:clip]
    analytical_I = []
    analytical_G = []
    for t in thetas:
        analytical_I.append(modest_I(tau_dir, t))
        analytical_G.append(modest_G(tau_dir,t))
    thetas = extend_theta(thetas)
    analytical_I = analytical_I + analytical_I[::-1]
    # divide by I_b = sigma*(T**4)
    all_ILambdas = all_ILambdas/I_b
    if show:
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)
        # theta = theta + list(np.array(thetas) + thetas[-1])
        # analytical_I = analytical_I + analytical_I[::-1]
        c1 = ax.scatter(thetas, analytical_I, label='Set 1', s=1)
        c1 = ax.scatter(thetas, all_ILambdas, label='Set 2')
        ax.set_thetamin(0)
        ax.set_thetamax(180)
        # Add a legend
        ax.legend()
        plt.show()
    
    return thetas, analytical_I, all_ILambdas[:clip*2], analytical_G

def plot_all_ILambda(lst_theta, lst_phi, lst_tau, lst_refining):
    fig = plt.figure()
    ax = fig.add_subplot(111, polar=True)
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                [thetas, analytical_I, all_ILambdas, analytical_G] = plot_ILambda(theta, phi, tau, res, show=False)
                # for i in range(len(all_ILambdas)):
                    # print(f"{theta}, {thetas[i]*180/np.pi}, {all_ILambdas[i]} : {analytical_I[i]}")
                # print(f"{len(thetas)} : {theta} : {len(all_ILambdas)}")
                
                # ax.scatter(thetas, analytical_I, label=f'a{theta},{tau},{res}', s=10, alpha=0.75)
                # ax.plot(thetas, all_ILambdas, "-*", label=f'n{theta},{tau},{res}')
                ax.plot(thetas, analytical_I, "--.", label=f'a{theta},{tau},{res}')
    ax.legend()
    # plt.savefig("plot_I_model", dpi=300)
    plt.show()

def plot_all_G(lst_theta, lst_phi, lst_tau, lst_refining):
    for theta,phi in zip(lst_theta, lst_phi):
        for tau in lst_tau:
            for res in lst_refining:
                [z_by_L, G_by_Ib] = plot_G(theta,phi,tau,res,show=False)
                plt.plot(z_by_L, G_by_Ib, label=f"{theta},{tau},{res}")
    plt.legend()
    plt.xlabel("z/L")
    plt.ylabel(r"$G/(4 \pi \cdot I_b)$")
    plt.grid()
    plt.savefig("plot_G", dpi=300)
    plt.show()
        
def plot_G(theta_dir, phi_dir, tau_dir, res_dir, show=True):
    file_name = f"Line_th_{theta_dir}-ph_{phi_dir}-tau_{tau_dir}-res_{res_dir}.csv"
    path = os.path.join(os.getcwd(),"DATA","all_data_linesample_RAD",file_name)
    df = pd.read_csv(path)
    # print(df.z + 0.6)
    # z_by_L = df.z + 0.6/LENGTH
    # z_by_L = (df.z + LENGTH/2)/LENGTH
    z_by_L = (df.z/LENGTH) + 0.5
    G_by_Ib = df.G/(4*pi*I_b)
    plt.plot(z_by_L, G_by_Ib)
    # print(df.G)
    if show:
        plt.grid()
        plt.show()
        
    return z_by_L, G_by_Ib

def plot_analytical_G(tau,theta):
    all_vec = read_directions()
    plt.plot(theta, modest_G(tau,theta))
    plt.show()



def modest_I(tau, theta):
    return 1 - (np.e)**((-tau)/np.cos(theta))

def modest_G(tau, theta):
    fn = lambda tau,theta : 1 - np.e**(-tau/np.cos(theta))
    return integrate.quad(fn, np.pi/2, 0,  args=tau)[0] # w.r.t theta






if __name__ == "__main__":

	print(os.getcwd())
