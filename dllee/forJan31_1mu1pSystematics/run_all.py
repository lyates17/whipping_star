import subprocess

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
    for plot_set in ["set1", "set2", "set3"]:
        for var in var_list:

            tag = "%s_%s-%s" % (sel, plot_set, var)
            cmd = "../../build/bin/sbnfit_make_covariance --xml auto_%s.xml --tag %s" % (tag, tag)
            print cmd
            
            subprocess.call(cmd, shell=True)

print "Done!"
