import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir,"auto")
pdir = os.path.join(topdir,"persistent")

scale_list = [ 0.02*i for i in range(101) ]

for scale in scale_list:

    tag = "{:03d}".format(int(scale*100))
    thisdir = os.path.join(autodir,tag)
    os.chdir(thisdir)

    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_calculate_chi --xml sens.xml --tag fakedata -s sens.SBNspec.root "
    cmd += "-b %s " % os.path.join(pdir, "leeless.SBNspec.root")
    cmd += "-c total_sens.SBNcovar.root "
    cmd += "-d %s " % os.path.join(pdir, "fakedata.SBNspec.root")
    cmd += "> log_fakedata.txt"
    print cmd
    subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
