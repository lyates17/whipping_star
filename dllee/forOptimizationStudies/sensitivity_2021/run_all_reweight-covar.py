import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir, "auto")

sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg" ] #, "dllee_bdt_score_median" ]
sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
sel1e1p_mpidp_cut_values = [ 0.0 ] #, 0.2 ]

os.chdir(autodir)


for var_e in sel1e1p_bdt_cut_variables:
    for val_p in sel1e1p_mpidp_cut_values:
        for val_e in sel1e1p_bdt_cut_values:
            for val_m in sel1mu1p_bdt_cut_values:
                
                tag = "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100.), int(val_p*100), int(val_m*100) )
                # make the reweightable sys covariance matrix
                cmd = "$SBNFIT_LIBDIR/bin/sbnfit_make_covariance --xml %s.xml --tag sens_%s" % (tag, tag)
                print cmd
                subprocess.call(cmd, shell=True)
                # make the leeless spectrum
                cmd = "$SBNFIT_LIBDIR/bin/sbnfit_scale_spec --xml %s.xml -i sens_%s.SBNspec.root -s lee -v 0.0 --tag leeless_%s" % (tag, tag, tag)
                print cmd
                subprocess.call(cmd, shell=True)
                # run the next steps in a separate script...

os.chdir(topdir)

print "Done!"
