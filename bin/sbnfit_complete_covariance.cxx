#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <vector>
#include <unistd.h>
#include <getopt.h>
#include <cstring>

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TString.h"
#include "TNtuple.h"
#include "TChain.h"
#include "TMath.h"
#include "TSystem.h"
#include "TMatrixT.h"
#include "TRandom.h"
#include "TError.h"
#include "TCanvas.h"
#include "TH2F.h"
#include "TGraph.h"

#include "params.h"
#include "SBNconfig.h"
#include "SBNchi.h"
#include "SBNspec.h"
#include "SBNosc.h"
#include "SBNfit.h"
#include "SBNfit3pN.h"
#include "SBNcovariance.h"

#define no_argument 0
#define required_argument 1
#define optional_argument 2

using namespace sbn;

/*************************************************************
 *************************************************************
 *		BEGIN sbnfit_complete_covariance.cxx
 ************************************************************
 ************************************************************/
int main(int argc, char* argv[])
{

    std::string xml = "example.xml";

    /*************************************************************
     *************************************************************
     *		Command Line Argument Reading
     ************************************************************
     ************************************************************/
    const struct option longopts[] =
    {
        {"xml", 		required_argument, 	0, 'x'},
        {"tag", 		required_argument,	0, 't'},
        {"signal", 		required_argument,	0, 's'},
    	{"covar",		required_argument,    0, 'c'},
        {"help", 		no_argument,	0, 'h'},
        {"flat", required_argument,0,'f'},
        {"zero",no_argument,0,'z'},
        {0,			    no_argument, 		0,  0},
    };

    int iarg = 0;
    opterr=1;
    int index;
    std::string covar_file = "Stats_Only";
    bool stats_only = true;
    std::string signal_file;

    bool bool_flat_det_sys = false;
    double flat_det_sys_percent = 0.0;

    bool remove_correlations = false;

    //a tag to identify outputs and this specific run. defaults to EXAMPLE1
    std::string tag = "TEST";

    while(iarg != -1)
    {
        iarg = getopt_long(argc,argv, "f:x:s:t:c:zh", longopts, &index);

        switch(iarg)
        {
              case 'f':
                bool_flat_det_sys = true;
                flat_det_sys_percent = (double)strtod(optarg,NULL);
                break;

            case 'x':
                xml = optarg;
                break;
            case 'z':
                remove_correlations = true; 
                break;

            case 't':
                tag = optarg;
                break;
     	    case 'c':
    	        covar_file=optarg;
                stats_only = false;
	          break;
            case 's':
                signal_file = optarg;
                break;

            case '?':
            case 'h':
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"sbnfit_complete_covariance completes the set of covariance matrices from an input SBNcovar.root file"<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"--- Required arguments: ---"<<std::endl;
                std::cout<<"\t-x\t--xml\t\tInput configuration .xml file for SBNconfig"<<std::endl;
                std::cout<<"\t-t\t--tag\t\tA unique tag to identify the outputs [Default to TEST]"<<std::endl;
                std::cout<<"\t-s\t--signal\t\tInput signal SBNspec.root file"<<std::endl;
                std::cout<<"\t-c\t--covarance\t use this root file for a covariance matrix" << std::endl;
                std::cout<<"--- Optional arguments: ---"<<std::endl;
                std::cout<<"\t-f\t--flat\t\tAdd a flat percent systematic to fractional covariance matrix (all channels) (default false, pass in percent, i.e 5.0 for 5\% experimental)"<<std::endl;
                std::cout<<"\t-z\t--zero\t\tZero out all off diagonal elements of the systematics covariance matrix (default false, experimental!)"<<std::endl;
                std::cout<<"\t-h\t--help\t\tThis help menu."<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;

                return 0;
        }
    }
    /*************************************************************
     *************************************************************
     *			Main Program Flow
     ************************************************************
     ************************************************************/
    time_t start_time = time(0);

    std::cout<<"Begining covariance calcluations for tag: "<<tag<<std::endl;
    
    std::cout<<"Loading SBNspec file : "<<signal_file<<" with xml "<<xml<<std::endl;
    SBNspec sig(signal_file,xml);
    
    std::cout<<"Loading fractional covariance matrix from "<<covar_file<<std::endl;

    TFile * fsys;
    TMatrixD * cov;
    
    if(!stats_only){
        fsys = new TFile(covar_file.c_str(),"read");
        cov = (TMatrixD*)fsys->Get("frac_covariance");
   
        TMatrixD frac_flat_matrix(sig.num_bins_total, sig.num_bins_total);
        if(bool_flat_det_sys){
            std::cout << "RUNNING with flat systematics: " << flat_det_sys_percent << "%!" << std::endl;
            frac_flat_matrix.ResizeTo(sig.num_bins_total,sig.num_bins_total);
            frac_flat_matrix.Zero();
            for(int i=0 ; i< sig.num_bins_total; i++){
                   frac_flat_matrix(i,i)=flat_det_sys_percent*flat_det_sys_percent/10000.;
            }
            (*cov) = (*cov)+(frac_flat_matrix);
        }


        if(remove_correlations){
            std::cout<<"WARNING! We are running in   `Remove All Off Diagional Covariances/Correlations Mode` make sure this is what you want. "<<std::endl;
            for(int i=0; i<sig.num_bins_total;i++){ 
                for(int j=0; j<sig.num_bins_total;j++){ 
                    if(i==j)continue;
                    (*cov)(i,j) =0.0;
                }
            }
        }

       int num_nans = 0;
       for(int i=0; i<sig.num_bins_total;i++){ 
                for(int j=0; j<sig.num_bins_total;j++){ 
                    double val = (*cov)(i,j);
                    if( isinf(val) || isnan(val) || val!=val){
                            (*cov)(i,j) = 0.0;
                            num_nans++;
                    }
                }
            }
        std::cout<<"We have removed "<<num_nans<<" / "<<pow(sig.num_bins_total,2)<<" nans in the fractional covariance matrix"<<std::endl;
    }

    SBNchi collapse_chi(sig, *cov);
    TFile *fout=new TFile((tag+".SBNcovar.root").c_str(),"RECREATE");
    fout->cd();
    TMatrixD full_covariance, frac_covariance, full_correlation;
    collapse_chi.FillCovarianceMatrix(&full_covariance);
    collapse_chi.FillFractionalMatrix(&frac_covariance);
    collapse_chi.FillCorrelationMatrix(&full_correlation);
    full_covariance.Write("full_covariance",TObject::kWriteDelete);
    frac_covariance.Write("frac_covariance",TObject::kWriteDelete);
    full_correlation.Write("full_correlation",TObject::kWriteDelete);
    TMatrixD coll_covariance, coll_frac_covariance, coll_correlation;
    collapse_chi.FillCollapsedCovarianceMatrix(&coll_covariance);
    collapse_chi.FillCollapsedFractionalMatrix(&coll_frac_covariance);
    collapse_chi.FillCollapsedCorrelationMatrix(&coll_correlation);
    coll_covariance.Write("collapsed_covariance",TObject::kWriteDelete);
    coll_frac_covariance.Write("collapsed_frac_covariance",TObject::kWriteDelete);
    coll_correlation.Write("collapsed_correlation",TObject::kWriteDelete);
    fout->Close();
    
    TFile *fplots=new TFile(("SBNfit_covariance_plots_"+tag+".root").c_str(),"RECREATE");
    collapse_chi.plot_one(full_covariance,"SBNfit_covariance_matrix_"+tag,fplots,true,false,false);
    collapse_chi.plot_one(frac_covariance,"SBNfit_fractional_covariance_matrix_"+tag,fplots,true,false,false);
    collapse_chi.plot_one(full_correlation,"SBNfit_correlation_matrix_"+tag,fplots,true,false,true);
    collapse_chi.plot_one(coll_covariance,"SBNfit_collapsed_covariance_matrix_"+tag,fplots,true,false,false);
    collapse_chi.plot_one(coll_frac_covariance,"SBNfit_collapsed_fractional_covariance_matrix_"+tag,fplots,true,false,false);
    collapse_chi.plot_one(coll_correlation,"SBNfit_collapsed_correlation_matrix_"+tag,fplots,true,false,true);

    std::cout << "Total wall time: " << difftime(time(0), start_time)/60.0 << " Minutes.\n";
    return 0;

}
