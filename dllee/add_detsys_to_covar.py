import sys
from ROOT import TFile,TMatrixD

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

# Specify detsys covariance matrix
# ... just doing flat, uncorrelated 10% for everything for now (note: 0.01 = (10%)^2)
detsys_entry = 0.01

# Add detsys to reweightable covariance matrix
# ... skipping EXT BNB contribution to 1mu1p, which is the last sub-channel
output_file = "%s_withDetSys.SBNcovar.root" % tag
output_f = TFile(output_file, "RECREATE")
covar = TMatrixD(rewght_covar)
numu_spec = spec_input_f.Get("nu_uBooNE_1mu1p_extbnb")
for i in range(covar.GetNrows()-numu_spec.GetNbinsX()):
    covar[i][i] += detsys_entry

if False:
    for i in range(covar.GetNrows()):
        for j in range(covar.GetNrows()):
            print i, j, rewght_covar[i][j], covar[i][j], covar[i][j]-rewght_covar[i][j]

covar.Write("frac_covariance")
output_f.Write()
output_f.Close()

print "Done!"
