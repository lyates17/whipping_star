import subprocess
from ROOT import TFile


outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = [ "pi0_mass_reco", "Delta_mass_reco" ]

for sel in ["postsel"]:
    for var in var_list:
        
        tag = "%s__%s" % (sel, var)
        input_file = "auto/%s.SBNcovar.root" % tag
        
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_frac_covariance")
        
        with open("%s/covar_%s.txt" % (outdir, tag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(',')
                out.write('\n')

print "Done!"
