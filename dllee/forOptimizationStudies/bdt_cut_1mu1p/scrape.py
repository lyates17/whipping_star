import subprocess

autodir = "auto"
outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

cut_values = [ 0.01*i for i in range(1,71) ]

with open("%s/opt.txt" % outdir, "w") as out:
    for cut in cut_values:
        
        tag = "opt{:02d}".format( int(cut*100.) )
        input_file = "log_%s.txt" % tag
        
        with open("%s/%s" % (autodir, input_file), "r") as this_in:
            for l in this_in:
                if "Median" not in l: continue
                alpha = float(l.split()[-4].split('(')[-1])
                sigma = float(l.split()[-2].split('#')[0])
                #print alpha, sigma
                    
        #if sigma >= 3.3:
        if tag[-1] == '0':
        #if True:
            out.write( "%s,%s,%s\n" % (cut, alpha, sigma) )

print "Done!"
