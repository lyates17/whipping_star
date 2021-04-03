import sys
from ROOT import TFile,TMatrixD
from math import sqrt

# Get the tag
if len(sys.argv) != 2:
    print "Need input tag!"
    print "Usage: %s [input tag]" % sys.argv[0]
    print "Exiting..."
    sys.exit(1)
tag = sys.argv[1]

# Get the spectra, list of keys
spec_input_file = "%s.SBNspec.root" % tag
spec_input_f = TFile(spec_input_file, "READ")
# Get reweightable covariance matrix
rewgt_input_file = "%s.SBNcovar.root" % tag
rewgt_input_f = TFile(rewgt_input_file, "READ")
rewght_covar = rewgt_input_f.Get("frac_covariance")

# Read in detsys covariance matrix
detsys_list = [ "1e1p_run1", "1e1p_run3", "1m1p_run1", "1m1p_run3" ]
detsys_dict = {}
for sel in detsys_list:
    detsys_dict[sel] = []
    with open("detsys/detsys_Enu_%s_cov.csv" % sel) as f:
        for l in f:
            row = [ float(x) for x in l.strip().split(',') ]
            detsys_dict[sel].append(row)
#print detsys_dict["1e1p_run3"][0][0]
# Combine Runs 1+3 and reduce to diagonals for now
run1_scale = 0.256
run3_scale = 0.744
sel1e1p_detsys_entries = [ run1_scale*(detsys_dict["1e1p_run1"][i][i]) + (run3_scale*detsys_dict["1e1p_run3"][i][i]) for i in range(spec_input_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()) ]
sel1mu1p_detsys_entries = [ run1_scale*(detsys_dict["1m1p_run1"][i][i]) + (run3_scale*detsys_dict["1m1p_run3"][i][i]) for i in range(1+spec_input_f.Get("nu_uBooNE_1mu1p_bnb").GetNbinsX()) ]

# remove first row of 1mu1p
sel1mu1p_detsys_entries = sel1mu1p_detsys_entries[1:]

# Print out...
print "1e1p errors (%s bins) :" % len(sel1e1p_detsys_entries)
print [ sqrt(x) for x in sel1e1p_detsys_entries ]
print "1mu1p errors (%s bins):" % len(sel1mu1p_detsys_entries)
print [ sqrt(x) for x in sel1mu1p_detsys_entries ]

# Add detsys to reweightable covariance matrix
output_file = "%s_withDetSys.SBNcovar.root" % tag
output_f = TFile(output_file, "RECREATE")
covar = TMatrixD(rewght_covar)
N_1e1p_subchannels = 0
spec_keys = [ key.GetName() for key in spec_input_f.GetListOfKeys() ]
N_1e1p_bins = spec_input_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()
for k in spec_keys:
    if "1e1p" in k: N_1e1p_subchannels += 1
# Now actually add them
for i in range(spec_input_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()):
    covar[i][i] += sel1e1p_detsys_entries[i]
for i in range(spec_input_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()):
    covar[N_1e1p_bins+i][N_1e1p_bins+i] += 0.04
for i in range(spec_input_f.Get("nu_uBooNE_1mu1p_bnb").GetNbinsX()):
    #print i
    covar[N_1e1p_bins*N_1e1p_subchannels+i][N_1e1p_bins*N_1e1p_subchannels+i] += sel1mu1p_detsys_entries[i]

if True:
    for i in range(covar.GetNrows()):
        for j in range(covar.GetNrows()):
            if i!=j: continue
            print i, j, rewght_covar[i][j], covar[i][j], covar[i][j]-rewght_covar[i][j]

covar.Write("frac_covariance")
output_f.Write()
output_f.Close()

print "Done!"
