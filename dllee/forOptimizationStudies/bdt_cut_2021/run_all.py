import os,subprocess

autodir = "auto"
topdir = os.getcwd()

cut_variables = [ "dllee_bdt_score_median", "dllee_bdt_score_avg" ]
#cut_values = [ 0.95, 0.9, 0.85, 0.8 ]
#cut_values = [ 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975 ]
cut_values = [ 0.98, 0.985, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999 ]

os.chdir(autodir)

for var in cut_variables:
    for val in cut_values:

        tag = "opt-{}-{:03d}".format( var.split('_')[-1], int(val*1000.) )
        # make the covariance matrix
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_make_covariance --xml %s.xml --tag sens_%s" % (tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)
        # make the leeless spectrum
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_scale_spec --xml %s.xml -i sens_%s.SBNspec.root -s lee -v 0.0 --tag leeless_%s" % (tag, tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)
        # run the frequentist study for sensitivity
        cmd = "/uboone/app/users/yatesla/sbnfit/whipping_star/build/bin/sbnfit_lee_frequentist_study "
        cmd += "--xml %s.xml --tag sens_%s_ -b leeless_%s.SBNspec.root -s sens_%s.SBNspec.root -c sens_%s.SBNcovar.root -e 1e-11 > log_%s.txt" % (tag, tag, tag, tag, tag, tag)
        print cmd
        subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
