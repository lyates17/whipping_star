import os,subprocess

autodir = "auto"
topdir = os.getcwd()

N_var = 31 

os.chdir(autodir)

for sel in ["opendata", "sideband"]:
    for i in range(N_var):
        tag = "%s__%s" % (sel, "var{:02d}".format(i))
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag %s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
