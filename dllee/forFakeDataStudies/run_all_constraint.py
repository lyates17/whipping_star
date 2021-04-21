import ROOT
import math
import os

def getSpecList(hist_list):

    ## Function that concatenates a list of TH1Ds into a python list
    ## Inputs: 
    ##   hist_list    list of spectra to be concatenated (python list of TH1Ds)
    ## Returns:
    ##   spec         concatenated spectrum (python list)

    # Initilize output spectrum
    spec = []

    # Loop over input spectra...
    for hist in hist_list:
        # Loop over bins in this spectrum...
        for i in range(hist.GetNbinsX()):
            spec.append( hist.GetBinContent(i+1) )

    # Return concatenated spectrum
    return spec
## End definition of getSpecList

def getSpecHist(spec, in_hist):

    ## Function that converts a spectrum into a TH1D
    ## Inputs: 
    ##   spec       input spectrum (python list)
    ##   in_hist    histogram to use as a template for the output (TH1D)
    ## Returns:
    ##   out_hist   input spectrum as TH1D

    # Initilize output spectrum histogram, as a copy of in_hist
    out_hist = ROOT.TH1D(in_hist)

    # Loop over input spectrum...
    for i in range(len(spec)):
        out_hist.SetBinContent(i+1, spec[i])
        out_hist.SetBinError(i+1, 0.)

    # Return spectrum histogram
    return out_hist
## End definition of getSpecList


def getFullCovar(frac_covar, spec, debug=False):

    ## Function that calcuates full covariance matrix
    ## Inputs: 
    ##   frac_covar    fractional covariance matrix (TMatrixD)
    ##   spec          spectrum (python list or similar)
    ##   debug         flag for whether to print out various debugging information
    ## Returns:
    ##   full_covar    full covariance matrix (TMatrixD)

    # If in debug mode, print out information on inputs
    if debug:
        print("spectrum: ", spec)
        print("fractional covariance matrix: ")
        print(frac_covar[0][0])
        frac_covar.Print()

    # Initialize output full covariance matrix as a copy of input fractional covariance matrix
    full_covar = ROOT.TMatrixD(frac_covar)

    # Compute M_ij = F_ij*N_i*N_j
    for i in range(full_covar.GetNrows()):
        for j in range(full_covar.GetNcols()):
            if math.isnan(full_covar[i][j]):
                # Note: Be *very careful* here if reusing this function... this ensures invertibility but may cause other problems
                if i==j:
                    full_covar[i][j] = 1.
                else:
                    full_covar[i][j] = 0.
            else:
                full_covar[i][j] *= spec[i]*spec[j]

    # If in debug mode, print out information on output
    if debug:
        print("full covariance matrix: ")
        print(full_covar[0][0])
        full_covar.Print()

    # Return full covariance matrix
    return full_covar
## End definition of getFullCovar


def getFracCovar(full_covar, spec, debug=False):

    ## Function that calcuates fractional covariance matrix
    ## Inputs: 
    ##   full_covar    full covariance matrix (TMatrixD)
    ##   spec          spectrum (python list or similar)
    ##   debug         flag for whether to print out various debugging information
    ## Returns:
    ##   frac_covar    fractional covariance matrix (TMatrixD)

    # If in debug mode, print out information on inputs
    if debug:
        print("spectrum: ", spec)
        print("full covariance matrix: ")
        print(full_covar[0][0])
        full_covar.Print()

    # Initialize output fractional covariance matrix as a copy of input full covariance matrix
    frac_covar = ROOT.TMatrixD(full_covar)

    # Compute F_ij = M_ij/(N_i*N_j)
    for i in range(full_covar.GetNrows()):
        for j in range(full_covar.GetNcols()):
            if spec[i]*spec[j] == 0.:
                frac_covar[i][j] = float('nan')
            else:
                frac_covar[i][j] *= 1./(spec[i]*spec[j])

    # If in debug mode, print out information on output
    if debug:
        print("fractional covariance matrix: ")
        print(frac_covar[0][0])
        frac_covar.Print()

    # Return fractional covariance matrix
    return frac_covar
## End definition of getFracCovar


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

    ## Function that calculates constrained nue prediction and covariance matrix using the method from docdb-32672
    ## Inputs:
    ##   nue_spec             nue MC spectrum (python list or similar)
    ##   numu_spec            numu MC spectrum (python list or similar)
    ##   covar                joint nue+numu total covariance marix (TMatrixD)
    ##                          note: this should include all systematic uncertainties and MC stat errors, but *not* data stat errors
    ##                          note: this should be the full/absolute covariance matrix, *not* fractional
    ##   numu_data_spec       numu data spectrum (python list or similar)
    ##   debug                flag for whether to print out various debugging information
    ## Returns:
    ##   constr_nue_spec      constrained nue spectrum (python list)
    ##   constr_nue_covar     constrained nue covariance matrix (TMatrixD)
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
    constr_nue_covar = ROOT.TMatrixD(Nbins_e,Nbins_e)
    for i in range(Nbins_e):
        for j in range(Nbins_e):
            constr_nue_covar[i][j] = covar_ee[i][j] - calc_mat2[i][j]
    # If in debug mode, print these matrices out
    if debug:
        print("covar_em*(covar_mm)^{-1}*covar_me: ")
        calc_mat2.Print()
        print("constrained nue covariance matrix: ")
        constr_nue_covar.Print()
        
    # Return constrained prediction, covariance matrix
    return constr_nue_spec, constr_nue_covar
