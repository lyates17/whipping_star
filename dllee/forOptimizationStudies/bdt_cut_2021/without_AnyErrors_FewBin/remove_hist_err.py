import sys,ROOT

# loop over tags
for tag in sys.argv[1:]:
    fname = "%s.SBNspec.root" % tag
    fin   = ROOT.TFile.Open(fname, "UPDATE")
    spec_list = [ key.GetName() for key in fin.GetListOfKeys() ]
    for spec_key in spec_list:
        specin = fin.Get(spec_key)
        for i in range(specin.GetNbinsX()):
            specin.SetBinError(i+1, 0.)
    fin.Write()
    fin.Close()
