import os,subprocess

autodir = "auto3"
topdir = os.getcwd()

#cut_values = [ 0.5, 0.6, 0.7, 0.8, 0.9 ]
cut_values = [ 0.5+0.01*i for i in range(50) ]

os.chdir(autodir)

for i in range(len(cut_values)):
    tag = "%s" % ("opt{:02d}".format( int(cut_values[i]*100.) ))
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