## End definition of runConstraint



# If this is the executable...
if __name__ == "__main__":

    topdir = os.getcwd()

    fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]
    
    # if we want debugging info, set this to True
    debug = True

    for tag in fakedata_list:

        workdir = os.path.join(topdir, tag)
        os.chdir(workdir)
        
        # create the output files
        out_h0_spec_f = ROOT.TFile("h0_constr.SBNspec.root", "RECREATE")
        out_h1_spec_f = ROOT.TFile("h1_constr.SBNspec.root", "RECREATE")
        out_covar_f   = ROOT.TFile("h1_constr.SBNcovar.root", "RECREATE")
        # open the input files
        in_h0_spec_f   = ROOT.TFile.Open("h0_total.SBNspec.root", "READ")
        in_h1_spec_f   = ROOT.TFile.Open("h1_total.SBNspec.root", "READ")
        in_covar_f     = ROOT.TFile.Open("h1_total.SBNcovar.root", "READ")
        in_data_spec_f = ROOT.TFile.Open("data.SBNspec.root", "READ")
        
        # define helper variables...
        Nbins_1e1p = in_h1_spec_f.Get("nu_uBooNE_1e1p_nue").GetNbinsX()
        sel1e1p_keys = ["nu_uBooNE_1e1p_nue", "nu_uBooNE_1e1p_bnb", "nu_uBooNE_1e1p_lee"]
        joint_keys   = ["nu_uBooNE_1e1p_nue", "nu_uBooNE_1e1p_bnb", "nu_uBooNE_1e1p_lee", "nu_uBooNE_1mu1p_bnb"]
        
        # convert input spectra from TH1Ds to python lists
        sel1e1p_spec  = getSpecList( [ in_h1_spec_f.Get(k) for k in sel1e1p_keys ] )
        sel1mu1p_spec = getSpecList( [ in_h1_spec_f.Get("nu_uBooNE_1mu1p_bnb") ] )
        joint_spec    = getSpecList( [ in_h1_spec_f.Get(k) for k in joint_keys ] )
        sel1mu1p_data_spec = getSpecList( [ in_data_spec_f.Get("nu_uBooNE_1mu1p_data") ] )
        # convert input fractional covariance matrix to full covariance matrix
        full_covar = getFullCovar( in_covar_f.Get("frac_covariance"), joint_spec, debug=debug )
        
        # run the constraint
        constr_1e1p_spec, constr_1e1p_full_covar = runConstraint(sel1e1p_spec, sel1mu1p_spec, full_covar, sel1mu1p_data_spec, debug=debug)
        
        # convert the constrained spectra back to TH1Ds
        out_h0_hist_dict = {}
        out_h1_hist_dict = {}
        for i in range(len(sel1e1p_keys)):
            # get the key
            key = sel1e1p_keys[i]
            # get the corresponding portion of the constrained 1e1p spectrum
            out_h1_list = constr_1e1p_spec[ i*Nbins_1e1p : (i+1)*Nbins_1e1p ]
            if 'lee' not in key:
                out_h0_list = out_h1_list
            else:
                out_h0_list = [ 0. for N in out_h1_list ]
            # fill output TH1Ds based on the results of the constraint procedure
            out_h0_hist_dict[key] = getSpecHist( out_h0_list, in_h0_spec_f.Get(key) )
            out_h1_hist_dict[key] = getSpecHist( out_h1_list, in_h1_spec_f.Get(key) )                                            
        # convert the constrained full covariance matrix to a fractional covariance matrix
        constr_1e1p_frac_covar = getFracCovar( constr_1e1p_full_covar, constr_1e1p_spec, debug=debug )
        
        # write everything out
        for key in sel1e1p_keys:
            out_h0_spec_f.WriteTObject(out_h0_hist_dict[key])
            out_h1_spec_f.WriteTObject(out_h1_hist_dict[key])
        out_covar_f.WriteTObject(constr_1e1p_frac_covar, "frac_covariance")
        # close the inputs
        in_h0_spec_f.Close()
        in_h1_spec_f.Close()
        in_covar_f.Close()
        in_data_spec_f.Close()
        # close the outputs
        out_h0_spec_f.Close()
        out_h1_spec_f.Close()
        out_covar_f.Close()
        
        # after one iteration, make sure debug is off
        debug = False

    print("Done!")
