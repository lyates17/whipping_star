import subprocess
from ROOT import TFile
import math

outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = [ "proton_score", "eminus_score", "gamma_score", "muon_score", "pion_score" ]

#for sel in ["presel", "postsel"]:
for sel in ["postsel"]:
    #for plot_set in ["set1", "set2", "set3"]:
    for var in var_list:
        
        tag = "%s__%s" % (sel, var)
        input_file = "auto/%s.SBNcovar.root" % tag
        
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_covariance")
        
        with open("%s/covar_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(',')
                out.write('\n')

        with open("%s/errors_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                out.write( str(math.sqrt(covar[i][i])) )
                if i != range(covar.GetNcols())[-1]: out.write(',')
            out.write('\n')


print "Done!"
