import subprocess
from ROOT import TFile

autodir = "auto"
outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

cut_values = [ 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9 ]

with open("%s/opt.txt" % outdir, "w") as out:
    for i in range(len(cut_values)):
    
        tag = "%s" % ("opt{:02d}".format( int(cut_values[i]*100.) ))
        input_file = "log_%s.txt" % tag
        
        with open("%s/%s" % (autodir, input_file), "r") as this_in:
            for l in this_in:
                if "Median" not in l: continue
                alpha = float(l.split()[-4].split('(')[-1])
                sigma = float(l.split()[-2].split('#')[0])
                #print alpha, sigma
        
        out.write( "%s,%s,%s\n" % (cut_values[i], alpha, sigma) )

print "Done!"
