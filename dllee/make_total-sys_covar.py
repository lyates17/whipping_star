import os,subprocess
import math
import ROOT

# Declare file names for input files
topdir = os.getcwd()
in_h0_spec_fname = os.path.join(topdir, "leeless.SBNspec.root")
in_h1_spec_fname = os.path.join(topdir, "sens.SBNspec.root")
in_covar_fname   = os.path.join(topdir, "sens.SBNcovar.root")
detsys_fname     = os.path.join(topdir, "detsys", "covMat_Tot.csv")

# Define a few helper variables...
#   Note: Making some assumptions about the xml configuration
Nbins_e = 10
Nbins_m = 19
#offset_1e1p_nue = 0
offset_1e1p_bnb = Nbins_e 
offset_1e1p_lee = 2*Nbins_e
offset_1mu1p    = 3*Nbins_e


# Open the input SBNfit file
in_covar_f   = ROOT.TFile.Open(in_covar_fname, "READ")

# Declare file names for output file
out_covar_fname   = in_covar_fname.replace(".SBNcovar.root", "_total-sys.SBNcovar.root")

# Create the output file
out_covar_f   = ROOT.TFile(out_covar_fname, "RECREATE")

# Initialize the output covariance matrix as a copy of the input
out_covar = ROOT.TMatrixD( in_covar_f.Get("frac_covariance") )
# Zero out any nans, so that things we add actually get added
for i in range(out_covar.GetNrows()):
    for j in range(out_covar.GetNcols()):
        if math.isnan(out_covar[i][j]):
            out_covar[i][j] = 0.

# Add detector systematics for 1e1p nue, 1e1p lee, and 1mu1p bnb... 
# Read in fractional detector systematic covariance matrix from csv file
#   Note: Covariance matrix in this file has dimension 20+12
#           20 1mu1p bins from 200 to 1200 MeV in  50 MeV bins, then
#           12 1e1p  bins from   0 to 1200 MeV in 100 MeV bins
print "Adding detector systematics from {}".format(detsys_fname)
detsys_covar = []
with open(detsys_fname, 'r') as f:
    for l in f:
        detsys_covar.append( [ float(x) for x in l.strip().split(',') ] )
# Break this out into block matrices with correct dimensions
#   Note: We only use the 19 1mu1p bins from 250 to 1200 MeV, so add 1 to the offset
#   Note: We only use the 10 1e1p  bins from 200 to 1200 MeV, so add 2 to the offset
in_offset_m = 1
in_offset_e = in_offset_m + Nbins_m + 2
detsys_covar_ee = []
for i in range(Nbins_e):
    detsys_covar_ee.append( [] )
    for j in range(Nbins_e):
        detsys_covar_ee[i].append( detsys_covar[in_offset_e+i][in_offset_e+j] )
detsys_covar_em = []
for i in range(Nbins_e):
    detsys_covar_em.append( [] )
    for j in range(Nbins_m):
        detsys_covar_em[i].append( detsys_covar[in_offset_e+i][in_offset_m+j] )
detsys_covar_mm = []
for i in range(Nbins_m):
    detsys_covar_mm.append( [] )
    for j in range(Nbins_m):
        detsys_covar_mm[i].append( detsys_covar[in_offset_m+i][in_offset_m+j] )
# Add detsys_covar_ee to the 1e1p nue and lee
for i in range(Nbins_e):
    for j in range(Nbins_e):
        out_covar[i][j] += detsys_covar_ee[i][j]
        out_covar[i][offset_1e1p_lee+j] += detsys_covar_ee[i][j]
        out_covar[offset_1e1p_lee+i][j] += detsys_covar_ee[i][j]
        out_covar[offset_1e1p_lee+i][offset_1e1p_lee+j] += detsys_covar_ee[i][j]
# Add detsys_covar_em to the block off-diagonals between {1e1p nue, 1e1p lee}x{1mu1p bnb}
for i in range(Nbins_e):
    for j in range(Nbins_m):
        out_covar[i][offset_1mu1p+j] += detsys_covar_em[i][j]
        out_covar[offset_1mu1p+j][i] += detsys_covar_em[i][j]
        out_covar[offset_1e1p_lee+i][offset_1mu1p+j] += detsys_covar_em[i][j]
        out_covar[offset_1mu1p+j][offset_1e1p_lee+i] += detsys_covar_em[i][j]
# Add detsys_covar_mm to the 1mu1p bnb
for i in range(Nbins_m):
    for j in range(Nbins_m):
        out_covar[offset_1mu1p+i][offset_1mu1p+j] += detsys_covar_mm[i][j]
# ... done adding detector systematics for 1e1p nue, 1e1p lee, and 1mu1p bnb

                
# Add detector systematics for 1e1p bnb (i.e., numu backgrounds to the 1e1p selection)...
detsys_bkg = 0.20**2  # settled on 20%, see Slack DM with Nick at 9:34 on April 5
print "Adding detector systematics for numu backgrounds to the 1e1p ({:.3f})".format(detsys_bkg)
for i in range(Nbins_e):
    out_covar[offset_1e1p_bnb+i][offset_1e1p_bnb+i] += detsys_bkg
# ... done adding detector systeamtics for 1e1p bnb
                
                
# Write everything out
out_covar_f.WriteTObject(out_covar, "frac_covariance")
# Close the outputs
out_covar_f.Close()
# Close the inputs
in_covar_f.Close()

print "Done!"
