import subprocess
from ROOT import TFile
import math

outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

N_var = 31


for sel in ["BDTCut_Run3", "BDTCutPostCut_Run3"]:
#for sel in ["BDTCutPostCut_Run3"]:
    for k in range(N_var):
        
        tag = "%s__%s" % (sel, "var{:02d}".format(k))
        input_file = "auto/%s.SBNcovar.root" % tag
        
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_frac_covariance")

        with open("%s/frac_covar_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(' ')
                out.write('\n')
        
        with open("%s/frac_errors_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                out.write( str(math.sqrt(covar[i][i])) )
                if i != range(covar.GetNcols())[-1]: out.write(' ')
            out.write('\n')

print "Done!"
