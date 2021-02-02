import ROOT
import math

def checkInversion(matrix, inverse, dim, debug=False):

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
    tol = 1e-6    # tolerance for deviations from identity matrix
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

def getNueComponent(matrix, nue_spec, debug=False):
    # Initialize a matrix of the right size
    nue_matrix = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())
    # Fill it
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            nue_matrix[i][j] = matrix[i][j]
    # Return it
    return nue_matrix
## End definition of getNueComponent


def runMBConstraint(nue_spec, numu_spec, covar, numu_data_spec, debug=False):

    ## Function that calculates the constrained nue prediction and covariance matrix using the "MiniBooNE" Mike 2008 procedure
    ## Inputs:
    ##   nue_spec          nue MC spectrum (TH1D)
    ##   numu_spec         numu MC spectrum (TH1D)
    ##   covar             joint nue+numu covariance marix (TMatrixT<double>) (note: for MB TN 255 procedure, this should be the total sys+stats covariance matrix)
    ##   numu_data_spec    numu data spectrum (TH1D)
    ##   debug             flag for whether to print out various debugging information
    ## Returns:
    ##   N_fit_nue_vec     constrained nue spectrum (TVectorT<double>)
    ##   covar_fit_nue     constrained nue covariance matrix (TMatrixT<double>) (note: *not* fractional)

    
    # If operating in debug mode, print out information on inputs
    if debug:
        print("nue spectrum: ", [ nue_spec.GetBinContent(i+1) for i in range(nue_spec.GetNbinsX()) ])
        print("numu spectrum: ", [ numu_spec.GetBinContent(i+1) for i in range(numu_spec.GetNbinsX()) ])
        print("numu data spectrum: ", [ numu_data_spec.GetBinContent(i+1) for i in range(numu_data_spec.GetNbinsX()) ])
        print("covariance matrix: ")
        covar.Print()
    
    # 1) Take the standard covariance matrix and invert it
    inverse = ROOT.TMatrixD(covar).Invert()
    # If in debug mode, print the inverse matrix and the first diagonal element in the numu block
    if debug:
        print("inverse of covariance matrix: ")
        inverse.Print()
        print(inverse[nue_spec.GetNbinsX()][nue_spec.GetNbinsX()])

    # 1a) Validate that the matrix inversion worked as expected
    #sn = 1e-16
    if not checkInversion(covar, inverse, nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        print("Matrix covar not invertable, returning...")
        return
        ## 1b) If not, add small number to diagonals and try again
        #print("Matrix not invertable, adding small number to diagonals and trying again...")
        #for i in range(nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        #    covar[i][i] += sn
        #inverse = ROOT.TMatrixD(covar).Invert()
        ## If that still doesn't work, return
        #if not checkInversion(covar, inverse, nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        #    print("Matrix still not invertable, returning...")
        #    return

    # 2B) Add the reciprocal of the numu data error squared, 1/N_i^{data}, to the diagonal of the numu part of the inverse matrix
    B_matrix_inverse = ROOT.TMatrixD(inverse)
    for i in range(numu_spec.GetNbinsX()):
        B_matrix_inverse[i+nue_spec.GetNbinsX()][i+nue_spec.GetNbinsX()] += 1. / numu_data_spec.GetBinContent(i+1)
    # If in debug mode, print this modified inverse matrix and first diagonal element in numu block
    if debug:
        print("inverse of B matrix: ")
        B_matrix_inverse.Print()
        print(B_matrix_inverse[nue_spec.GetNbinsX()][nue_spec.GetNbinsX()])

    # 2C) Add the reciprocal of the number of numu MC events, 1/N_i^{MC}, to the diagonal of the numu part of the inverse matrix
    C_matrix_inverse = ROOT.TMatrixD(inverse)
    for i in range(numu_spec.GetNbinsX()):
        C_matrix_inverse[i+nue_spec.GetNbinsX()][i+nue_spec.GetNbinsX()] += 1. / numu_spec.GetBinContent(i+1)
    # If in debug mode, print this modified inverse matrix and first diagonal element in numu block
    if debug:
        print("inverse of C matrix: ")
        C_matrix_inverse.Print()
        print(C_matrix_inverse[nue_spec.GetNbinsX()][nue_spec.GetNbinsX()])

    # 3) Invert the B inverse matrix to get contrained covariance matrix
    B_matrix = ROOT.TMatrixD(B_matrix_inverse).Invert()
    # If in debug mode, print out this matrix
    if debug:
        print("constrained covariance matrix, B: ")
        B_matrix.Print()

    # 3a) Validate that the matrix inversion worked as expected
    if not checkInversion(B_matrix, B_matrix_inverse, nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        print("Matrix B_inverse not invertable, returning...")
        return
    
    # 4) Calculate N_i^{fit}
    # 4a) Form the vector N^{MC}...
    N_MC_vec = ROOT.TVectorD(nue_spec.GetNbinsX()+numu_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        N_MC_vec[i] = nue_spec.GetBinContent(i+1)
    for i in range(numu_spec.GetNbinsX()):
        N_MC_vec[i+nue_spec.GetNbinsX()] = numu_spec.GetBinContent(i+1)
    # If in debug mode, print out this vector
    if debug:
        print("vector of MC bin values: ")
        N_MC_vec.Print()
    # 4b) Calculate the vector N^{fit} by multiplying B*C^{-1}*N^{MC}...
    N_fit_vec = ROOT.TVectorD(nue_spec.GetNbinsX()+numu_spec.GetNbinsX())  # N_fit_vec = B*(calc_vec)
    calc_vec = ROOT.TVectorD(nue_spec.GetNbinsX()+numu_spec.GetNbinsX())   # calc_vec = C^{-1}*N^{MC}
    for j in range(nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        calc_vec[j] = 0.
        for k in range(nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
            calc_vec[j] += C_matrix_inverse[j][k]*N_MC_vec[k]
    for i in range(nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        N_fit_vec[i] = 0.
        for j in range(nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
            N_fit_vec[i] += B_matrix[i][j]*calc_vec[j]
    # If in debug mode, print out this vector
    if debug:
        print("vector of fit bin values: ")
        N_fit_vec.Print()

    # 5) Get the nue components of the N_i^{fit} and the constrained covariance matrix, B
    N_fit_nue_vec = ROOT.TVectorD(nue_spec.GetNbinsX())
    B_nue_matrix  = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        N_fit_nue_vec[i] = N_fit_vec[i]
        for j in range(nue_spec.GetNbinsX()):
            B_nue_matrix[i][j] = B_matrix[i][j]
    # If in debug mode, print out this vector and matrix
    if debug:
        print("vector of fit nue bin values: ")
        N_fit_nue_vec.Print()
        print("nue block of the constrained covariance matrix, B_nue: ")
        B_nue_matrix.Print()
    
    # Return constrained prediction, covariance matrix
    return N_fit_nue_vec, B_nue_matrix
## End definition of runMBConstraint


def runNewConstraint(nue_spec, numu_spec, covar, numu_data_spec, debug=False):

    ## Function that calculates the constrained nue prediction and covariance matrix using the "new" Xin/Matt/Mike 2020 method
    ## Inputs:
    ##   nue_spec          nue MC spectrum (TH1D)
    ##   numu_spec         numu MC spectrum (TH1D)
    ##   covar             joint nue+numu covariance marix (TMatrixT<double>) (note: for agreed-upon procedure, this should have stats added to the numu component but not the nue component)
    ##   numu_data_spec    numu data spectrum (TH1D)
    ##   debug             flag for whether to print out various debugging information
    ## Returns:
    ##   constr_nue_vec       constrained nue spectrum (TVectorT<double>)
    ##   constr_covar_nue     constrained nue covariance matrix (TMatrixT<double>) (note: *not* fractional)
    
    
    # If operating in debug mode, print out information on inputs
    if debug:
        print("nue spectrum: ", [ nue_spec.GetBinContent(i+1) for i in range(nue_spec.GetNbinsX()) ])
        print("numu spectrum: ", [ numu_spec.GetBinContent(i+1) for i in range(numu_spec.GetNbinsX()) ])
        print("numu data spectrum: ", [ numu_data_spec.GetBinContent(i+1) for i in range(numu_data_spec.GetNbinsX()) ])
        print("covariance matrix: ")
        covar.Print()

    # Take the standard covariance matrix and break it into its block components
    covar_ee = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            covar_ee[i][j] = covar[i][j]
    covar_em = ROOT.TMatrixD(nue_spec.GetNbinsX(),numu_spec.GetNbinsX())
    covar_me = ROOT.TMatrixD(numu_spec.GetNbinsX(),nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        for j in range(numu_spec.GetNbinsX()):
            covar_em[i][j] = covar[i][nue_spec.GetNbinsX()+j]
            covar_me[j][i] = covar[i][nue_spec.GetNbinsX()+j]
    covar_mm = ROOT.TMatrixD(numu_spec.GetNbinsX(),numu_spec.GetNbinsX())
    for i in range(numu_spec.GetNbinsX()):
        for j in range(numu_spec.GetNbinsX()):
            covar_mm[i][j] = covar[nue_spec.GetNbinsX()+i][nue_spec.GetNbinsX()+j]
    # If in debug mode, print these matrices and their first diagonal elements
    if debug:
        print("covariance matrix ee: ")
        covar_ee.Print()
        print(covar_ee[0][0])
        print("covariance matrix em: ")
        covar_em.Print()
        print(covar_em[0][0])
        print("covariance matrix me: ")
        covar_me.Print()
        print(covar_me[0][0])
        print("covariance matrix mm: ")
        covar_mm.Print()
        print(covar_mm[0][0])

    # Compute the constrained nue prediction as mu_e^{constrained} = mu_e + covar_em*(covar_mm)^{-1}*(X_m - mu_m)...
    #   where mu are the predicted spectra (N^{MC}), X are the observed spectra (N^{data}), and the covar are the blocks of the covariance matrix as defined above
    diff_vec = ROOT.TMatrixD(numu_spec.GetNbinsX(),1)  # diff_vec = X_m - mu_m
    for i in range(numu_spec.GetNbinsX()):
        diff_vec[i][0] = numu_data_spec.GetBinContent(i+1) - numu_spec.GetBinContent(i+1)
    covar_mm_inverse = ROOT.TMatrixD(covar_mm).Invert()
    if not checkInversion(covar_mm, covar_mm_inverse, numu_spec.GetNbinsX()):
        print("Matrix covar_mm not invertable, returning...")
        return
    calc_vec1 = ROOT.TMatrixD(numu_spec.GetNbinsX(),1)  # calc_vec1 = (covar_mm)^{-1}*diff_vec
    #calc_vec1 = ROOT.TMatrixD.Mult(covar_mm_inverse, diff_vec)
    for i in range(numu_spec.GetNbinsX()):
        calc_vec1[i][0] = 0.
        for j in range(numu_spec.GetNbinsX()):
            calc_vec1[i][0] += covar_mm_inverse[i][j]*diff_vec[j][0]
    calc_vec2 = ROOT.TMatrixD(nue_spec.GetNbinsX(),1)   # calc_vec2 = covar_em*(covar_mm)^{-1}*diff_vec
    #calc_vec2 = ROOT.TMatrixD.Mult(covar_em, calc_vec1)
    for i in range(nue_spec.GetNbinsX()):
        calc_vec2[i][0] = 0.
        for j in range(numu_spec.GetNbinsX()):
            calc_vec2[i][0] += covar_em[i][j]*calc_vec1[j][0]
    constr_nue_vec = ROOT.TVectorD(nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        constr_nue_vec[i] = nue_spec.GetBinContent(i+1) + calc_vec2[i][0]
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
        constr_nue_vec.Print()

    # Compute the constrained nue covariance matrix as covar_ee^{constrained} = covar_ee - covar_em*(covar_mm)^{-1}*covar_me
    calc_mat1 = ROOT.TMatrixD(numu_spec.GetNbinsX(),nue_spec.GetNbinsX())  # calc_mat1 = (covar_mm)^{-1}*covar_me
    #calc_mat1 = ROOT.TMatrixD.Mult(covar_mm_inverse, covar_me)
    for i in range(numu_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            calc_mat1[i][j] = 0.
            for k in range(numu_spec.GetNbinsX()):
                calc_mat1[i][j] += covar_mm_inverse[i][k]*covar_me[k][j]
    calc_mat2 = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())   # calc_mat2 = covar_em*(covar_mm)^{-1}*covar_me
    #calc_mat2 = ROOT.TMatrixD.Mult(covar_em, calc_mat1)
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            calc_mat2[i][j] = 0.
            for k in range(numu_spec.GetNbinsX()):
                calc_mat2[i][j] += covar_em[i][k]*calc_mat1[k][j]
    constr_covar_nue = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            constr_covar_nue[i][j] = covar_ee[i][j] - calc_mat2[i][j]
    # If in debug mode, print these matrices out
    if debug:
        print("covar_em*(covar_mm)^{-1}*covar_me: ")
        calc_mat2.Print()
        print("constrained nue covariance matrix: ")
        constr_covar_nue.Print()
        
    # Retrun constrained prediction, covariance matrix
    return constr_nue_vec, constr_covar_nue
## End definition of runNewConstraint


def calcChi2(pred_spec, obs_spec, covar, debug=False):

    ## Function that calculates the chi2 between data and prediction
    ## Inputs:
    ##   pred_spec    predicted spectrum (python list or TVectorT<double>, *not* TH1D)
    ##   obs_spec     observed spectrum (python list or TVectorT<double>, *not* TH1D)
    ##   covar        covariance matrix for the spectra (note: should be the *total* sys+stat covariance matrix with desired type of stat errors)
    ##   debug        flag for whether to print out various debugging information
    ## Returns:
    ##   chi2         chi2 for the obs_spec compared to pred_spec with covariance matrix covar

    
    # If in debug mode, print out information on inputs
    Nbins = covar.GetNrows()
    if debug:
        print("number of bins: ", Nbins)
        print("predicted spectrum: ", [ pred_spec[i] for i in range(Nbins) ])
        print("observed spectrum: ", [ obs_spec[i] for i in range(Nbins) ])
        print("covariance matrix: ")
        covar.Print()
    
    # Invert the covariance matrix
    inverse = ROOT.TMatrixD(covar).Invert()
    # If in debug mode, print out this matrix
    if debug:
        print("inverse of the covariance matrix: ")
        inverse.Print()

    # Validate that the matrix inversion worked as expected
    if not checkInversion(covar, inverse, Nbins):
        print("Matrix covar not invertable, returning...")
        return
    
    # Calculate the chi2 with the constrained covariance matrix
    chi2 = 0.
    for i in range(Nbins):
        for j in range(Nbins):
            chi2 += ( (obs_spec[i] - pred_spec[i]) * inverse[i][j] * (obs_spec[j] - pred_spec[j]) )
    if debug:
        print("chi2: ", chi2)

    return chi2
## End definition of calcChi2

# If this is the executable...
if __name__ == "__main__":

    # Declare spectrum and covarinace matrix input files
    spec_fname = 'sens.SBNspec.root'
    covar_fname = 'total_sens.SBNcovar.root'
    data_spec_fname = 'data.SBNspec.root'
    
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
    constr_nue_spec, constr_nue_covar = runNewConstraint(spec_dict['1e1p'], spec_dict['1mu1p'], total_covar, data_spec_dict['1mu1p'], debug=True)

    print("N_fit_nue: ", [ constr_nue_spec[i] for i in range(spec_dict['1e1p'].GetNbinsX()) ])
    print("sigma_fit_nue: ", [ math.sqrt(constr_nue_covar[i][i]) for i in range(spec_dict['1e1p'].GetNbinsX()) ])
    

    print("Done!")
