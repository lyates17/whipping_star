import ROOT
import math

def checkInversion(matrix, inverse, dim, debug=False):

    # Make copies of the matrices
    mat = ROOT.TMatrixD(matrix)
    inv = ROOT.TMatrixD(inverse)

    # Compute check1 = matrix * inverse
    check1 = ROOT.TMatrixD(mat)
    check1 *= inv

    # Compute check2 = inverse* covar
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


def calcChiWithConstraint(nue_spec, numu_spec, sys_covar, nue_data_spec, numu_data_spec, debug=True):

    ## Function that calculates the chi2 between nue data and constrained nue prediction
    ## Inputs:
    ##   nue_spec          nue MC spectrum (TH1D)
    ##   numu_spec         numu MC spectrum (TH1D)
    ##   sys_covar         joint systematic covariance marix (TMatrixT<double>)
    ##   nue_data_spec     nue data spectrum (TH1D)
    ##   numu_data_spec    numu data spectrum (TH1D)
    ##   debug             flag for whether to print out various debugging information
    ## Returns:
    ##   chi2              chi2 for nue data spec with respect to constrained nue spectrum

    
    # If operating in debug mode, print out information on inputs
    if debug:
        print("nue spectrum: ", [ nue_spec.GetBinContent(i+1) for i in range(nue_spec.GetNbinsX()) ])
        print("numu spectrum: ", [ numu_spec.GetBinContent(i+1) for i in range(numu_spec.GetNbinsX()) ])
        print("nue data spectrum: ", [ nue_data_spec.GetBinContent(i+1) for i in range(nue_data_spec.GetNbinsX()) ])
        print("numu data spectrum: ", [ numu_data_spec.GetBinContent(i+1) for i in range(numu_data_spec.GetNbinsX()) ])
        print("covariance matrix: ")
        sys_covar.Print()

    
    # 0) Add statistical uncertainty (squared) to diagonals of systematics covariance matrix
    #      "Data-like" statistical uncertaintites => N_i
    #covar = ROOT.TMatrixD(sys_covar)
    #for i in range(nue_spec.GetNbinsX()):
    #    covar[i][i] += nue_spec.GetBinContent(i+1)
    #for i in range(numu_spec.GetNbinsX()):
    #    covar[i+nue_spec.GetNbinsX()][i+nue_spec.GetNbinsX()] += numu_spec.GetBinContent(i+1)
    # If operating in debug mode, print out this covariance matrix too
    #if debug:
    #    print("covariance matrix with stat error added: ")
    #    covar.Print()

    # 1) Take the standard covariance matrix and invert it
    covar = ROOT.TMatrixD(sys_covar)  # define it here since we're removing the stat error
    inverse = ROOT.TMatrixD(covar).Invert()
    # If in debug mode, print the inverse matrix and the first diagonal element in the numu block
    if debug:
        print("inverse of covariance matrix: ")
        inverse.Print()
        print(inverse[nue_spec.GetNbinsX()][nue_spec.GetNbinsX()])

    # 1a) Validate that the matrix inversion worked as expected
    #sn = 1e-16
    if not checkInversion(covar, inverse, nue_spec.GetNbinsX()+numu_spec.GetNbinsX()):
        print("Matrix not invertable, returning...")
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
        print("Matrix not invertable, returning...")
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
    # 4b) Calculate the vector N^{fit} by multiplying B*(C^{-1}*N^{MC})...
    N_fit_vec = ROOT.TVectorD(nue_spec.GetNbinsX()+numu_spec.GetNbinsX())
    calc_vec = ROOT.TVectorD(nue_spec.GetNbinsX()+numu_spec.GetNbinsX())
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

    # 5) Get the nue block of the constrained covariance matrix
    B_nue_matrix = ROOT.TMatrixD(nue_spec.GetNbinsX(),nue_spec.GetNbinsX())
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            B_nue_matrix[i][j] = B_matrix[i][j]
    # If in debug mode, print out this matrix
    if debug:
        print("nue block of the constrained covariance matrix, B_nue: ")
        B_nue_matrix.Print()
    # 5a) *Now* add the statistical error in -- using Pearson-like stat error for now
    for i in range(nue_spec.GetNbinsX()):
        B_nue_matrix[i][i] += N_fit_vec[i]

    
    # Calculate the chi2 with the constrained covariance matrix...
    # Invert the nue block of the constrained covarinace matrix (with statistical error added!)
    B_nue_matrix_inverse = ROOT.TMatrixD(B_nue_matrix).Invert()
    # If in debug mode, print out this matrix
    if debug:
        print("inverse of the nue block of the constrained covariance matrix, B_nue_inverse: ")
        B_nue_matrix_inverse.Print()
    # Validate that the matrix inversion worked as expected
    if not checkInversion(B_nue_matrix, B_nue_matrix_inverse, nue_spec.GetNbinsX()):
        print("Matrix not invertable, returning...")
        return
    # Use the above to calculate the chi2
    chi2 = 0.
    for i in range(nue_spec.GetNbinsX()):
        for j in range(nue_spec.GetNbinsX()):
            chi2 += ( (nue_data_spec.GetBinContent(i+1) - N_fit_vec[i]) * B_nue_matrix_inverse[i][j]
                          * (nue_data_spec.GetBinContent(j+1) - N_fit_vec[j]) )
    if debug:
        print("chi2: ", chi2)

    
    # Return constrained prediction, uncertanties
    return chi2

## End definition of runConstraint


# If this is the executable...
if __name__ == "__main__":

    # Declare spectrum and covarinace matrix input files
    spec_fname = 'set1/sens_pred.SBNspec.root'
    covar_fname = 'set1/total_sens_pred.SBNcovar.root'
    data_spec_fname = 'set1/fakedata.SBNspec.root'
    
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

    # Get the total, individual covariance matrices
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
        if sel not in data_spec_dict: data_spec_dict[sel] = data_spec_file.Get(k)
        else: data_spec_dict[sel].Add(data_spec_file.Get(k))

    # Run the constraint and calculate chi2
    chi2 = calcChiWithConstraint(spec_dict['1e1p'], spec_dict['1mu1p'], total_covar, data_spec_dict['1e1p'], data_spec_dict['1mu1p'], debug=True)
