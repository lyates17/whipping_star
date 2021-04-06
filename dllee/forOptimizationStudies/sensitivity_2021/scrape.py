import os,subprocess

topdir = os.getcwd()
autodir = os.path.join(topdir, "auto")
outdir  = os.path.join(topdir, "output")

subprocess.call("mkdir -p %s" % outdir, shell=True)

sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg" ] #, "dllee_bdt_score_median" ]
sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
sel1e1p_mpidp_cut_values = [ 0.0 ] #, 0.2 ]


with open("%s/opt.txt" % outdir, "w") as out:

    for var_e in sel1e1p_bdt_cut_variables:
        for val_e in sel1e1p_bdt_cut_values:
            for val_m in sel1mu1p_bdt_cut_values:
                for val_p in sel1e1p_mpidp_cut_values:

                    tag = "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100.), int(val_p*100), int(val_m*100) )
                    input_file = "log_{}.txt".format(tag)
                    
                    with open(os.path.join(autodir, input_file), "r") as this_in:
                        for l in this_in:
                            if "Median" not in l: continue
                            alpha = float(l.split()[-4].split('(')[-1])
                            sigma = float(l.split()[-2].split('#')[0])
                            #print alpha, sigma
                    
                    if True:
                        out.write( "{},{},{},{},{},{}\n".format(var_e, val_e, val_p, val_m, alpha, sigma) )

os.chdir(topdir)

print "Done!"
