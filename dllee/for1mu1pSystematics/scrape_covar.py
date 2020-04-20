import subprocess
from ROOT import TFile


outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = [ "x_reco", "y_reco", "z_reco",
             "nu_energy_reco",
             "openang_reco",
             "pT_reco", "alphaT_reco",
             "Bjx_reco", "Bjy_reco",
             "Q2_reco","Q0_reco", "Q3_reco",
             "lepton_theta_reco", "lepton_phi_reco", "lepton_length_reco", "lepton_KE_reco",
             "proton_theta_reco", "proton_phi_reco", "proton_length_reco", "proton_KE_reco",
             "pT_ratio_reco" ]

#for sel in ["presel", "postsel"]:
for sel in ["postsel"]:
    #for plot_set in ["set1", "set2", "set3"]:
    for var in var_list:
        
        tag = "%s__%s" % (sel, var)
        input_file = "auto/%s.SBNcovar.root" % tag
        
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_covariance")
        
        with open("%s/covar_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(',')
                out.write('\n')

print "Done!"
