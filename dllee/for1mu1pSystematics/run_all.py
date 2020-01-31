import os,subprocess

autodir = "auto"
topdir = os.getcwd()

var_list = [ "x_reco", "y_reco", "z_reco",
             "nu_energy_reco",
             "openang_reco",
             "pT_reco", "alphaT_reco",
             "Bjx_reco", "Bjy_reco",
             "Q2_reco","Q0_reco", "Q3_reco",
             "lepton_theta_reco", "lepton_phi_reco", "lepton_length_reco", "lepton_KE_reco",
             "proton_theta_reco", "proton_phi_reco", "proton_length_reco", "proton_KE_reco",
             "pT_ratio_reco" ]

os.chdir(autodir)

#for sel in ["presel", "postsel"]:
for sel in ["postsel"]:
    for plot_set in ["set1", "set2", "set3"]:
        for var in var_list:
            tag = "%s_%s__%s" % (sel, plot_set, var)
            cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
            print cmd
            subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
