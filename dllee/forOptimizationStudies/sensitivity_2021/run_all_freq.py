import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir, "auto")

sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg", "dllee_bdt_score_median" ]
sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
sel1e1p_mpidp_cut_values = [ 0.0, 0.2 ]

os.chdir(autodir)


for var_e in sel1e1p_bdt_cut_variables:
    for val_p in sel1e1p_mpidp_cut_values:
        for val_e in sel1e1p_bdt_cut_values:
            for val_m in sel1mu1p_bdt_cut_values:

                tag = "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100.), int(val_p*100), int(val_m*100) )

                # run the frequentist study for sensitivity
                cmd = "$SBNFIT_LIBDIR/bin/sbnfit_lee_frequentist_study "
                cmd += "--xml {}_constr.xml --tag sens_{}_constr_ -b leeless_{}_constr.SBNspec.root -s sens_{}_constr.SBNspec.root -c sens_{}_constr.SBNcovar.root -e 1e-11 > log_{}.txt".format(tag, tag, tag, tag, tag, tag)
                print cmd
                subprocess.call(cmd, shell=True)

os.chdir(topdir)

print "Done!"
