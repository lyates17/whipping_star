import subprocess
from ROOT import TFile
import math

sel = "sideband"
k = 0

tag = "var00"
input_file = "%s.SBNcovar.root" % tag
        
input_f = TFile(input_file, "READ")
covar = input_f.Get("collapsed_frac_covariance")

with open("frac_covar_%s.txt" % (tag), "w") as out:
    for i in range(covar.GetNrows()):
        for j in range(covar.GetNcols()):
            out.write( str(covar[i][j]) )
            if j != range(covar.GetNcols())[-1]: out.write(' ')
        out.write('\n')
        
with open("frac_errors_%s.txt" % (tag), "w") as out:
    for i in range(covar.GetNrows()):
        out.write( str(math.sqrt(covar[i][i])) )
        if i != range(covar.GetNcols())[-1]: out.write(' ')
    out.write('\n')

print "Done!"
