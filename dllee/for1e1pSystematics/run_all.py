import os,subprocess

autodir = "auto"
topdir = os.getcwd()

var_list = [ 'nu_energy_reco', 'eta_reco', 'pT_reco', 'alphaT_reco', 'sphB_reco', 'pzEnu_reco', 'charge_near_trunk_reco', 'Q0_reco','Q3_reco', 'sum_thetas_reco','sum_phis_reco',
             'pT_ratio_reco', 'proton_theta_reco', 'proton_phi_reco', 'min_shr_frac_reco', 'max_shr_frac_reco', 'BjxB_reco', 'BjyB_reco', 'proton_KE_reco', 'lepton_KE_reco',
             'lepton_theta_reco', 'lepton_phi_reco', 'openang_reco', 'x_reco', 'y_reco', 'z_reco', 'bdt_score', 'mpid_muon_score', 'mpid_proton_score', 'mpid_electron_score' ]

os.chdir(autodir)

#for sel in ["highE", "final", "blind"]:
for sel in ["blind"]:
    for var in var_list:
        tag = "%s__%s" % (sel, var)
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
