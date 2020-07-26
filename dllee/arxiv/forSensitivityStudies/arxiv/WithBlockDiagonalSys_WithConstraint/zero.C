#include "TFile.h"
#include "TMatrix.h"

void zero() {

  TFile* covar_file = new TFile("sens.SBNcovar.root", "READ");
  TMatrixD* frac_covar = (TMatrixD*)covar_file->Get("frac_covariance");

  int N_1e1pBins  = 36;  // 12 bins * 3 subchannels
  int N_1mu1pBins = 9;   // 3 bins * 3 subchannels

  for ( int i=0; i < frac_covar->GetNrows(); i++ ) {
    for ( int j=0; j < frac_covar->GetNcols(); j++ ) {
      if ( (i<N_1e1pBins && j<N_1e1pBins) || (i>=N_1e1pBins && j>=N_1e1pBins) ) continue;
      (*frac_covar)(i,j) = 0.;
    }
  }

  TFile* out = new TFile("sens_BlockDiagSys.SBNcovar.root", "RECREATE");
  gDirectory->WriteObject(frac_covar, "frac_covariance");

  out->Write();
  out->Close();

  std::cout << "Done!" << std::endl;

}
