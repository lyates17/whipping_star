import ROOT
import math

# TODO: define functions that form total, fractional covariane matrices (given the other + a spectrum)

def getSpecList(hist_list, debug=False):




def checkInversion(matrix, inverse, tol=1e-6, debug=False):

    # Make copies of the matrices
    mat = ROOT.TMatrixD(matrix)
    inv = ROOT.TMatrixD(inverse)

    # Compute check1 = matrix * inverse
    check1 = ROOT.TMatrixD(mat)
    check1 *= inv

    # Compute check2 = inverse * covar
    check2 = ROOT.TMatrixD(inv)
    check2 *= mat

    # If in debug mode, print resulting matrices
    if debug:
        print("covar * inverse matrix: ")
        check1.Print()
        print("inverse * covar matrix: ")
        check2.Print()

    # For both check1 and check2, check that diagonal entries are nearly 1 and off-diagonal entries are nearly zero
    dim = mat.GetNrows()  # dimension of the matrix
    #tol = 1e-6           # tolerance for deviations from identity matrix, passed as an argument instead
    for i in range(dim):
        for j in range(dim):
            # Diagonal entries...
            if i == j:
                if ( abs(check1[i][j]-1) < tol ) and ( abs(check2[i][j]-1) < tol ): continue
                else: return False
            # Off-diagonal entries...
            else: 
                if ( abs(check1[i][j]) < tol ) and ( abs(check2[i][j]) < tol): continue
                else: return False

    return True
## End definition of checkInversion


