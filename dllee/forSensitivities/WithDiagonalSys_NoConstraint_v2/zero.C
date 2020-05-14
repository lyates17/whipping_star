#include "TFile.h"
#include "TMatrix.h"

void zero() {

  TFile* covar_file = new TFile("sens.SBNcovar.root", "READ");
  TMatrixD* frac_covar = (TMatrixD*)covar_file->Get("frac_covariance");

  for ( int i=0; i < frac_covar->GetNrows(); i++ ) {
    for ( int j=0; j < frac_covar->GetNcols(); j++ ) {
      if ( i != j ) (*frac_covar)(i,j) = 0.;
    }
  }

  TFile* out = new TFile("sens_DiagSys.SBNcovar.root", "RECREATE");
  gDirectory->WriteObject(frac_covar, "frac_covariance");

  out->Write();
  out->Close();

  std::cout << "Done!" << std::endl;

}
