import os,subprocess
import ROOT

topdir = os.getcwd()
autodir = os.path.join(topdir, "auto")

sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg", "dllee_bdt_score_median" ]
sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
sel1e1p_mpidp_cut_values = [ 0.0, 0.2 ]

detsys_subdir_dict = {}
detsys_subdir_dict["dllee_bdt_score_avg"]    = "AvgScore"
detsys_subdir_dict["dllee_bdt_score_median"] = "AvgScore"  # TODO: when detector systematic covariance matrices for median score strategy are available, update this
bkg_subdir_dict = {}
bkg_subdir_dict["dllee_bdt_score_avg"]    = "avgscore"
bkg_subdir_dict["dllee_bdt_score_median"] = "medianscore"

os.chdir(autodir)


for var_e in sel1e1p_bdt_cut_variables:
    for val_p in sel1e1p_mpidp_cut_values:

        detsysdir = os.path.join(topdir, "detsys", detsys_subdir_dict[var_e])  # TODO: when detector systematic covariance matrices with proton MPID cut are available, update this
        bkgdir    = os.path.join(topdir, "bkg", "{:02d}".format(int(val_p*100)), bkg_subdir_dict[var_e])
        
        for val_e in sel1e1p_bdt_cut_values:
            for val_m in sel1mu1p_bdt_cut_values:
                
                tag = "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100), int(val_p*100), int(val_m*100) )
                print tag

                # create the output files
                out_h0_spec_f = ROOT.TFile("leeless_{}_total.SBNspec.root".format(tag), "RECREATE")
                out_h1_spec_f = ROOT.TFile("sens_{}_total.SBNspec.root".format(tag), "RECREATE")
                out_covar_f   = ROOT.TFile("sens_{}_total.SBNcovar.root".format(tag), "RECREATE")
                # open the input files
                in_h0_spec_f = ROOT.TFile.Open("leeless_{}.SBNspec.root".format(tag), "READ")
                in_h1_spec_f = ROOT.TFile.Open("sens_{}.SBNspec.root".format(tag), "READ")
                in_covar_f   = ROOT.TFile.Open("sens_{}.SBNcovar.root".format(tag), "READ")
                # initialize the output spectra, covariance matrix as copies of the inputs
                out_h0_spec_dict = {}
                out_h1_spec_dict = {}
                for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
                    out_h0_spec_dict[k] = ROOT.TH1D( in_h0_spec_f.Get(k) )
                    out_h1_spec_dict[k] = ROOT.TH1D( in_h1_spec_f.Get(k) )
                out_covar = ROOT.TMatrixD( in_covar_f.Get("frac_covariance") )
                
                # define a few helper variables...
                Nbins_e = 10
                Nbins_m = 20
                #offset_1e1p_nue = 0
                offset_1e1p_bnb = Nbins_e 
                offset_1e1p_lee = 2*Nbins_e
                offset_1mu1p    = 3*Nbins_e
                
                # add detector systematics for 1e1p nue, 1e1p lee, and 1mu1p bnb... 
                # read in fractional detector systematic covariance matrix from csv file
                #   note: covariance matrix in this file has dimension 20+12
                #           20 1mu1p bins from 200 to 1200 MeV in  50 MeV bins, then
                #           12 1e1p  bins from   0 to 1200 MeV in 100 MeV bins
                dettag = "mu{}e{}".format( val_m, val_e ).replace('.', '')
                detsys_f = os.path.join(detsysdir, dettag, "covMat_Tot.csv")
                print "Adding detector systematics from {}".format(detsys_f)
                detsys_covar = []
                with open(detsys_f, 'r') as f:
                    for l in f:
                        detsys_covar.append( [ float(x) for x in l.strip().split(',') ] )
                # break this out into block matrices with correct dimensions
                #   note: we only use the 10 1e1p bins from 200 to 1200 MeV, so add 2 to the offset
                in_offset_e = Nbins_m + 2
                detsys_covar_ee = []
                for i in range(Nbins_e):
                    detsys_covar_ee.append( [] )
                    for j in range(Nbins_e):
                        detsys_covar_ee[i].append( detsys_covar[in_offset_e+i][in_offset_e+j] )
                detsys_covar_em = []
                for i in range(Nbins_e):
                    detsys_covar_em.append( [] )
                    for j in range(Nbins_m):
                        detsys_covar_em[i].append( detsys_covar[in_offset_e+i][j] )
                detsys_covar_mm = []
                for i in range(Nbins_m):
                    detsys_covar_mm.append( [] )
                    for j in range(Nbins_m):
                        detsys_covar_mm[i].append( detsys_covar[i][j] )
                # add detsys_covar_ee to the 1e1p nue and lee
                for i in range(Nbins_e):
                    for j in range(Nbins_e):
                        out_covar[i][j] += detsys_covar_ee[i][j]
                        out_covar[i][offset_1e1p_lee+j] += detsys_covar_ee[i][j]
                        out_covar[offset_1e1p_lee+i][j] += detsys_covar_ee[i][j]
                        out_covar[offset_1e1p_lee+i][offset_1e1p_lee+j] += detsys_covar_ee[i][j]
                # add detsys_covar_em to the block off-diagonals between {1e1p nue, 1e1p lee}x{1mu1p bnb}
                for i in range(Nbins_e):
                    for j in range(Nbins_m):
                        out_covar[i][offset_1mu1p+j] += detsys_covar_em[i][j]
                        out_covar[offset_1mu1p+j][i] += detsys_covar_em[i][j]
                        out_covar[offset_1e1p_lee+i][offset_1mu1p+j] += detsys_covar_em[i][j]
                        out_covar[offset_1mu1p+j][offset_1e1p_lee+i] += detsys_covar_em[i][j]
                # add detsys_covar_mm to the 1mu1p bnb
                for i in range(Nbins_m):
                    for j in range(Nbins_m):
                        out_covar[offset_1mu1p+i][offset_1mu1p+j] += detsys_covar_mm[i][j]
                # ... done adding detector systematics for 1e1p nue, 1e1p lee, and 1mu1p bnb
                
                
                # add detector systematics for 1e1p bnb (i.e., numu backgrounds to the 1e1p selection)...
                detsys_bkg = 0.2**2  # TODO: update this value
                print "Adding detector systematics for numu backgrounds to the 1e1p ({:.3f})".format(detsys_bkg)
                for i in range(Nbins_e):
                    out_covar[offset_1e1p_bnb+i][offset_1e1p_bnb+i] += detsys_bkg
                # ... done adding detector systeamtics for 1e1p bnb
                
                #for i in range( out_covar.GetNrows() ):
                #    for j in range( out_covar.GetNrows() ):
                #        #if not((i==j) or (i+1==j) or (i+offset_1mu1p==j)): continue
                #        print "{}, {}: {}".format(i, j, out_covar[i][j] - in_covar_f.Get("frac_covariance")[i][j] )
                
                
                # add *fractional* mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p...
                #   and remove them from spec errors, so SBNfit doesn't double-count
                print "Adding mc stat errors from {}".format("sens_{}.SBNspec.root".format(tag))
                for i in range(Nbins_e):
                    if in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1) > 0.:
                        out_covar[i][i] += in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetBinContent(i+1)
                    out_h0_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
                    out_h1_spec_dict["nu_uBooNE_1e1p_nue"].SetBinError(i+1, 0.)
                for i in range(Nbins_e):
                    if in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1) > 0.:
                        out_covar[offset_1e1p_lee+i][offset_1e1p_lee+i] += in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1e1p_lee").GetBinContent(i+1)
                    out_h0_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
                    out_h1_spec_dict["nu_uBooNE_1e1p_lee"].SetBinError(i+1, 0.)
                for i in range(Nbins_m):
                    if in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1) > 0.:
                        out_covar[offset_1mu1p+i][offset_1mu1p+i] += in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinError(i+1) / in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb").GetBinContent(i+1)
                    out_h0_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
                    out_h1_spec_dict["nu_uBooNE_1mu1p_bnb"].SetBinError(i+1, 0.)
                # ... done adding mc stat errors for 1e1p nue, 1e1p lee, and 1mu1p
                
                # update prediction and mc stat errors for 1e1p bnb (i.e., numu backgrounds to the 1e1p selection)...
                # read in the fitted prediction and associated mc stat covariance matrix
                #   note: both have 11 1e1p bins from 100 to 1200 MeV in 100 MeV bins
                #   note: mc stat covariance matrix in this file is *fractional*
                bkgtag = "bkg_{:.2f}".format(val_e)
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
                # update everything -- spec bin contents, spec errors, and covariance matrix
                #   note: we only use the 10 1e1p bins from 200 to 1200 MeV, so have an offset of 1
                in_offset_bkg = 1
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