def runConstraint(nue_spec, numu_spec, covar, numu_data_spec, debug=False):

    ## Function that calculates the constrained nue prediction and covariance matrix using the method from docdb-32672
    ## Inputs:
    ##   nue_spec          nue MC spectrum (python list or similar)
    ##   numu_spec         numu MC spectrum (python list or similar)
    ##   covar             joint nue+numu total covariance marix (TMatrixT<double>)
    ##                       note: this should include all systematic uncertainties and MC stat errors, but *not* data stat errors
    ##                       note: this should be the absolute covariance matrix, *not* fractional
    ##   numu_data_spec    numu data spectrum (python list or similar)
    ##   debug             flag for whether to print out various debugging information
    ## Returns:
    ##   constr_nue_spec      constrained nue spectrum (python list)
    ##   constr_covar_nue     constrained nue covariance matrix (TMatrixT<double>)
    ##                          note: *not* fractional, same as input covar
    
    
    # If operating in debug mode, print out information on inputs
    if debug:
        print("nue spectrum: ", nue_spec)
        print("numu spectrum: ", numu_spec)
        print("numu data spectrum: ", numu_data_spec)
        print("covariance matrix: ")
        covar.Print()

    # Count the number of bins in each spectrum
    Nbins_e = len(nue_spec)
    Nbins_m = len(numu_spec)
    # Check that the dimensions of the inputs are consistent
    if len(numu_data_spec) != Nbins_m:
        print("Length of numu data spec doesn't match numu spec! returning...")
        return
    if covar.GetNrows() != Nbins_e+Nbins_m:
        print("Dimension of covariance matrix doesn't match nue+numu spec! returning...")
        return
    # If in debug mode, pring out the number of bins in each spectrum
    if debug:
        print("nue spectrum bins: ", Nbins_e)
        print("numu spectrum bins: ", Nbins_m)

    # Take the standard covariance matrix and break it into its block components
    covar_ee = ROOT.TMatrixD(Nbins_e,Nbins_e)
    for i in range(Nbins_e):
        for j in range(Nbins_e):
            covar_ee[i][j] = covar[i][j]
    covar_em = ROOT.TMatrixD(Nbins_e,Nbins_m)
    covar_me = ROOT.TMatrixD(Nbins_m,Nbins_e)
    for i in range(Nbins_e):
        for j in range(Nbins_m):
            covar_em[i][j] = covar[i][Nbins_e+j]
            covar_me[j][i] = covar[i][Nbins_e+j]
    covar_mm = ROOT.TMatrixD(Nbins_m,Nbins_m)
    for i in range(Nbins_m):
        for j in range(Nbins_m):
            covar_mm[i][j] = covar[Nbins_e+i][Nbins_e+j]
    # If in debug mode, print these matrices and their first diagonal elements
    if debug:
        print("covariance matrix ee: ")
        print(covar_ee[0][0])
        covar_ee.Print()
        print("covariance matrix em: ")
        print(covar_em[0][0])
        covar_em.Print()
        print("covariance matrix me: ")
        print(covar_me[0][0])
        covar_me.Print()
        print("covariance matrix mm: ")
        print(covar_mm[0][0])
        covar_mm.Print()

    # Add the predicted data statistical errors to covar_mm
    for i in range(Nbins_m):
        covar_mm[i][i] += numu_spec[i]
    # If in debug mode, print this matrix and its first diagonal element
    if debug:
        print("covariance matrix mm, with expected data statistical errors added:")
        print(covar_mm[0][0])
        covar_mm.Print()

    # Compute the constrained nue prediction as mu_e^{constrained} = mu_e + covar_em*(covar_mm)^{-1}*(X_m - mu_m)...
    #   where mu are the predicted spectra (N^{MC}), X are the observed spectra (N^{data}), and the covar are the blocks of the covariance matrix as defined above
    diff_vec = ROOT.TMatrixD(Nbins_m,1)  # diff_vec = X_m - mu_m
    for i in range(Nbins_m):
        diff_vec[i][0] = numu_data_spec[i] - numu_spec[i]
    covar_mm_inverse = ROOT.TMatrixD(covar_mm).Invert()
    if not checkInversion(covar_mm, covar_mm_inverse):
        print("Matrix covar_mm not invertable, returning...")
        return
    calc_vec1 = ROOT.TMatrixD(Nbins_m,1)  # calc_vec1 = (covar_mm)^{-1}*diff_vec
    #calc_vec1 = ROOT.TMatrixD.Mult(covar_mm_inverse, diff_vec)
    for i in range(Nbins_m):
        calc_vec1[i][0] = 0.
        for j in range(Nbins_m):
            calc_vec1[i][0] += covar_mm_inverse[i][j]*diff_vec[j][0]
    calc_vec2 = ROOT.TMatrixD(Nbins_e,1)   # calc_vec2 = covar_em*(covar_mm)^{-1}*diff_vec = covar_em*calc_vec1
    #calc_vec2 = ROOT.TMatrixD.Mult(covar_em, calc_vec1)
    for i in range(Nbins_e):
        calc_vec2[i][0] = 0.
        for j in range(Nbins_m):
            calc_vec2[i][0] += covar_em[i][j]*calc_vec1[j][0]
    constr_nue_spec = [ 0. for i in range(Nbins_e) ]
    for i in range(Nbins_e):
        constr_nue_spec[i] = nue_spec[i] + calc_vec2[i][0]
    # If in debug mode, print these matrices/vectors out...
    if debug:
        print("diff vec: ")
        diff_vec.Print()
        print("inverse of covar_mm: ")
        covar_mm_inverse.Print()
        print("(inverse of covar_mm)*diff_vec vec: ")
        calc_vec1.Print()
        print("covar_em*(inverse of covar_mm)*diff_vec vec:")
        calc_vec2.Print()
        print("constrained nue prediction: ")
        print(constr_nue_spec)

    # Compute the constrained nue covariance matrix as covar_ee^{constrained} = covar_ee - covar_em*(covar_mm)^{-1}*covar_me
    calc_mat1 = ROOT.TMatrixD(Nbins_m,Nbins_e)  # calc_mat1 = (covar_mm)^{-1}*covar_me
    #calc_mat1 = ROOT.TMatrixD.Mult(covar_mm_inverse, covar_me)
    for i in range(Nbins_m):
        for j in range(Nbins_e):
            calc_mat1[i][j] = 0.
            for k in range(Nbins_m):
                calc_mat1[i][j] += covar_mm_inverse[i][k]*covar_me[k][j]
    calc_mat2 = ROOT.TMatrixD(Nbins_e,Nbins_e)   # calc_mat2 = covar_em*(covar_mm)^{-1}*covar_me
    #calc_mat2 = ROOT.TMatrixD.Mult(covar_em, calc_mat1)
    for i in range(Nbins_e):
        for j in range(Nbins_e):
            calc_mat2[i][j] = 0.
            for k in range(Nbins_m):
                calc_mat2[i][j] += covar_em[i][k]*calc_mat1[k][j]
    constr_covar_nue = ROOT.TMatrixD(Nbins_e,Nbins_e)
    for i in range(Nbins_e):
        for j in range(Nbins_e):
            constr_covar_nue[i][j] = covar_ee[i][j] - calc_mat2[i][j]
    # If in debug mode, print these matrices out
    if debug:
        print("covar_em*(covar_mm)^{-1}*covar_me: ")
        calc_mat2.Print()
        print("constrained nue covariance matrix: ")
        constr_covar_nue.Print()
        
    # Retrun constrained prediction, covariance matrix
    return constr_nue_spec, constr_covar_nue
## End definition of runConstraint



