import os,subprocess

autodir = "auto"
topdir = os.getcwd()

var_list = [ "pi0_mass_reco", "Delta_mass_reco" ]

os.chdir(autodir)

for sel in ["postsel"]:
    for var in var_list:
        tag = "%s__%s" % (sel, var)
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
