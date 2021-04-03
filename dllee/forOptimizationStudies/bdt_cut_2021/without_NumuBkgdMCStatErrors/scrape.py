import subprocess

autodir = "auto"
outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

#cut_variables = [ "dllee_bdt_score_median", "dllee_bdt_score_avg" ]
cut_variables = [ "dllee_bdt_score_avg" ]
#cut_values = [ 0.95, 0.9, 0.85, 0.8 ]
#cut_values = [ 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975 ]
#cut_values.extend( [ 0.98, 0.985, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999 ] )
cut_values = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 0.975 ]

with open("%s/opt.txt" % outdir, "w") as out:

    for var in cut_variables:
        for val in cut_values:

            tag = "opt-{}-{:03d}".format( var.split('_')[-1], int(val*1000.) )
            input_file = "log_%s.txt" % tag
            
            with open("%s/%s" % (autodir, input_file), "r") as this_in:
                for l in this_in:
                    if "Median" not in l: continue
                    alpha = float(l.split()[-4].split('(')[-1])
                    sigma = float(l.split()[-2].split('#')[0])
                    #print alpha, sigma
                    
            if True:
                out.write( "%s,%s,%s,%s\n" % (var, val, alpha, sigma) )

print "Done!"
