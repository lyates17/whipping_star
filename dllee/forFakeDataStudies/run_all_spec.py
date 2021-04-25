import os,subprocess

topdir = os.getcwd()

fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]

for tag in fakedata_list:

    workdir = os.path.join(topdir, tag)
    os.chdir(workdir)
    
    # make the main spectrum
    cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_spec --xml dllee_sens_pred_{}.xml --tag h1".format(tag)
    print cmd
    subprocess.call(cmd, shell=True)
    cmd = "mv h1_CV.SBNspec.root h1.SBNspec.root"
    print cmd
    subprocess.call(cmd, shell=True)
    # make the leeless spectrum
    cmd = "$SBNFIT_LIBDIR/bin/sbnfit_scale_spec --xml dllee_sens_pred_{}.xml -i h1.SBNspec.root -s lee -v 0.0 --tag h0".format(tag)
    print cmd
    subprocess.call(cmd, shell=True)
    # make the data spectrum
    cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_spec --xml dllee_sens_fakedata_{}.xml --tag data".format(tag)
    print cmd
    subprocess.call(cmd, shell=True)
    cmd = "mv data_CV.SBNspec.root data.SBNspec.root"
    print cmd
    subprocess.call(cmd, shell=True)
    # make the 1e1p-only data spectrum
    cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_spec --xml dllee_sens_fakedata_1e1p-only_{}.xml --tag data_1e1p-only".format(tag)
    print cmd
    subprocess.call(cmd, shell=True)
    cmd = "mv data_1e1p-only_CV.SBNspec.root data_1e1p-only.SBNspec.root"
    print cmd
    subprocess.call(cmd, shell=True)
    
    # if not set5...
    if tag!='set5':
        # make the truth spectrum for plots (nue, bnb, lee)
        cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_spec --xml dllee_sens_pred_truth_{}.xml --tag true".format(tag)
        print cmd
        subprocess.call(cmd, shell=True)
        cmd = "mv true_CV.SBNspec.root true.SBNspec.root"
        print cmd
        subprocess.call(cmd, shell=True)
        # make the truth spectrum for tables (nueCCQE, nueOther, numuCCQE, etc.)
        cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_spec --xml dllee_sens_pred_truth2_{}.xml --tag true2".format(tag)
        print cmd
        subprocess.call(cmd, shell=True)
        cmd = "mv true2_CV.SBNspec.root true2.SBNspec.root"
        print cmd
        subprocess.call(cmd, shell=True)
    
    # run the next steps in a separate script...
    
os.chdir(topdir)

print "Done!"
