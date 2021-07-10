import os,subprocess
import math
import ROOT

# Declare file names for input files
topdir = os.getcwd()
in_h0_spec_fname = os.path.join(topdir, "leeless_Runs1to5.SBNspec.root")
in_h1_spec_fname = os.path.join(topdir, "sens_Runs1to5.SBNspec.root")
in_covar_fname   = os.path.join(topdir, "sens_Runs1to5.SBNcovar.root")
detsys_fname     = os.path.join(topdir, "../detsys", "covMat_Tot.csv")
bkg_pred_fname   = os.path.join(topdir, "../bkg", "bkg_0.95_prediction.txt")
bkg_covar_fname  = os.path.join(topdir, "../bkg", "bkg_0.95_cov.txt")

# Define a few helper variables...
#   Note: Making some assumptions about the xml configuration
Nbins_e = 10
Nbins_m = 19
#offset_1e1p_nue = 0
offset_1e1p_bnb = Nbins_e 
offset_1e1p_lee = 2*Nbins_e
offset_1mu1p    = 3*Nbins_e


# Open the input SBNfit files
in_h0_spec_f = ROOT.TFile.Open(in_h0_spec_fname, "READ")
in_h1_spec_f = ROOT.TFile.Open(in_h1_spec_fname, "READ")
in_covar_f   = ROOT.TFile.Open(in_covar_fname, "READ")

# Declare file names for output files
out_h0_spec_fname = in_h0_spec_fname.replace(".SBNspec.root", "_total.SBNspec.root")
out_h1_spec_fname = in_h1_spec_fname.replace(".SBNspec.root", "_total.SBNspec.root")
out_covar_fname   = in_covar_fname.replace(".SBNcovar.root", "_total.SBNcovar.root")

# Create the output files
out_h0_spec_f = ROOT.TFile(out_h0_spec_fname, "RECREATE")
out_h1_spec_f = ROOT.TFile(out_h1_spec_fname, "RECREATE")
out_covar_f   = ROOT.TFile(out_covar_fname, "RECREATE")

# Initialize the output spectra, covariance matrix as copies of the inputs
out_h0_spec_dict = {}
out_h1_spec_dict = {}
for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
    out_h0_spec_dict[k] = ROOT.TH1D( in_h0_spec_f.Get(k) )
    out_h1_spec_dict[k] = ROOT.TH1D( in_h1_spec_f.Get(k) )
out_covar = ROOT.TMatrixD( in_covar_f.Get("frac_covariance") )
# Zero out any nans, so that things we add actually get added
for i in range(out_covar.GetNrows()):
    for j in range(out_covar.GetNcols()):
        if math.isnan(out_covar[i][j]):
            out_covar[i][j] = 0.

# Zero out correlations between 1e1p bnb and other channels
for i in range(3*Nbins_e+Nbins_m):
    for j in range(3*Nbins_e+Nbins_m):
        # Determine whether i refers to a 1e1p_bnb row
        if ((i<offset_1e1p_bnb) or (i>=offset_1e1p_lee)):
            cond_i = False
        else:
            cond_i = True
        # Determine whether j refers to a 1e1p_bnb column
        if ((j<offset_1e1p_bnb) or (j>=offset_1e1p_lee)):
            cond_j = False
        else:
            cond_j = True
        # If neither is 1e1p_bnb, don't change anything
        if (not(cond_i) and not(cond_j)):
            continue
        # If i is 1e1p_bnb but j is not, or vice versa, zero out correlations
        if ((cond_i and not(cond_j)) or (not(cond_i) and cond_j)):
            out_covar[i][j] = 0.
        # If both are 1e1p but they are not equal to each other, also zero out correlations
        if ((cond_i and cond_j) and not(i==j)):
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

                
# Add *fractional* mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p...
#   and remove them from spec errors, so SBNfit doesn't double-count
print "Adding mc stat errors from {}".format(in_h1_spec_fname)
for i in range(Nbins_e):
    if in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1) > 0.:
        out_covar[i][i] += (in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1))**2
    out_h0_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
    out_h1_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
for i in range(Nbins_e):
    if in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1) > 0.:
        out_covar[offset_1e1p_lee+i][offset_1e1p_lee+i] += (in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1))**2
    out_h0_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
    out_h1_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
for i in range(Nbins_m):
    if in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1) > 0.:
        out_covar[offset_1mu1p+i][offset_1mu1p+i] += (in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1))**2
    out_h0_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
    out_h1_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
# ... done adding mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p


# Update prediction and mc stat errors for 1e1p bnb (i.e., numu backgrounds to the 1e1p selection)...
# Read in the fitted prediction and associated mc stat covariance matrix
#   Note: Both have 11 1e1p bins from 100 to 1200 MeV in 100 MeV bins
#   Note: MC stat covariance matrix in this file is *fractional*
print "Updating prediction for numu backgrounds to the 1e1p from {}".format(bkg_pred_fname)
print "Adding mc stat errors for numu backgrounds to the 1e1p from {}".format(bkg_covar_fname)
with open(bkg_pred_fname, 'r') as f:
    # First line has binning information, second line has spectrum
    bkg_pred = [ float(x) for x in f.readlines()[1].strip().split() ]
bkg_covar = []
with open(bkg_covar_fname, 'r') as f:
    for l in f:
        bkg_covar.append( [ float(x) for x in l.strip().split() ] )
# scale the prediction as needed
in_pot_bkg  = float(1.631e+20) + float(2.749e+20) + float(2.291e+20)  # Run 1 + 2 + 3, for the final filtered data samples
in_pot_spec = float(13.e+20)
bkg_scale = in_pot_spec / in_pot_bkg
bkg_pred = [ bkg_scale*x for x in bkg_pred ]
print "Scaling the nominal prediction for numu backgrounds to the 1e1p by {:.3e}/{:.3e} = {:.3f}".format(in_pot_spec, in_pot_bkg, bkg_scale)
print "  Resulting backgrounds: {}".format([round(x,3) for x in bkg_pred])
# Update everything -- spec bin contents, spec errors, and covariance matrix
#   Note: We only use the 10 1e1p bins from 200 to 1200 MeV, so have an offset of 1
in_offset_bkg = 1
for i in range(Nbins_e):
    out_h0_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinContent(i+1, bkg_pred[in_offset_bkg+i])
    out_h1_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinContent(i+1, bkg_pred[in_offset_bkg+i])
    out_h0_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinError(i+1, 0.)
    out_h1_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinError(i+1, 0.)
    for j in range(Nbins_e):
        out_covar[offset_1e1p_bnb+i][offset_1e1p_bnb+j] += bkg_covar[in_offset_bkg+i][in_offset_bkg+j]
# ... done updating prediction and mc stat errors for 1e1p bnb

                
# Write everything out
for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
    out_h0_spec_f.WriteTObject(out_h0_spec_dict[k])
    out_h1_spec_f.WriteTObject(out_h1_spec_dict[k])
out_covar_f.WriteTObject(out_covar, "frac_covariance")
# Close the outputs
out_h0_spec_f.Close()
out_h1_spec_f.Close()
out_covar_f.Close()
# Close the inputs
in_h0_spec_f.Close()
in_h1_spec_f.Close()
in_covar_f.Close()

print "Done!"
