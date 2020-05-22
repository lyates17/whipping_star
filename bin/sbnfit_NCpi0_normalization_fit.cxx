#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <vector>
#include <unistd.h>
#include <getopt.h>
#include <cstring>
#include <gsl/gsl_math.h>
#include <gsl/gsl_interp2d.h>
#include <gsl/gsl_spline2d.h>

#include "TFile.h"
#include "TTree.h"
#include "TH1F.h"
#include "TH2D.h"
#include "THStack.h"
#include "TLegend.h"
#include "TMultiGraph.h"
#include "TString.h"
#include "TNtuple.h"
#include "TChain.h"
#include "TMath.h"
#include "TSystem.h"
#include "TMatrixT.h"
#include "TObjArray.h"
#include "TList.h"
#include "TRandom.h"
#include "TError.h"
#include "TCanvas.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TROOT.h"
#include "TMarker.h"

#include "params.h"
#include "SBNconfig.h"
#include "SBNchi.h"
#include "SBNspec.h"
#include "SBNosc.h"
#include "SBNfit.h"
#include "SBNfit3pN.h"
#include "SBNcovariance.h"
#include "SBNfeld.h"


#define no_argument 0
#define required_argument 1
#define optional_argument 2

using namespace sbn;

/*************************************************************
 *************************************************************
 *		BEGIN sbnfit_make_covariance.cxx
 ************************************************************
 ************************************************************/
