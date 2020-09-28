import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir,"auto")
pdir = os.path.join(topdir,"persistent")
# Main xml, SM+1*LEE spectrum, and SM+1*LEE covariance matrix
pxml = os.path.join(pdir,"dllee_sens_pred_set4.xml")
pspec = os.path.join(pdir,"sens_pred.SBNspec.root")
pcovar = os.path.join(pdir,"total_sens_pred.SBNcovar.root")

scale_list = [ 0.01*i for i in range(501) ]
#scale_list = [ 0., 1., 2., 3., 4., 5. ]


for scale in scale_list:

    tag = "{:03d}".format(int(scale*100))
    thisdir = os.path.join(autodir,tag)
    subprocess.call("mkdir -p %s" % thisdir, shell=True)
    os.chdir(thisdir)

    # Scale the spectrum
    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_scale_spec "
    cmd += "--xml %s " % pxml
    cmd += "-i %s " % pspec
    cmd += "-s lee -v %s -t sens" % scale
    print cmd
    subprocess.call(cmd, shell=True)

    # Build the covariance matrices with the scaled spectra
    cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_complete_covariance "
    cmd += "--xml %s " % pxml
    cmd += "--tag total_sens "
    cmd += "-s sens.SBNspec.root "  # feed in the scaled spectrum from above
    cmd += "-c %s" % pcovar
    print cmd
    subprocess.call(cmd, shell=True)

    #cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_lee_frequentist_study --xml sens.xml --tag sens -s sens.SBNspec.root "
    #cmd += "-b %s " % os.path.join(pdir, "leeless.SBNspec.root")
    #cmd += "-c total_sens.SBNcovar.root -n 10000 > log.txt"
    #print cmd
    #subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
