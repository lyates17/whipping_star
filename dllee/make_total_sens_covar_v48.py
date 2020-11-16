from ROOT import TFile,TMatrixD

# Get reweightable covariance matrix
tag = "sens_v48"
rewgt_input_file = "%s.SBNcovar.root" % tag
rewgt_input_f = TFile(rewgt_input_file, "READ")
rewght_covar = rewgt_input_f.Get("frac_covariance")

# Get detsys covariance matrix
# ... flat is the only thing that works for now...
#detsys_input_file = ""
sel1e1p_entry = 0.0003742756318718823
sel1m1p_entry = 0.008285363079390817
mixed_entry = -5.593215393234595e-05

# Add them together
N_1e1p_bins = 10
N_1e1p_subchannels = 3
N_1m1p_bins = 19
N_1m1p_subchannels = 2
output_file = "total_%s.SBNcovar.root" % tag
output_f = TFile(output_file, "RECREATE")
covar = TMatrixD(rewght_covar)
for i in range(covar.GetNrows()):
    for j in range(covar.GetNcols()):
        #covar[i][j] += detsys_covar[i][j]
        if ( (i<N_1e1p_bins) and (j<N_1e1p_bins) ): covar[i][j] += sel1e1p_entry
        if ( (i>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins)
             and (j>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins) ): covar[i][j] += sel1e1p_entry
        if ( (i<N_1e1p_bins) and (j>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins) ): covar[i][j] += sel1e1p_entry
        if ( (j<N_1e1p_bins) and (i>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins) ): covar[i][j] += sel1e1p_entry
        if ( (i>=N_1e1p_subchannels*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) 
             and (j>=N_1e1p_subchannels*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) ): covar[i][j] += sel1m1p_entry
        if ( (i<N_1e1p_bins) and (j>=N_1e1p_subchannels*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) ):  covar[i][j] += mixed_entry
        if ( (i>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins)
             and (j>=N_1e1p_subchannels*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) ): covar[i][j] += mixed_entry
        if ( (j<N_1e1p_bins) and (i>=N_1e1p_subchannels*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) ):  covar[i][j] += mixed_entry
        if ( (j>=(N_1e1p_subchannels-1)*N_1e1p_bins) and (j<N_1e1p_subchannels*N_1e1p_bins)
             and (i>=N_1e1p_subchannels*N_1e1p_bins) and (i<N_1e1p_subchannels*N_1e1p_bins+N_1m1p_bins) ): covar[i][j] += mixed_entry

for i in range(covar.GetNrows()):
    for j in range(covar.GetNrows()):
        #print i, j, rewght_covar[i][j], covar[i][j], covar[i][j]-rewght_covar[i][j]
        pass

covar.Write("frac_covariance")
output_f.Write()
output_f.Close()

print "Done!"
