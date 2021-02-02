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

# Get info on matrix from spec file
spec_keys = [ key.GetName() for key in spec_input_f.GetListOfKeys() ]
if (("nu_uBooNE_1e1p_nue" not in spec_keys) or ("nu_uBooNE_1mu1p_bnb" not in spec_keys)):
    print "Input spec file %s has some non-standard naming... Don't know what to do here!" % spec_input_file
    print "Exiting..."
    sys.exit(2)
N_1e1p_bins = spec_input_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()
N_1m1p_bins = spec_input_f.Get("nu_uBooNE_1mu1p_bnb").GetNbinsX()
N_1e1p_subchannels = 0
N_1m1p_subchannels = 0
for k in spec_keys:
    if k.split('_')[2] == '1e1p': N_1e1p_subchannels += 1
    elif k.split('_')[2] == '1mu1p': N_1m1p_subchannels += 1
    else:
        print "Spectra %s in input spec file has some non-standard naming... Don't know what to do here!" % k
        print "Exiting..."
        sys.exit(3)
if True:
    print "Number of 1e1p bins: %s" % N_1e1p_bins
    print "Number of 1e1p subchannels: %s" % N_1e1p_subchannels
    print "Number of 1mu1p bins: %s" % N_1m1p_bins
    print "Number of 1mu1p subchannels: %s" % N_1m1p_subchannels
# Fake data has no EXT on the numu, so just add one here...
N_1m1p_subchannels += 1
    

# Specify detsys covariance matrix
# ... just doing flat, uncorrelated 10% for everything for now (note: 0.01 = (10%)^2)
# TODO: update this to do different systematics for intrinsics vs. bnb backgrounds vs. extbnb backgrounds vs. LEE, etc.
#       or maybe we just need to do two versions of this, one for SM-only and one for SM+LEE...
sel1e1p_entries = [ 0.01 for i in range(N_1e1p_bins*N_1e1p_subchannels) ]
sel1m1p_entries = [ 0.01 for i in range(N_1m1p_bins*(N_1m1p_subchannels-1))]  # skip last 1mu1p subchannel, which is EXTBNB and therefore has no detsys

# Add detsys to reweightable covariance matrix
output_file = "total_%s.SBNcovar.root" % tag
output_f = TFile(output_file, "RECREATE")
covar = TMatrixD(rewght_covar)
for i in range(covar.GetNrows()):
    if (i<N_1e1p_bins*N_1e1p_subchannels): covar[i][i] += sel1e1p_entries[i]
    if ( (i>=N_1e1p_bins*N_1e1p_subchannels) and (i<N_1e1p_bins*N_1e1p_subchannels+N_1m1p_bins*(N_1m1p_subchannels-1)) ): covar[i][i] += sel1m1p_entries[i-N_1e1p_bins*N_1e1p_subchannels]

if True:
    for i in range(covar.GetNrows()):
        for j in range(covar.GetNrows()):
            print i, j, rewght_covar[i][j], covar[i][j], covar[i][j]-rewght_covar[i][j]

covar.Write("frac_covariance")
output_f.Write()
output_f.Close()

print "Done!"
