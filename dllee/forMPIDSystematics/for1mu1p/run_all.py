import os,subprocess

autodir = "auto"
topdir = os.getcwd()

var_list = [ "proton_score", "eminus_score", "gamma_score", "muon_score", "pion_score" ]

os.chdir(autodir)

#for sel in ["presel", "postsel"]:
for sel in ["postsel"]:
    #for plot_set in ["set1", "set2", "set3"]:
    for var in var_list:
        tag = "%s__%s" % (sel, var)
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
