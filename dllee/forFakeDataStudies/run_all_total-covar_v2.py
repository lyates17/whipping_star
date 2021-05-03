import os,subprocess
from math import sqrt
import ROOT

topdir = os.getcwd()

pdir      = os.path.join(topdir, "persistent")
bkgdir    = os.path.join(pdir, "bkg")
specdir   = os.path.join(pdir, "spec")

fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]

# define a few helper variables...
Nbins_e = 10
Nbins_m = 19
#offset_1e1p_nue = 0
offset_1e1p_bnb = Nbins_e 
offset_1e1p_lee = 2*Nbins_e
offset_1mu1p    = 3*Nbins_e


for tag in fakedata_list:

    workdir = os.path.join(topdir, tag)
    os.chdir(workdir)

    # create the output files
    out_h0_spec_f = ROOT.TFile("h0_total.SBNspec.root", "RECREATE")
    out_h1_spec_f = ROOT.TFile("h1_total.SBNspec.root", "RECREATE")
    out_covar_f   = ROOT.TFile("h1_total.SBNcovar.root", "RECREATE")
    # open the input files
    in_h0_spec_f = ROOT.TFile.Open("h0.SBNspec.root", "READ")
    in_h1_spec_f = ROOT.TFile.Open("h1.SBNspec.root", "READ")
    in_covar_f   = ROOT.TFile.Open(os.path.join(pdir, "sens_total-sys.SBNcovar.root"), "READ")
    # initialize the output spectra, covariance matrix as copies of the inputs
    out_h0_spec_dict = {}
    out_h1_spec_dict = {}
    for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
        out_h0_spec_dict[k] = ROOT.TH1D( in_h0_spec_f.Get(k) )
        out_h1_spec_dict[k] = ROOT.TH1D( in_h1_spec_f.Get(k) )
    out_covar = ROOT.TMatrixD( in_covar_f.Get("frac_covariance") )
    
    # read in the predicted spectra (see Slack message from Nick on 4/28)
    #   note: have 12 1e1p bins from 0 to 1200 MeV, so have an offset of 2
    #   note: order is nue, bnb, lee
    #   note: then have sum of weights squared for bnb events, and then sum of bnb events
    in_offset_spec = 2
    in_pred_spec = []
    with open(os.path.join(specdir, "sel1e1p_spec_{}.txt".format(tag)), 'r') as f:
        for l in f:
            s = [ float(x) for x in l.strip().split() ]
            in_pred_spec.append(s)

    # detector systematics already added...
    
    # add *fractional* mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p...
    #   and remove them from spec errors, so SBNfit doesn't double-count
    # update prediction for 1e1p nue and lee...
    print "Adding mc stat errors from {}".format("h1.SBNspec.root")
    print "Updating prediction for 1e1p from {}".format("sel1e1p_spec_{}.txt".format(tag))
    for i in range(Nbins_e):
        if in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1) > 0.:
            out_covar[i][i] += (in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1))**2
        out_h0_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
        out_h1_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
        out_h0_spec_dict["nu_uBooNE_1e1p_nue"].SetBinContent(i+1, in_pred_spec[0][in_offset_spec+i])
        out_h1_spec_dict["nu_uBooNE_1e1p_nue"].SetBinContent(i+1, in_pred_spec[0][in_offset_spec+i])
    for i in range(Nbins_e):
        if in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1) > 0.:
            out_covar[offset_1e1p_lee+i][offset_1e1p_lee+i] += (in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1))**2
        out_h0_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
        out_h1_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
        out_h0_spec_dict["nu_uBooNE_1e1p_lee"].SetBinContent(i+1, 0.)
        out_h1_spec_dict["nu_uBooNE_1e1p_lee"].SetBinContent(i+1, in_pred_spec[2][i+2])
    for i in range(Nbins_m):
        if in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1) > 0.:
            out_covar[offset_1mu1p+i][offset_1mu1p+i] += (in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1))**2
        out_h0_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
        out_h1_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
    # ... done adding mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p
                
    # update prediction and mc stat errors for 1e1p bnb (i.e., numu backgrounds to the 1e1p selection)...
    # read in the fitted prediction and associated mc stat covariance matrix
    #   note: both have 11 1e1p bins from 100 to 1200 MeV in 100 MeV bins
    #   note: mc stat covariance matrix in this file is *fractional*
    bkgtag = "bkg_{:.2f}".format(0.95)
    bkg_pred_f   = os.path.join(bkgdir, "{}_prediction.txt".format(bkgtag))
    bkg_mcstat_f = os.path.join(bkgdir, "{}_cov.txt".format(bkgtag))
    print "Updating prediction for numu backgrounds to the 1e1p from {}".format(bkg_pred_f)
    print "Adding mc stat errors for numu backgrounds to the 1e1p from {}".format(bkg_mcstat_f)
    with open(bkg_pred_f, 'r') as f:
        # first line has binning information, second line has spectrum
        bkg_pred = [ float(x) for x in f.readlines()[1].strip().split() ]
    bkg_mcstat_covar = []
    with open(bkg_mcstat_f, 'r') as f:
        for l in f:
            bkg_mcstat_covar.append( [ float(x) for x in l.strip().split() ] )
    # scale the prediction to match the normalization of the backgrounds in this set, and update the MC stat covariance matrix too
    #   note: we only use the 10 1e1p bins from 200 to 1200 MeV, so have an offset of 1
    in_offset_bkg = 1
    in_norm_bkg      = sum(bkg_pred[in_offset_bkg:])
    in_norm_1e1p_bnb = sum(in_pred_spec[1][in_offset_spec:])
    bkg_scale = in_norm_1e1p_bnb / in_norm_bkg
    bkg_pred = [ bkg_scale*x for x in bkg_pred ]
    for i in range(len(bkg_mcstat_covar)):
        for j in range(len(bkg_mcstat_covar[i])):
            bkg_mcstat_covar[i][j] += ( in_pred_spec[3][0] - 0.033752591055783904 )  # see Slack message from Nick on 4/21, 08:51
    print "Scaling the nominal prediction for numu backgrounds to the 1e1p by {:.3f}/{:.3f} = {:.3f}".format(in_norm_1e1p_bnb, in_norm_bkg, bkg_scale)
    print "  Resulting backgrounds: {} (sum: {:.3f} = {:.3f})".format([round(x,3) for x in bkg_pred], in_norm_1e1p_bnb, sum(bkg_pred[in_offset_bkg:]))
    # update everything -- spec bin contents, spec errors, and covariance matrix
    #   note: we only use the 10 1e1p bins from 200 to 1200 MeV, so have an offset of 1
    #in_offset_bkg = 1  # declared above
    for i in range(Nbins_e):
        out_h0_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinContent(i+1, bkg_pred[in_offset_bkg+i])
        out_h1_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinContent(i+1, bkg_pred[in_offset_bkg+i])
        out_h0_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinError(i+1, 0.)
        out_h1_spec_dict["nu_uBooNE_1e1p_bnb"].SetBinError(i+1, 0.)
        for j in range(Nbins_e):
            out_covar[offset_1e1p_bnb+i][offset_1e1p_bnb+j] += bkg_mcstat_covar[in_offset_bkg+i][in_offset_bkg+j]
    # ... done updating prediction and mc stat errors for 1e1p bnb
    
    
    # write everything out
    for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
        out_h0_spec_f.WriteTObject(out_h0_spec_dict[k])
        out_h1_spec_f.WriteTObject(out_h1_spec_dict[k])
    out_covar_f.WriteTObject(out_covar, "frac_covariance")
    # close the inputs
    in_h0_spec_f.Close()
    in_h1_spec_f.Close()
    in_covar_f.Close()
    # close the outputs
    out_h0_spec_f.Close()
    out_h1_spec_f.Close()
    out_covar_f.Close()
    
    # again, run the next steps in a separate script...

os.chdir(topdir)

print "Done!"
