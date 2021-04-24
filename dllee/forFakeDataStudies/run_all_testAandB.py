import os,subprocess

topdir = os.getcwd()

fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]

for tag in fakedata_list:

    workdir = os.path.join(topdir, tag)
    os.chdir(workdir)
    
    # run the frequentist study for tests A and B
    cmd = "$SBNFIT_LIBDIR/bin/sbnfit_lee_frequentist_study_withData "
    cmd += "--xml dllee_sens_pred_1e1p-only_{}.xml --tag testAandB ".format(tag)
    cmd += "-b h0_constr.SBNspec.root -s h1_constr.SBNspec.root -c h1_constr.SBNcovar.root -d data_1e1p-only.SBNspec.root "
    cmd += "-e 1e-11 > log_testAandB.txt".format(tag)
    print cmd
    subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
