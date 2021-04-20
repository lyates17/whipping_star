import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir,"auto")
pdir = os.path.join(topdir,"persistent")

scale_list = [ 0.02*i for i in range(101) ]

for scale in scale_list:

    tag = "{:03d}".format(int(scale*100))
    thisdir = os.path.join(autodir,tag)
    os.chdir(thisdir)

    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml sens.xml --tag sens"
    print cmd
    subprocess.call(cmd, shell=True)

    cmd = "cp %s ." % os.path.join(pdir, "make_total_sens_covar.py")
    subprocess.call(cmd, shell=True)
    cmd = "python make_total_sens_covar.py"
    print cmd
    subprocess.call(cmd, shell=True)

    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_complete_covariance --xml sens.xml --tag total_sens -s sens.SBNspec.root -c total_sens.SBNcovar.root"
    print cmd
    subprocess.call(cmd, shell=True)

    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_lee_frequentist_study --xml sens.xml --tag sens -s sens.SBNspec.root "
    cmd += "-b %s " % os.path.join(pdir, "leeless.SBNspec.root")
    cmd += "-c total_sens.SBNcovar.root -n 10000 > log.txt"
    print cmd
    subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
