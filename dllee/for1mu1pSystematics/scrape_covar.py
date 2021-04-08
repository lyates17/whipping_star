import subprocess
from ROOT import TFile


outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = [ "x_reco", "y_reco", "z_reco",
             "openang_reco", "sum_thetas_reco", "sum_phis_reco",
             "charge_near_trunk_reco",
             "nu_energy_reco",
             "phiT_reco", "alphaT_reco", "pT_reco", "pT_ratio_reco",
             "BjxB_reco", "BjyB_reco",
             "Q2_reco", "Q0_reco", "Q3_reco", "sphB_reco",
             "lepton_theta_reco", "lepton_phi_reco", "lepton_length_reco", "lepton_KE_reco", "lepton_cos_theta_reco",
             "proton_theta_reco", "proton_phi_reco", "proton_length_reco", "proton_KE_reco", "proton_cos_theta_reco", 
             "mpid_electron_score", "mpid_muon_score", "mpid_proton_score", #"mpid_gamma_score", "mpid_pion_score",
             #"bdt_score" ]
             "dllee_bdt_score_avg" ]

#for sel in ["sel_total", "sel_run1", "sel_run2", "sel_run3"]:
#for sel in ["sel_total_withoutPi0Weights", "sel_total_withPi0Weights"]: 
for sel in ["sel_total_withPi0Weights"]: 
    for var in var_list:
        
        #if var != "bdt_score" and sel != "sel_total":
        #    continue

        tag = "%s__%s" % (sel, var)
        input_file = "auto/%s.SBNcovar.root" % tag
        
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_frac_covariance")
        
        with open("%s/frac_covar_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(',')
                out.write('\n')

print "Done!"