int main(int argc, char* argv[])
{

    std::string xml = "oscillate_example.xml";

    /*************************************************************
     *************************************************************
     *		Command Line Argument Reading
     ************************************************************
     ************************************************************/
    const struct option longopts[] =
    {
        {"xml", 		required_argument, 	0, 'x'},
        {"printall", 		no_argument, 		0, 'p'},
        {"stat", 		no_argument, 		0, 's'},
        {"montecarlo", 		required_argument,	0, 'm'},
        {"data", 		required_argument,	0, 'd'},
	{"interpolation",       required_argument,      0, 'i'},
	{"totcovarmatrix",      required_argument,      0, 't'},
	{"detmatrix",           required_argument,      0, 'c'},
	{"geniematrix",         required_argument,      0, 'g'},
	{"flat",        required_argument, 0 ,'f'},
        {"randomseed",        required_argument, 0 ,'r'},
        {"help", 		no_argument,	0, 'h'},
        {0,			    no_argument, 		0,  0},
    };

    int iarg = 0;
    opterr=1;
    int index;

    //a tag to identify outputs and this specific run. defaults to EXAMPLE1
    std::string tag;
    bool bool_stat_only = false;
    int interpolation_number = -99;  //number of points for chi2 value interpolation
    double random_number_seed = -1;

    bool input_data = false;
    std::string data_filename;
    std::string mc_filename;
    std::string totcovmatrix_file;  //root file containing total covariance matrix
    std::string genie_matrix_file;  //root file containing flux/XS covariance matrix
    std::string det_matrix_file; //root file containing each det syst covar matrix;

    bool bool_flat_det_sys = false;
    double flat_det_sys_percent = 0.0;

    while(iarg != -1)
    {
        iarg = getopt_long(argc,argv, "d:x:m:r:t:c:g:p:i:f:sh", longopts, &index);

        switch(iarg)
        {
            case 'x':
                xml = optarg;
                break;
            case 'd':
                input_data = true;
                data_filename = optarg;
                break;
	    case 'm':
		mc_filename = optarg;
		break;
	    case 'i':
		interpolation_number = (int)strtod(optarg, NULL);
		break;
	    case 't':
		totcovmatrix_file = optarg;
		break;
	    case 'c':
		det_matrix_file = optarg;
		break;
	    case 'g':
		genie_matrix_file = optarg;
		break;
            case 'f':
                bool_flat_det_sys = true;
                flat_det_sys_percent = (double)strtod(optarg,NULL);
                break;
            case 'r':
                random_number_seed = (double)strtod(optarg,NULL);
                std::cout<<"Reading in random seed argument: "<<random_number_seed<<std::endl;
                break;
            case 's':
                bool_stat_only = true;
                break;
            case '?':
            case 'h':
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"sbnfit_fraction_fit is a work in progress."<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"--- Required arguments: ---"<<std::endl;
                std::cout<<"\t-x\t--xml\t\tInput configuration .xml file for SBNconfig"<<std::endl;
                std::cout<<"\t-d\t--data\t\tInput observed data for a global scan"<<std::endl;
                std::cout<<"\t-m\t--montecarlo\t\tInput monte carlo for global scan"<<std::endl;
		std::cout<<"\t-i\t--interpolation\t\tInput number of points for interpolation"<< std::endl;
		std::cout<<"\t-c\t--covariance matrix\t\tInput syst covariance matrix for global scan"<< std::endl;
		std::cout<<"\t-g\t--FluxXS covariance matrix\t\tInput FluxXS covariance matrix to extract genie matrix"<< std::endl;
                std::cout<<"\t-f\t--flat\t\t Input flat systematic fractional covariance matrix"<<std::endl;
                std::cout<<"--- Optional arguments: ---"<<std::endl;
                std::cout<<"\t-s\t--stat\t\tStat only runs"<<std::endl;
                std::cout<<"\t-r\t--randomseed\t\tRandomNumber Seed (default from machine)"<<std::endl; 
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

    std::cout<<"Begining Fraction Fit"<<std::endl;

    NGrid mygrid;

    //now only available for 2 subchannels only
    mygrid.AddDimension("NCPi0Coh", 0., 5., 0.05); //0.1full
    //mygrid.AddFixedDimension("NCPi0Coh", 1.0);   //fixed
    mygrid.AddDimension("NCPi0NotCoh", 0.5, 1.25, 0.01);   //0.1 FULL


    std::cout << "Fraction Fit|| "<< "\tStart initializing MC and data spectrum" << std::endl;

    //initialize the MC spectrum
    SBNspec mc_spec(mc_filename, xml);
    mc_spec.CollapseVector();

    //initlaize the data spectrum
    SBNspec data_spec(data_filename, xml);
    data_spec.CollapseVector();  //collapse full vector
   
 

   std::cout<< "Fraction Fit||" << "\tGrab info of the grid"<< std::endl;
   //check grid size
   std::vector<std::vector<double>> grid = mygrid.GetGrid();
   if(grid.size() != mygrid.f_num_total_points){
	std::cout <<  "the number of points don't match: something wrong with the grid setup!!" << std::endl;
	return 1;
   }

   //collect the name of dimensions: subchannels you want to vary; and the range
   std::vector<std::string> dimension_name;
   const double range_x_low = mygrid.f_dimensions.at(0).f_min;
   //const double range_x_up = mygrid.f_dimensions.at(0).f_max+1;
   const double range_x_up = mygrid.f_dimensions.at(0).f_max;
   const double range_y_low = mygrid.f_dimensions.at(1).f_min;
   const double range_y_up = mygrid.f_dimensions.at(1).f_max;
   int nbin_x = mygrid.f_dimensions.at(0).f_N;  //number of point in x axis
   int nbin_y = mygrid.f_dimensions.at(1).f_N;  
 
   dimension_name.clear(); 
   for(int i=0; i< mygrid.f_num_dimensions ; i++){
	dimension_name.push_back(mygrid.f_dimensions.at(i).f_name);
   }



   TFile* f_output = new TFile("chi_contour.root", "recreate");
   TH2D* h_chi2_inter=NULL;  
   //CNP chi
   TH2D* h_CNPchi2_raw = new TH2D("h_CNPchi2_raw", Form("h_CNPchi2_raw;%s;%s",dimension_name[0].c_str(), dimension_name[1].c_str()), nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up);
   TH2D* h_CNPchi2_delta = new TH2D("h_CNPchi2_delta", Form("h_CNPchi2_delta;%s;%s",dimension_name[0].c_str(), dimension_name[1].c_str()), nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up);



    std::cout << "Fraction Fit||" <<  "\tInitialize fractional systematric covariance matrix" << std::endl;
    //initialize covariance matrix
    TMatrixT<double> frac_GENIE_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);  //fractional genie covariance matrix
    TMatrixT<double> frac_det_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);  // one det syst covariance matrix
    TMatrixT<double> frac_syst_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);    //fractional covariance matrix other than genie
    TMatrixT<double> frac_total_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);  //fractional total covariance matrix
    frac_GENIE_matrix.Zero();
    frac_det_matrix.Zero();

    if(bool_stat_only){
    	frac_syst_matrix.Zero();
        std::cout<<"RUNNING Stat Only!"<<std::endl;
    }else if(bool_flat_det_sys){
	std::cout << "RUNNING with flat systematics: " << flat_det_sys_percent << "%!" << std::endl;
	frac_syst_matrix.Zero();
	//set up flat fractional syst covariance
	for(int i=0 ; i< mc_spec.num_bins_total; i++)
		for(int j=0;j<mc_spec.num_bins_total; j++)
			frac_syst_matrix(i,j)=flat_det_sys_percent*flat_det_sys_percent/10000.;
    }
    else{
	std::cout<< "RUNNING with Systematics!" << std::endl;
	frac_syst_matrix.Zero();


	std::cout << "Open covariance matrix root file: " << totcovmatrix_file << std::endl;
	TFile* f_covar = new TFile(totcovmatrix_file.c_str(), "read");
	TMatrixT<double>* frac_temp=(TMatrixT<double>*)f_covar->Get("frac_covariance");
	frac_total_matrix = *frac_temp;


/*	TFile* f_det = new TFile(det_matrix_file.c_str(), "read");
	frac_temp = (TMatrixT<double>*)f_det->Get("frac_covariance");
	frac_det_matrix = *frac_temp;
        f_det->Close();
*/	
/*	for(int i=0; i<mc_spec.num_bins_total; i++){
	 for(int j=0; j<mc_spec.num_bins_total;j++){
		//zero out off-diagonal elements
		if(i !=j ) frac_total_matrix(i,j)=0.0;

		//zero out correlation between 1p and 0p component
		//if((i < mc_spec.num_bins_total/2) && (j >= mc_spec.num_bins_total/2)){
		//	frac_total_matrix(i,j)=0.0;
		//	frac_total_matrix(j,i)=0.0;
		//}
	 }
	}
*/	
	

	//in case we want to move some parts of a covariance matrix
	//as in NC pi0 fit, where we want to remove cross section error of NC pi0 COH and non-COH
	TFile* f_genie = new TFile(genie_matrix_file.c_str(), "read");

        TMatrixT<double>* UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/All_UBGenie_frac_covariance");
        frac_GENIE_matrix = *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/AxFFCCQEshape_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/DecayAngMEC_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/NormCCCOH_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/NormNCCOH_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/RPA_CCQE_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/Theta_Delta2Npi_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/VecFFCCQEshape_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;
        UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/XSecShape_CCMEC_UBGenie_frac_covariance");
        frac_GENIE_matrix += *UBGenie_temp;

	//fix the nan in genie matrix
	for(int i=0; i<mc_spec.num_bins_total; i++){
         for(int j=0; j<mc_spec.num_bins_total;j++){
		if(std::isnan(frac_GENIE_matrix(i,j))) frac_GENIE_matrix(i,j) = 0.0;
 	 }
	}

	frac_syst_matrix = frac_total_matrix - frac_det_matrix - frac_GENIE_matrix;

        //UBGenie_temp = (TMatrixT<double>*)f_genie->Get("individualDir/NormNCCOH_UBGenie_frac_covariance");
        //frac_GENIE_matrix -= *UBGenie_temp;

	//start of simply subtracting GENIE part of NC pi0
	//locate any bin related to grid
	/*std::vector<bool> xsec_bin;
	xsec_bin.clear();

	for(auto hist:mc_spec.hist){

		bool has_axis_name = false;
		std::string hist_name = hist.GetName();
		for(int i=0; i< mygrid.f_num_dimensions; i++){
			std::string axis_name = mygrid.f_dimensions.at(i).f_name;

			if(hist_name.find(axis_name) != std::string::npos){
				 has_axis_name=true;
				 break;
			}
		}
		std::cout << has_axis_name <<std::endl;
		if(has_axis_name){ for(int i =0; i< hist.GetNbinsX(); i++) xsec_bin.push_back(true);}
		else{ for(int i =0 ; i<hist.GetNbinsX(); i++) xsec_bin.push_back(false);}
	}

	if(xsec_bin.size() != mc_spec.num_bins_total){
		std::cout << "Something wrong with counting NBins of histogram"<< std::endl;
		return 1;
	}

	std::cout << "Subtracting cross section error of NC pi0" << std::endl;
	for(int i =0; i< mc_spec.num_bins_total; i++){
		for(int j=0; j< mc_spec.num_bins_total; j++){
			if(xsec_bin[i] || xsec_bin[j]) frac_syst_matrix(i,j)=(*frac_temp)(i,j)-(*UBGenie_temp)(i,j);
			else frac_syst_matrix(i,j)=(*frac_temp)(i,j);
		}
	}
	//end of simply subtracting GENIE part of NC pi0
*/	
	f_covar->Close();
	f_genie->Close();	
    }

   f_output->cd();
   frac_syst_matrix.Write("frac_other_syst_matrix");
   frac_GENIE_matrix.Write("frac_GENIE_matrix");

   std::cout << "Fraction Fit||"<<  "\tStart GLOBAL SCAN" <<std::endl;
   std::vector<double> chi_CNP;  //vector to save CNP chi square values.
   std::vector<double> last_chi_CNP;  //vector to save CNP chi square values.
   chi_CNP.reserve(grid.size()); 

   //do iterative fit
   int iterative_number = 5;  //max number of iteration
   double chi_square_tolerance = 1e-3;
   bool chi_converged = false;
   int best_fit, last_best_fit;
   double best_chi,last_best_chi;	
   //CNP Chi calculation
   SBNchi chi_CNP_temp(xml);
   //covariance matrix
   TMatrixT<double> full_syst(mc_spec.num_bins_total, mc_spec.num_bins_total);
   TMatrixT<double> genie_syst(mc_spec.num_bins_total, mc_spec.num_bins_total);
   TMatrixT<double> collapsed_temp(mc_spec.num_bins_total_compressed, mc_spec.num_bins_total_compressed);
   TMatrixT<double> collapsed_syst(mc_spec.num_bins_total_compressed, mc_spec.num_bins_total_compressed);
   TMatrixT<double> invert_collapsed_temp(mc_spec.num_bins_total_compressed, mc_spec.num_bins_total_compressed);


   SBNspec mc_bkg(mc_filename,xml, false);   // (constrained) background
   mc_bkg.Scale("NCDeltaRadOverlayLEE", 0.0); 
   for(int n_iter = 0; n_iter<iterative_number; n_iter++){ 
		

	   if(n_iter == 0){
		SBNspec mc_copy(mc_filename, xml, false);
		mc_copy.Scale("NCDeltaRadOverlayLEE", 0.0);  //do not included 2x NCdelta in the mc ---> null hypothesis


		full_syst = chi_CNP_temp.FillSystMatrix(frac_syst_matrix, mc_copy.full_vector);

		for(int i=0; i< mygrid.f_num_dimensions; i++){
			SBNspec comp(mc_filename, xml, false);
			comp.Keep(dimension_name[i], 1.0);
	
			genie_syst = chi_CNP_temp.FillSystMatrix(frac_GENIE_matrix,comp.full_vector);
			f_output->cd();
                        genie_syst.Write(Form("genie_%s_%d", dimension_name[i].c_str(), n_iter));

			genie_syst = chi_CNP_temp.CalcShapeOnlyCovarianceMatrix(frac_GENIE_matrix, &comp, &comp);
			full_syst += genie_syst;	
			mc_bkg.Scale(dimension_name[i], 0.0);

			f_output->cd();
			genie_syst.Write(Form("shape_genie_%s_%d", dimension_name[i].c_str(), n_iter));		
		}
		//mc_bkg.Scale("BNBOther", 0.0);
		genie_syst = chi_CNP_temp.FillSystMatrix(frac_GENIE_matrix, mc_bkg.full_vector);
		full_syst += genie_syst;

		chi_CNP_temp.CollapseModes(full_syst, collapsed_syst);

		//CNP chi square
		collapsed_temp = chi_CNP_temp.AddStatMatrixCNP(&collapsed_syst, mc_copy.collapsed_vector, data_spec.collapsed_vector);	

		//Neyman Chi square
		//collapsed_temp = chi_CNP_temp.AddStatMatrix(&collapsed_syst,data_spec.collapsed_vector);


	        //compare plots before the fit
	        tag = "before_fit";
	        std::cout << "Fraction Fit|| \tCompare the MC and data spectrum with systematic error bars with tag " << tag << std::endl;
		mc_spec.CompareSBNspecs(collapsed_syst,&data_spec, tag);
	        tag.clear();

	   }
	   else{
		SBNspec last_best_fit_spec(mc_filename, xml, false);
		last_best_fit_spec.Scale("NCDeltaRadOverlayLEE", 0.0); //do not included 2x NCdelta in the mc ---> null hypothesis

		std::vector<double> best_fit_point = grid[last_best_fit];
		for(int j=0; j<best_fit_point.size(); j++){
			last_best_fit_spec.Scale(dimension_name[j], best_fit_point[j]);			
		}

                
                full_syst = chi_CNP_temp.FillSystMatrix(frac_syst_matrix, last_best_fit_spec.full_vector);
                
                for(int i=0; i< mygrid.f_num_dimensions; i++){
                        SBNspec comp = last_best_fit_spec;
                        comp.Keep(dimension_name[i], 1.0);

			genie_syst = chi_CNP_temp.FillSystMatrix(frac_GENIE_matrix,comp.full_vector);
                        f_output->cd();
                        genie_syst.Write(Form("genie_%s_%d", dimension_name[i].c_str(), n_iter));

                        genie_syst = chi_CNP_temp.CalcShapeOnlyCovarianceMatrix(frac_GENIE_matrix, &comp, &comp);
                        full_syst += genie_syst; 

			f_output->cd();
                        genie_syst.Write(Form("shape_genie_%s_%d", dimension_name[i].c_str(), n_iter));	
                }
                genie_syst = chi_CNP_temp.FillSystMatrix(frac_GENIE_matrix, mc_bkg.full_vector);
		full_syst += genie_syst;                

		
		chi_CNP_temp.CollapseModes(full_syst, collapsed_syst);

		//CNPchi	
		collapsed_temp = chi_CNP_temp.AddStatMatrixCNP(&collapsed_syst, last_best_fit_spec.collapsed_vector, data_spec.collapsed_vector); 

		//Neyman Chi
		//collapsed_temp = chi_CNP_temp.AddStatMatrix(&collapsed_syst, data_spec.collapsed_vector);
	   }

	   //write collapsed full covariance matrix to file, for check
	   f_output->cd();
	   genie_syst.Write(Form("genie_full_otherbkg_%d", n_iter));
	   full_syst.Write(Form("syst_full_matrix_%d", n_iter));
	   collapsed_syst.Write(Form("syst_collapsed_matrix_%d", n_iter));
	   collapsed_temp.Write(Form("full_collapsed_matrix_%d", n_iter));

           invert_collapsed_temp = chi_CNP_temp.InvertMatrix(collapsed_temp);  //inverted covariance matrix


	   best_chi = DBL_MAX;
	   chi_CNP.clear();
	   SBNspec spec_temp;
	   for(int i =0; i< grid.size() ;i++){

		//set a temperary SBNspec, assume there is already a MC CV root file with corresponding sequence defined in xml	
		spec_temp=mc_spec;
		spec_temp.Scale("NCDeltaRadOverlayLEE", 0.0);

		
		//access grid point
		std::vector<double> point = grid[i];
		//scale chosen subchannels
		for(int j=0; j< point.size(); j++ ){
			spec_temp.Scale(dimension_name[j], point[j]);
		}

		//regular chi calculation
		double chi_value = chi_CNP_temp.CalcChi(invert_collapsed_temp, spec_temp.collapsed_vector, data_spec.collapsed_vector);
		chi_CNP.push_back(chi_value);
	
		if(chi_value < best_chi){
			best_chi = chi_value;
			best_fit = i;
		}


	   }
	   std::cout << "On iteration " << n_iter << ", minimum chi square value " << best_chi; 
	   if(chi_converged) break;

	   if(n_iter != 0){
		if(abs(best_chi - last_best_chi) < chi_square_tolerance) chi_converged = true;
	   }

	   last_best_chi = best_chi;
	   last_best_fit = best_fit;
	   last_chi_CNP = chi_CNP;

	   std::cout << " And chi value is converged: " << chi_converged << std::endl;

   }


   //compare spectrum between data and the best fit point of CNP chi
   SBNspec best_spec(mc_filename, xml, false);
   std::vector<double> best_point = grid[best_fit];
   for(int i=0; i< best_point.size(); i++ ){
                best_spec.Scale(dimension_name[i], best_point[i]);
   }
   std::cout << "Fraction Fit||" <<  "\tBest Fit Point: (" << best_point[0] << ", " << best_point[1] << ")"<<std::endl;
   tag = "best_fit";
   std::cout << "Fraction Fit || \t Compare data and MC spectrum at the best-fit point with tag " << tag<<std::endl;
   best_spec.CompareSBNspecs(collapsed_syst, &data_spec, tag);
   tag = "NULLvsBEST";
   std::cout << "Fraction Fit || \t Compare null spectrum and the best-fit point spectrum with tag " << tag<<std::endl;
   //collapsed systematic covariance matrix at best-fit point
   mc_spec.CompareSBNspecs(collapsed_syst, &best_spec, tag);

   std::cout << "Print out delta CNP chi square for grid points now" << std::endl;
   //TH1D* h_cnp = new TH1D("h_cnp", "CNP chi; NCpi0 non-coherent; CNP chi", 300, 0, 3);
   //TH1D* h_chi = new TH1D("h_chi", "regular chi", 300, 0, 3);
   //delta chi2;
   for(int i=0; i< grid.size(); i++){
	 std::vector<double> point = grid[i];
	 
         h_CNPchi2_raw->Fill(point[0], point[1], chi_CNP[i]);

	 chi_CNP[i] -= best_chi;
	 h_CNPchi2_delta->Fill(point[0], point[1], chi_CNP[i]);
	 //h_cnp->Fill(point[1], chi_CNP[i]);
	 std::cout << "Delta CNP Chi: " << i << " " << chi_CNP[i];
	 for(int j =0;j <point.size(); j++) std::cout << " " << point[j];
	 std::cout << std::endl;
   }

 
   f_output->cd();
   //h_cnp->Write();
   //h_chi->Write();
   h_CNPchi2_raw->Write(); 
   h_CNPchi2_delta->Write();
   std::cout << "Fraction Fit||" <<  "\t End of Global Scan--CNP Chi2 calculation" << std::endl;

  /*
   //do projection to compare chi and CNP chi
   TCanvas* c_compare = new TCanvas("c_compare", "c_compare");
   h_chi->SetLineColor(kBlue);
   h_cnp->SetLineColor(kRed);
   THStack* h_stack=new THStack("h_stack", "delta chi");
   TLegend* leg = new TLegend(0.1,0.7,0.48,0.9);
   h_stack->Add(h_chi, "HIST");
   h_stack->Add(h_cnp, "HIST");
   leg->AddEntry(h_chi, "regular chi", "l");
   leg->AddEntry(h_cnp, "CNP chi", "l");
   c_compare->cd();
   h_stack->Draw("nostack");
   leg->Draw();
   h_stack->GetXaxis()->SetTitle("NC pi0 non-coherent");
   h_stack->GetYaxis()->SetTitle("delta chi");
   c_compare->Update();
   c_compare->Write();
   */




   //****************** START INTERPOLATION*********************************

   if(interpolation_number != -99){

	//the upper range of x, y axis for interpolation
	double range_x_inter = mygrid.f_dimensions.at(0).f_max - mygrid.f_dimensions.at(0).f_step;
	double range_y_inter = mygrid.f_dimensions.at(1).f_max - mygrid.f_dimensions.at(1).f_step;
	std::cout << "range x interpolation " << range_x_inter << " Y: "<< range_y_inter <<std::endl;

	//save interpolated 2D plot
   	h_chi2_inter = new TH2D("h_chi2_interpolation", Form("delta CNP chi interpolation;%s;%s", dimension_name[0].c_str(), dimension_name[1].c_str()), interpolation_number, range_x_low,range_x_inter, interpolation_number, range_y_low, range_y_inter);
	//h_chi2_inter->SetMinimum(-1);


	std::cout << "Fraction Fit||" << "\tStart interpolation of CNP chi2 with number "<< interpolation_number <<std::endl;
   	const gsl_interp2d_type *T = gsl_interp2d_bicubic;
	std::vector<double> grid_x;   //to save grid point values.
	std::vector<double> grid_y;
	grid_x = mygrid.f_dimensions.at(0).f_points;  //initialize grid point
	grid_y = mygrid.f_dimensions.at(1).f_points;   //initialize grid point
	//double x_step = fabs(range_x_low - range_x_inter)/(double)interpolation_number;
	//double y_step = fabs(range_y_low - range_y_inter)/(double)interpolation_number;
	double x_step = fabs(range_x_low - range_x_inter)/(interpolation_number - 1.);
	double y_step = fabs(range_y_low - range_y_inter)/(interpolation_number - 1.);
	std::cout << "Step size X:" << x_step << " Step size Y:" << y_step <<std::endl;

  	gsl_spline2d *spline = gsl_spline2d_alloc(T, nbin_y, nbin_x);  //due to the way grid points are sequenced in our code, we change the y and x position in gsl interpolation

  	gsl_interp_accel *xacc = gsl_interp_accel_alloc();
  	gsl_interp_accel *yacc = gsl_interp_accel_alloc();

	/* initialize interpolation */
	gsl_spline2d_init(spline,  &grid_y[0], &grid_x[0], &chi_CNP[0] , nbin_y, nbin_x);


	/* interpolate N values in x and y and print out grid for plotting */
	for (int i = 0; i < interpolation_number; i++){

	      double xi;

	      if(i == (interpolation_number -1)) xi = range_x_low + (i-0.5)*x_step;  //to fill the last bin
	      else xi = range_x_low + i*x_step;
	      //if(xi > range_x_inter) continue;  //skip points that are out of bounds

	      for (int j = 0; j < interpolation_number; j++)
		{

		  double yj;
	          if(j == (interpolation_number -1)) yj = range_y_low + (j-0.5)*y_step;
	          else yj = range_y_low + j*y_step;
		  //if(yj > range_y_inter) continue;   //skip points that are out of bounds

		  double zij = gsl_spline2d_eval(spline, yj, xi, yacc, xacc);  //again, y and x values are exchanged here

		  h_chi2_inter->Fill(xi, yj, zij);

		  //std::cout << "Interpolated value: " << zij << " ||Grid Point:(" << xi << ", " << yj << ")" << std::endl; 
		}
	}

	  f_output->cd();
	  h_chi2_inter->Write();

	  gsl_spline2d_free(spline);
	  gsl_interp_accel_free(xacc);
	  gsl_interp_accel_free(yacc);
	  
         std::cout << "Fraction Fit||" << "\tFinish interpolation of CNP chi2 with number "<< interpolation_number <<std::endl;
  }
  else{ 
	h_chi2_inter = (TH2D*)h_CNPchi2_delta->Clone();
  }

   //*****************END OF INTERPOLATION*************************************************






  //****************draw contour, get range for fraction fit****************************

   std::cout << "Fraction Fit||" <<  "\tDraw contours"<<std::endl;
   // empty TH2D to draw x & y axis on canvas
   TH2D* hr = NULL;
   if(interpolation_number != -99)
	hr = new TH2D("hr", Form("contour;%s;%s", dimension_name[0].c_str(), dimension_name[1].c_str()), interpolation_number, range_x_low,range_x_up, interpolation_number, range_y_low, range_y_up);
   else hr = new TH2D("hr", Form("contour;%s;%s", dimension_name[0].c_str(), dimension_name[1].c_str()), nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up);
   hr->SetStats(kFALSE);

   TGraph* c_graph=NULL;
   TGraph* temp_graph = NULL;
   TList* con_list=NULL;
   TMarker* marker = new TMarker(best_point[0], best_point[1], 29);  // a marker at best fit point
   marker->SetMarkerSize(2);

   //std::vector<double> contour{2.30, 4.61,6.18,11.83}; // chi2 value for 2 dof with 1 sigma, 90%, 2 sigma and 3 sigma confidence level
   //std::vector<std::string> CL_string{"1sigma", "90", "2sigma", "3sigma"};
   std::vector<double> contour{2.30, 6.18,11.83}; // chi2 value for 2 dof with 1 sigma, 90%, 2 sigma and 3 sigma confidence level
   std::vector<std::string> CL_string{"1sigma", "2sigma", "3sigma"};
   TCanvas* c = new TCanvas("c", "c");
   h_chi2_inter->SetContour((int)contour.size(), &contour[0]);
   h_chi2_inter->Draw("CONT Z LIST");//"LIST" generates a list of TGraph for each contour
   c->Update();
   f_output->cd();
   c->Write("contour");

   //grab contour object
   TObjArray *conts = (TObjArray*)gROOT->GetListOfSpecials()->FindObject("contours");
   TCanvas* v_canvas[conts->GetSize()];
	
   //hr->Draw();

   //loop over contours
   for(int i=0; i<conts->GetSize(); i++){
	con_list = (TList*)conts->At(i);   //a list of TGraph for i'th contour.
	std::cout << "Contour Z=" << contour[i] << " has "<< con_list->GetSize() << " enclosed region(s)! " << std::endl;

	double x_min = DBL_MAX;
	double x_max = DBL_MIN;
	double y_min = DBL_MAX;
	double y_max = DBL_MIN;

	v_canvas[i] = new TCanvas(Form("c_%s", CL_string[i].c_str()), Form("c_%s", CL_string[i].c_str()));
	hr->SetTitle(Form("%s_contour", CL_string[i].c_str()));
	hr->Draw();
	marker->Draw();
	c_graph = (TGraph*)con_list->First();  //grab the TGraph
	

	for(int j=0; j< con_list->GetSize() ; j++){
		temp_graph= (TGraph*)c_graph->Clone();
                temp_graph->Draw("C");
		//std::cout << "TGraph "<< j << ": number of points " << copy_graph->GetN() << std::endl;
			
		// grab x ,y coordinate
		double x,y;
		for(int k =0; k< temp_graph->GetN(); k++){
			temp_graph->GetPoint(k, x, y);
			if(x < x_min) x_min = x;
			if(x > x_max) x_max = x;

			if(y < y_min) y_min =y;
			if(y > y_max) y_max = y;
		}
	
		
		//move to next graph
		c_graph=(TGraph*)con_list->After(c_graph);
	}

	v_canvas[i]->Update();
	f_output->cd();
	v_canvas[i]->Write();

	std::cout << "Contour " << CL_string[i] << ": " << contour[i] << std::endl;
	std::cout << "range for x :" << x_min << "~" << x_max << std::endl;
	std::cout << "range for y : " << y_min << "~" << y_max << std::endl;
   } // contour loop

    f_output->Close(); 

    std::cout << "Fraction Fit||" << "\tFinish drawing contours"<<std::endl;
    std::cout << "Fraction Fit||" << "\tFinished" <<std::endl;
    std::cout << "Total wall time: " << difftime(time(0), start_time)/60.0 << " Minutes.\n";
    return 0;

}

