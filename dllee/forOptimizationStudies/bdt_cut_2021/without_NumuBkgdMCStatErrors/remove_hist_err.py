import sys,ROOT

# loop over tags
for tag in sys.argv[1:]:
    fname = "%s.SBNspec.root" % tag
    fin   = ROOT.TFile.Open(fname, "UPDATE")
    specin = fin.Get("nu_uBooNE_1e1p_bnb")
    for i in range(specin.GetNbinsX()):
        specin.SetBinError(i+1, 0.)
    fin.Write()
    fin.Close()
