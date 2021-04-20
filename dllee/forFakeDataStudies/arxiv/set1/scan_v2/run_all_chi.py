import os,subprocess
import ROOT
from calc_chi_with_constraint import calcChiWithConstraint

topdir = os.getcwd()
autodir = os.path.join(topdir,"auto")
pdir = os.path.join(topdir,"persistent")
outdir = os.path.join(topdir,"output")
subprocess.call("mkdir -p %s" % outdir, shell=True)
output = os.path.join(outdir,"output.txt")

scale_list = [ 0.05*i for i in range(141) ]

for scale in scale_list:

    tag = "{:03d}".format(int(scale*100))
    thisdir = os.path.join(autodir,tag)
    os.chdir(thisdir)

    spec_fname = 'sens.SBNspec.root'
    covar_fname = 'total_sens.SBNcovar.root'
    data_spec_fname = os.path.join(pdir,'fakedata.SBNspec.root')

    # Create dict of nue, numu spectra
    spec_file = ROOT.TFile.Open(spec_fname)
    spec_keys = [ key.GetName() for key in spec_file.GetListOfKeys() ]
    spec_dict = {}
    for k in spec_keys:
        # Get the name of the selection that this spectrum contributes to
        sel = k.split('_')[2]
        # Add it to the dictionary
        if sel not in spec_dict:
            spec_dict[sel] = spec_file.Get(k)
        else: spec_dict[sel].Add(spec_file.Get(k))

    # Get the total covariance matrix
    covar_file = ROOT.TFile.Open(covar_fname)
    # Get the total collapsed covariance matrix
    total_covar = covar_file.Get("collapsed_covariance")

    # Get the data spectrum
    data_spec_file = ROOT.TFile.Open(data_spec_fname)
    data_spec_keys = [ key.GetName() for key in data_spec_file.GetListOfKeys() ]
    data_spec_dict = {}
    for k in data_spec_keys:
        # Get the name of the selection that this spectrum contributes to
        sel = k.split('_')[2]
        # Add it to the dictionary
        if sel not in data_spec_dict:
            data_spec_dict[sel] = data_spec_file.Get(k)
        else: data_spec_dict[sel].Add(data_spec_file.Get(k))

    # Calculate the chi2 with constraint
    chi2 = calcChiWithConstraint(spec_dict['1e1p'], spec_dict['1mu1p'], total_covar, data_spec_dict['1e1p'], data_spec_dict['1mu1p'], debug=False)
    print scale, chi2

    with open(output, 'a+') as f:
        f.write("%s,%s\n" % (scale, chi2))

os.chdir(topdir)

print "Done!"
