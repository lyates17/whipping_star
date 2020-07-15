import os,subprocess

autodir = "auto"
topdir = os.getcwd()

var_list = [ "x_reco", "y_reco", "z_reco",
             "openang_reco", "sum_thetas_reco", "sum_phis_reco",
             "charge_near_trunk_reco",
             "nu_energy_reco",
             "phiT_reco", "alphaT_reco", "pT_reco", "pT_ratio_reco",
             "Bjx_reco", "Bjy_reco", "BjxB_reco", "BjyB_reco",
             "Q2_reco", "sph_reco", "Q0_reco", "Q3_reco", "sphB_reco",
             "lepton_theta_reco", "lepton_phi_reco", "lepton_length_reco", "lepton_KE_reco", "lepton_cos_theta_reco",
             "proton_theta_reco", "proton_phi_reco", "proton_length_reco", "proton_KE_reco", "proton_cos_theta_reco" ]

os.chdir(autodir)

for sel in ["sel"]:
    for var in var_list:
        tag = "%s__%s" % (sel, var)
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
