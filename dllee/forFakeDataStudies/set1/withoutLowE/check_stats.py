import ROOT
from math import sqrt

run1_fname = "/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run1_Jul15.root"
run3_fname = "/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run3_Jul15.root"

run1_dict = { "fname": run1_fname, "nue_scale": 0.00201, "nue_lowE_scale": 0.000458, "bnb_scale": 0.418 }
run3_dict = { "fname": run3_fname, "nue_scale": 0.00608, "nue_lowE_scale": 0.000665, "bnb_scale": 0.318 }
master_dict = { "run1": run1_dict, "run3": run3_dict }

#input_file = ROOT.TFile.Open(input_fname)
#nue_tree = input_file.Get("sel_nue_tree")
#nue_tree.SetBranchStatus("sys_weights",0)
#nue_tree.GetEntry(0)

for key in master_dict:

    print key

    # Reset values
    N_nue = 0.
    sigma_nue = 0.
    N_lowE = 0.
    sigma_lowE = 0.

    # Get the run-dependent information
    run_dict = master_dict[key]
    
    # Open the input file
    input_fname = run_dict["fname"]
    input_file  = ROOT.TFile.Open(input_fname)
    
    # Loop over the nue tree
    nue_tree = input_file.Get("sel_nue_tree")
    nue_tree.SetBranchStatus("sys_weights",0)
    for entry in nue_tree:
        if entry.nu_energy_true > 400: continue
        weight = entry.xsec_corr_weight * entry.lee_weight * run_dict["nue_scale"]
        N_nue += weight
        sigma_nue += weight*weight
    sigma_nue = sqrt(sigma_nue)
    run_dict["N_nue"] = N_nue
    run_dict["sigma_nue"] = sigma_nue
    print N_nue, sigma_nue

    # Loop over the lowE tree
    lowE_tree = input_file.Get("sel_nue_lowE_tree")
    lowE_tree.SetBranchStatus("sys_weights",0)
    for entry in lowE_tree:
        if entry.nu_energy_true > 400: continue
        weight = entry.xsec_corr_weight * entry.lee_weight * run_dict["nue_lowE_scale"]
        N_lowE += weight
        sigma_lowE += weight*weight
    sigma_lowE = sqrt(sigma_lowE)
    run_dict["N_lowE"] = N_lowE
    run_dict["sigma_lowE"] = sigma_lowE
    print N_lowE, sigma_lowE

print "total"
N_nue_tot = 0.
sigma_nue_tot = 0.
N_lowE_tot = 0.
sigma_lowE_tot = 0.
for key in master_dict:
    N_nue_tot += master_dict[key]["N_nue"]
    sigma_nue_tot += master_dict[key]["sigma_nue"]*master_dict[key]["sigma_nue"]
    N_lowE_tot += master_dict[key]["N_lowE"]
    sigma_lowE_tot += master_dict[key]["sigma_lowE"]*master_dict[key]["sigma_lowE"]
sigma_nue_tot = sqrt(sigma_nue_tot)
sigma_lowE_tot = sqrt(sigma_lowE_tot)
print N_nue_tot, sigma_nue_tot
print N_lowE_tot, sigma_lowE_tot
if ( abs(N_lowE_tot-N_nue_tot) > sigma_nue_tot ): print "Warning: These are *not* statistically consistent!"
else: print "These are statistically consistent"

print "Done!"