# If this is the executable...
if __name__ == "__main__":

    topdir = os.getcwd()
    autodir = os.path.join(topdir, "auto")

    sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg", "dllee_bdt_score_median" ]
    sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
    sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
    sel1e1p_mpidp_cut_values = [ 0.0, 0.2 ]
    
    os.chdir(autodir)

    for var_e in sel1e1p_bdt_cut_variables:
        for val_p in sel1e1p_mpidp_cut_values:
            for val_e in sel1e1p_bdt_cut_values:
                for val_m in sel1mu1p_bdt_cut_values:
                    
                    tag = "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100.), int(val_p*100), int(val_m*100) )
                    print tag

                    # create the output files
                    out_h0_spec_f = ROOT.TFile("leeless_{}_constr.SBNspec.root".format(tag), "RECREATE")
                    out_h1_spec_f = ROOT.TFile("sens_{}_constr.SBNspec.root".format(tag), "RECREATE")
                    out_covar_f   = ROOT.TFile("sens_{}_constr.SBNcovar.root".format(tag), "RECREATE")
                    # open the input files
                    in_h0_spec_f   = ROOT.TFile.Open("leeless_{}_total.SBNspec.root".format(tag), "READ")
                    in_h1_spec_f   = ROOT.TFile.Open("sens_{}_total.SBNspec.root".format(tag), "READ")
                    in_covar_f     = ROOT.TFile.Open("sens_{}_total.SBNcovar.root".format(tag), "READ")
                    in_data_spec_f = in_h0_spec_f  # TODO: when real numu data is available, update this
                    
                    # convert input spectra from TH1Ds to python lists
                    nue_spec   = getSpecList( [ in_h1_spec_f.Get(k) for k in ["nu_uBooNE_1e1p_nue", "nu_uBooNE_1e1p_bnb", "nu_uBooNE_1e1p_lee"] ] )
                    numu_spec  = getSpecList( [ in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb") ] )
                    total_spec = getSpecList( [ in_h1_spec_f.Get(k) for k in ["nu_uBooNE_1e1p_nue", "nu_uBooNE_1e1p_bnb", "nu_uBooNE_1e1p_lee", "nu_uBooNE_1mu1p_bnb"] ] )
                    # convert input fractional covariance matrix to total covariance matrix
                    total_covar = getTotalCovar()

                    # initialize the output spectra as copies of the inputs
                    out_h0_spec_dict = {}
                    out_h1_spec_dict = {}
                    for k in [ key.GetName() for key in in_h1_spec_f.GetListOfKeys() ]:
                        if '1mu1p' in k: continue
                        out_h0_spec_dict[k] = ROOT.TH1D( in_h0_spec_f.Get(k) )
                        out_h1_spec_dict[k] = ROOT.TH1D( in_h1_spec_f.Get(k) )

    
    # Create dict of nue, numu spectra
    spec_file = ROOT.TFile.Open(spec_fname)
    spec_keys = [ key.GetName() for key in spec_file.GetListOfKeys() ]
    spec_dict = {}
    for k in spec_keys:
        # Get the name of the selection that this spectrum contributes to
        sel = k.split('_')[2]
        # Add it to the dictionary
        if sel not in spec_dict: spec_dict[sel] = spec_file.Get(k)
        else: spec_dict[sel].Add(spec_file.Get(k))

    # Get the total collapsed covariance matrix
    covar_file = ROOT.TFile.Open(covar_fname)
    total_covar = covar_file.Get("collapsed_covariance")

    # Get the data spectrum
    data_spec_file = ROOT.TFile.Open(data_spec_fname)
    data_spec_keys = [ key.GetName() for key in data_spec_file.GetListOfKeys() ]
    data_spec_dict = {}
    for k in data_spec_keys:
        # Get the name of the selection that this spectrum contributes to
        sel = k.split('_')[2]
        # Add it to the dictionary
        if sel not in data_spec_dict: data_spec_dict[sel] = data_spec_file.Get(k)
        else: data_spec_dict[sel].Add(data_spec_file.Get(k))

    # Add statistical errors to the numu component of the joint covariance matrix
    for i in range(spec_dict['1mu1p'].GetNbinsX()):
        total_covar[spec_dict['1e1p'].GetNbinsX()+i][spec_dict['1e1p'].GetNbinsX()+i] += spec_dict['1mu1p'].GetBinContent(i+1)
    # Calculate the constrained nue spectrum, covarinace matrix
    constr_nue_spec, constr_nue_covar = runConstraint(spec_dict['1e1p'], spec_dict['1mu1p'], total_covar, data_spec_dict['1mu1p'], debug=True)

    print("N_fit_nue: ", [ constr_nue_spec[i] for i in range(spec_dict['1e1p'].GetNbinsX()) ])
    print("sigma_fit_nue: ", [ math.sqrt(constr_nue_covar[i][i]) for i in range(spec_dict['1e1p'].GetNbinsX()) ])
    

    print("Done!")
