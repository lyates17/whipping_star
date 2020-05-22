#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <cmath>
#include <vector>
#include <unistd.h>
#include <getopt.h>
#include <float.h>
#include <cstring>
#include <gsl/gsl_math.h>
#include <gsl/gsl_interp2d.h>
#include <gsl/gsl_spline2d.h>

#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TH3.h"
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
        {"pullterm", 		required_argument,	0, 'p'},
        {"stat", 		no_argument, 		0, 's'},
        {"montecarlo", 		required_argument,	0, 'm'},
        {"data", 		required_argument,	0, 'd'},
	{"central_value",       required_argument,      0, 'b'},
	{"interpolation",       required_argument,      0, 'i'},
	{"covarmatrix",         required_argument,      0, 'c'},
	{"geniematrix",         required_argument,      0, 'g'},
	{"flat",        required_argument, 0 ,'f'},
        {"randomseed",        required_argument, 0 ,'r'},
 	{"verbose",             no_argument,            0, 'v'},
        {"help", 		no_argument,	0, 'h'},
        {0,			    no_argument, 		0,  0},
    };

    int iarg = 0;
    opterr=1;
    int index;

    //a tag to identify outputs and this specific run. defaults to EXAMPLE1
    std::string tag;
    bool add_pull_term = false;
    bool bool_stat_only = false;
    int interpolation_number = -99;  //number of points for chi2 value interpolation
    double random_number_seed = -1;



    bool input_data = false;
    std::string data_filename;  //root file containing data/mc spectra
    std::string mc_filename;
    std::string covmatrix_file;  //root file containing fractional covariance matrix
    std::string genie_matrix_file;  //root file containing fractional covariance matrix
    std::string pullterm_file;

    bool bool_flat_det_sys = false;
    double flat_det_sys_percent = 0.0;
	
    double f_central = -100.0;

    while(iarg != -1)
    {
        iarg = getopt_long(argc,argv, "d:x:m:b:c:g:r:p:i:f:sh", longopts, &index);

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
	    case 'b':
		f_central = (double)strtod(optarg, NULL);
		break;
	    case 'i':
		interpolation_number = (int)strtod(optarg, NULL);
		break;
	    case 'c':
		covmatrix_file = optarg;
		break;
	    case 'g':
		genie_matrix_file = optarg;
		break;
	    case 'p':
		add_pull_term = true;
		pullterm_file = optarg;
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

    std::cout<<"Begining NC delta Fit"<<std::endl;

    NGrid mygrid;

    //now only available for 2 subchannels only 
    //maybe add prior value & range
    mygrid.AddConstrainedDimension("NCPi0Coh", 0.5, 3, 0.05, 1.55, 0.5);   //0.1 FULL
    //mygrid.AddDimension("NCPi0NotCoh", 0., 3, 0.1);   //0.1 FULL
    mygrid.AddConstrainedDimension("NCPi0NotCoh", 0.5, 1.25, 0.04, 0.78, 0.1);   //0.1 FULL
    mygrid.AddDimension("NCDeltaRadOverlaySM", 0., 4, 0.02);   //0.1 FULL



    //grab the grid
    std::vector<std::vector<double>> grid = mygrid.GetGrid();
    if(grid.size() != mygrid.f_num_total_points){
	std::cout <<  "the number of points don't match: something wrong with the grid setup!!" << std::endl;
	return 1;
    }

    std::cout << "NC delta Fit|| "<< "\tStart initializing MC and data spectrum" << std::endl;
    //initialize the MC spectrum
    SBNspec mc_spec(mc_filename, xml);
    mc_spec.Scale("NCDeltaRadOverlayLEE", 0.0);
    //initialize constrained MC(include signal) & constrained background spectrum
    for(int i=0; i< mygrid.f_num_dimensions; i++){
	auto const dimension = mygrid.f_dimensions.at(i);  //grab one dimension
	if(dimension.f_has_constrain == true){
		 mc_spec.Scale(dimension.f_name, dimension.f_constrain_value);	
	}
	else{
		if(f_central >=0) mc_spec.Scale(dimension.f_name, f_central);
	}
    }
    
    //initlaize the data spectrum
    SBNspec data_spec;;
    if(!input_data){
	 std::cout << "NC delta Fit||\t No real data input, gonna do sensitivity study" << std::endl;
	 data_spec = mc_spec;
    }
    else{
	SBNspec data_temp(data_filename, xml);
	data_spec = data_temp; 
    }
    data_spec.CollapseVector();  //collapse full vector
   

    std::cout << "NC delta Fit||" <<  "\tInitialize fractional systematric covariance matrix" << std::endl;
    //initialize covariance matrix
    TMatrixT<double> frac_syst_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);
    TMatrixT<double> frac_total_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);
    TMatrixT<double> frac_GENIE_matrix(mc_spec.num_bins_total, mc_spec.num_bins_total);
    frac_GENIE_matrix.Zero();

    if(bool_stat_only){
    	frac_syst_matrix.Zero();
        std::cout<<"NC delta Fit||\tRUNNING Stat Only!"<<std::endl;
    }else if(bool_flat_det_sys){
	std::cout << "NC delta Fit||\tRUNNING with flat systematics: " << flat_det_sys_percent << "%!" << std::endl;
	frac_syst_matrix.Zero();
	//set up flat fractional syst covariance
	for(int i=0 ; i< mc_spec.num_bins_total; i++)
		for(int j=0;j<mc_spec.num_bins_total; j++)
			frac_syst_matrix(i,j)=flat_det_sys_percent*flat_det_sys_percent/10000.;
    }
    else{
	std::cout<< "NC delta Fit||\tRUNNING with Systematics!" << std::endl;
	frac_syst_matrix.Zero();

	std::cout << "\tOpen covariance matrix root file: " << covmatrix_file << std::endl;
	TFile* f_covar = new TFile(covmatrix_file.c_str(), "read");
	TMatrixT<double>* m_temp;
	m_temp = (TMatrixD*)f_covar->Get("frac_covariance");
	frac_total_matrix = *m_temp;

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

        frac_syst_matrix = frac_total_matrix - frac_GENIE_matrix;
	f_covar->Close();	
	f_genie->Close();
    }

   TFile* f_pull=NULL;
   TH2D* h_pull = NULL;
   std::vector<double> pull_term_vec;
   std::string x_axis_title, y_axis_title;
   if(add_pull_term){
	std::cout << "NC delta Fit||\t Grab pull term from " << pullterm_file << std::endl;
	f_pull = new TFile(pullterm_file.c_str(), "read");
	h_pull=(TH2D*)f_pull->Get("h_chi2_interpolation");
	x_axis_title = h_pull->GetXaxis()->GetTitle();
	y_axis_title = h_pull->GetYaxis()->GetTitle();
  	std::cout << "\tx axis name: " << x_axis_title << " and y axis name: " << y_axis_title << std::endl; 
	//std::cout << h_pull->FindBin(0, 0.5) << std::endl;
  }

   std::cout<< "NC delta Fit||\tGrab info of the grid"<< std::endl;
 


   //collect the name of dimensions: subchannels you want to vary; and the range
   //for plot reason
   std::vector<std::string> dimension_name;
   const double range_x_low = mygrid.f_dimensions.at(0).f_min;
   const double range_x_up = mygrid.f_dimensions.at(0).f_max;
   const double range_y_low = mygrid.f_dimensions.at(1).f_min;
   const double range_y_up = mygrid.f_dimensions.at(1).f_max;
   const double range_z_low = mygrid.f_dimensions.at(2).f_min;
   const double range_z_up = mygrid.f_dimensions.at(2).f_max;
   int nbin_x = mygrid.f_dimensions.at(0).f_N;  //number of point in x axis
   int nbin_y = mygrid.f_dimensions.at(1).f_N;  
   int nbin_z = mygrid.f_dimensions.at(2).f_N;  
 
   dimension_name.clear(); 
   for(int i=0; i< mygrid.f_num_dimensions ; i++){
	dimension_name.push_back(mygrid.f_dimensions.at(i).f_name);
   }



   //*********************loop over grid points, calc chi square********************************
   TFile* f_output = new TFile(Form("chi_contour_CV_%f.root",f_central), "recreate");
   TH3D* h_chi2_raw = new TH3D("h_chi2_raw", Form("h_chi2_raw;%s;%s;%s", dimension_name[0].c_str(), dimension_name[1].c_str(), dimension_name[2].c_str()), nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up, nbin_z, range_z_low, range_z_up);
   TH3D* h_chi2_delta = new TH3D("h_chi2_delta", Form("h_chi2_delta;%s;%s;%s", dimension_name[0].c_str(), dimension_name[1].c_str(), dimension_name[2].c_str()), nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up, nbin_z, range_z_low, range_z_up);
   TH3D* h_chi2_inter=NULL;  


	
   //give grid, do iterative fit, and grab the best fit point and the chi surface
   std::cout << "NC delta Fit||\tStart Iterative Chi calculation" <<std::endl;
   std::vector<double> chi;  //vector to save chi square values.
   chi.reserve(grid.size());  //reserve the memory
   std::vector<double> last_chi;  //vector to save chi square values for last iteration
   double best_chi; // best chi value
   double last_best_chi;
   int iterative_number = 1; //times to perform iterative fit
   double chi_square_tolerance = 1e-3;
   bool chi_converged = false;
   int best_fit, last_best_fit;  //best fit point & last best fit point
   //initialize a SBNchi
   SBNchi chi_temp(xml);
   //inverted collapsed covariance matrix	
    TMatrixT<double> full_syst(chi_temp.num_bins_total, chi_temp.num_bins_total);
   TMatrixT<double> genie_syst(chi_temp.num_bins_total, chi_temp.num_bins_total);
   TMatrixT<double> collapsed_syst(chi_temp.num_bins_total_compressed, chi_temp.num_bins_total_compressed);
   TMatrixT<double> collapsed_temp(chi_temp.num_bins_total_compressed, chi_temp.num_bins_total_compressed);
   TMatrixT<double> invert_collapsed_temp(chi_temp.num_bins_total_compressed, chi_temp.num_bins_total_compressed);


   TMatrixT<double> norm_only_syst(chi_temp.num_bins_total, chi_temp.num_bins_total);

   //stats only chi2
   std::vector<double> chi_stat;
   TMatrixT<double> collapsed_stat(chi_temp.num_bins_total_compressed, chi_temp.num_bins_total_compressed);
   TMatrixT<double> invert_collapsed_stat(chi_temp.num_bins_total_compressed, chi_temp.num_bins_total_compressed);


   input_data = true;
   for(int n_iter=0; n_iter < iterative_number; n_iter++){
	if(input_data){
	   collapsed_stat.Zero();
		
	   // for the first iteration, use null hypothesis to build covar matrix
	   if(n_iter == 0){
		SBNspec mc_copy = mc_spec;
                //mc_copy.Scale("NCDeltaRadOverlayLEE", 0.0);  //do not included 2x NCdelta in the mc ---> null hypothesis
		SBNspec mc_bkg= mc_copy;
	
		full_syst = chi_temp.FillSystMatrix(frac_syst_matrix, mc_copy.full_vector);

                for(int i=0; i< mygrid.f_num_dimensions; i++){
                        SBNspec comp = mc_copy;
			auto const dimension = mygrid.f_dimensions.at(i);
			if(dimension.f_has_constrain == true){
				comp.Keep(dimension_name[i], 1.0);
				genie_syst = chi_temp.FillSystMatrix(frac_GENIE_matrix,comp.full_vector);
                        	f_output->cd();
                        	genie_syst.Write(Form("genie_%s_%d", dimension_name[i].c_str(), n_iter));
                        
                        	genie_syst = chi_temp.CalcShapeOnlyCovarianceMatrix(frac_GENIE_matrix, &comp, &comp);
				f_output->cd();
				genie_syst.Write(Form("shape_genie_%s_%d", dimension_name[i].c_str(), n_iter));
                        	full_syst += genie_syst;
                        	mc_bkg.Scale(dimension_name[i], 0.0);

				norm_only_syst = chi_temp.SplitCovarianceMatrix(&frac_total_matrix, comp.full_vector, 3); 
				for(int k=0; k< comp.num_bins_total; k++){
					for(int j=0; j< comp.num_bins_total; j++){
						if(comp.full_vector.at(k)==0 || comp.full_vector.at(j) ==0) norm_only_syst(k,j) = 0;
						else norm_only_syst(k,j) = norm_only_syst(k,j)/(comp.full_vector.at(k)*comp.full_vector.at(j));
					}
				}
				f_output->cd();
				norm_only_syst.Write(Form("norm_total_%s_%d", dimension_name[i].c_str(), n_iter));
			}

                }
		genie_syst = chi_temp.FillSystMatrix(frac_GENIE_matrix, mc_bkg.full_vector);
                full_syst += genie_syst;
		
		chi_temp.CollapseModes(full_syst, collapsed_syst);
	
		collapsed_temp = chi_temp.AddStatMatrixCNP(&collapsed_syst, mc_copy.collapsed_vector, data_spec.collapsed_vector);
		//stat only covariance matrix
		collapsed_stat = chi_temp.AddStatMatrixCNP(&collapsed_stat, mc_copy.collapsed_vector, data_spec.collapsed_vector);
		

	        //compare data with constrained mc
		std::cout << "NC delta Fit||\tGenerating comparison between data and constrained MC" << std::endl; 
		tag="constrained_mc";
		mc_spec.CompareSBNspecs(collapsed_syst, &data_spec, tag);
		tag.clear();
	   }
	   else{
	   //otherwise use the best fit point in last iteration to build covar matrix
		std::vector<double> best_fit_point = grid[best_fit];
		SBNspec best_signal(mc_filename, xml, false);
		best_signal.Scale("NCDeltaRadOverlayLEE", 0.0);
		for(int i=0; i< best_fit_point.size(); i++){
			auto const dimension = mygrid.f_dimensions.at(i);
                        best_signal.Scale(dimension.f_name, best_fit_point[i]);
		}	


		full_syst = chi_temp.FillSystMatrix(frac_syst_matrix, best_signal.full_vector);

		SBNspec best_bkgd = best_signal;
                for(int i=0; i< mygrid.f_num_dimensions; i++){
                        SBNspec comp = best_signal;
			auto const dimension = mygrid.f_dimensions.at(i);
			if(dimension.f_has_constrain == true){
				comp.Keep(dimension_name[i], 1.0);
				genie_syst = chi_temp.FillSystMatrix(frac_GENIE_matrix,comp.full_vector);
                        	f_output->cd();
                        	genie_syst.Write(Form("genie_%s_%d", dimension_name[i].c_str(), n_iter));
                        
                        	genie_syst = chi_temp.CalcShapeOnlyCovarianceMatrix(frac_GENIE_matrix, &comp, &comp);
				f_output->cd();
				genie_syst.Write(Form("shape_genie_%s_%d", dimension_name[i].c_str(), n_iter));
                        	full_syst += genie_syst;
                        	best_bkgd.Scale(dimension_name[i], 0.0);
			}

                }
		genie_syst = chi_temp.FillSystMatrix(frac_GENIE_matrix, best_bkgd.full_vector);
                full_syst += genie_syst;
		chi_temp.CollapseModes(full_syst, collapsed_syst);

		collapsed_temp = chi_temp.AddStatMatrixCNP(&collapsed_syst, best_signal.collapsed_vector, data_spec.collapsed_vector);
		//stat only covariance matrix
		collapsed_stat = chi_temp.AddStatMatrixCNP(&collapsed_stat, best_signal.collapsed_vector, data_spec.collapsed_vector);
	   }


	   //inverted matrix
	   invert_collapsed_temp = chi_temp.InvertMatrix(collapsed_temp);
	   invert_collapsed_stat = chi_temp.InvertMatrix(collapsed_stat);

	   f_output->cd();
	   full_syst.Write(Form("syst_full_matrix_%d", n_iter));
	   collapsed_syst.Write(Form("syst_collapsed_matrix_%d", n_iter));
	   collapsed_temp.Write(Form("full_collapsed_matrix_%d", n_iter));
        } //end of 'input_data' loop

	   //clean everything before looping
	   best_chi = DBL_MAX;
	   chi.clear();
	   SBNspec spec_cv(mc_filename, xml, false);
	   spec_cv.Scale("NCDeltaRadOverlayLEE", 0.0);
	   SBNspec spec_signal;
	   SBNspec spec_bkgd;
	   SBNspec comp;
	   for(int i =0; i< grid.size() ;i++){

		//access grid point
		std::vector<double> point = grid[i];

		std::cout << i << std::endl;
		//set a temperary SBNspec, assume there is already a MC CV root file with corresponding sequence defined in xml	
		spec_signal = spec_cv;
		//scale chosen subchannels
		for(int j=0; j< point.size(); j++ ){
			auto const dimension = mygrid.f_dimensions.at(j);
			spec_signal.Scale(dimension.f_name, point[j]);
		}

		if(!input_data){
			spec_bkgd = spec_signal;
			full_syst = chi_temp.FillSystMatrix(frac_syst_matrix, spec_signal.full_vector);

			for(int j=0; j< mygrid.f_num_dimensions; j++){
				auto const dimension = mygrid.f_dimensions.at(j);
				if(dimension.f_has_constrain == true){
					comp = spec_signal;
					comp.Keep(dimension_name[j], 1.0);
					genie_syst = chi_temp.CalcShapeOnlyCovarianceMatrix(frac_GENIE_matrix, &comp, &comp);
					full_syst += genie_syst;
					spec_bkgd.Scale(dimension_name[j], 0.0);
				}
			}
			genie_syst = chi_temp.FillSystMatrix(frac_GENIE_matrix, spec_bkgd.full_vector);
			full_syst += genie_syst;
			chi_temp.CollapseModes(full_syst, collapsed_syst);

			collapsed_stat.Zero();
			collapsed_temp= chi_temp.AddStatMatrixCNP(&collapsed_syst, spec_signal.collapsed_vector, data_spec.collapsed_vector);
			collapsed_stat= chi_temp.AddStatMatrixCNP(&collapsed_stat, spec_signal.collapsed_vector, data_spec.collapsed_vector);
	   		invert_collapsed_temp = chi_temp.InvertMatrix(collapsed_temp);
	   		invert_collapsed_stat = chi_temp.InvertMatrix(collapsed_stat);
		}

		//calculate chi2
		double chi_value=chi_temp.CalcChi(invert_collapsed_temp, spec_signal.collapsed_vector, data_spec.collapsed_vector);
		double chi_stat_value=chi_temp.CalcChi(invert_collapsed_stat, spec_signal.collapsed_vector, data_spec.collapsed_vector);

		//directly add pull term using chi2 surface
		if(add_pull_term){

			//fill pull term values for grid as vec, for future use
			if(n_iter ==0){
				double x=DBL_MAX;
				double y=DBL_MAX;
				for(int j=0; j< point.size(); j++ ){
					auto const dimension = mygrid.f_dimensions.at(j);
					if(dimension.f_name == x_axis_title) x=point[j];
					else if(dimension.f_name == y_axis_title) y=point[j];
					else ;
				}
				if(x==DBL_MAX || y==DBL_MAX){
					std::cout << "Pull term||\t Grid dimension doesn't match X/Y axes in pull term??" << std::endl;
					exit(1);
				}
				//std::cout << x << " " << y << " " << h_pull->FindBin(x,y) << std::endl;
				int global_bin = h_pull->FindBin(x,y);
				pull_term_vec.push_back(h_pull->GetBinContent(global_bin));	
			}

			//add pull term
			chi_value += pull_term_vec[i];
			chi_stat_value += pull_term_vec[i];
		
			//simple pull term implmentation
			/*for( int j=0; j<point.size(); j++){
				auto const dimension = mygrid.f_dimensions.at(j);
				if(dimension.f_has_constrain==true) chi_value += pow((point[j] - dimension.f_constrain_value)/dimension.f_constrain_range, 2.0);
			}*/
		}
		// complete chi square calculation
		chi.push_back(chi_value);
		chi_stat.push_back(chi_stat_value);

		if(chi_value < best_chi){
			best_chi = chi_value;
			best_fit = i;
		}
	   }
	   std::cout << "On iteration " << n_iter << ", best fit point: " << best_fit << " with chi minimum " << best_chi;
	  
	   if(chi_converged) break;
 
	   if(n_iter != 0){
		if(abs(best_chi-last_best_chi) < chi_square_tolerance) chi_converged = true;;
	   }

	   last_best_fit = best_fit;
	   last_best_chi = best_chi;
	   last_chi = chi;

	   std::cout << ", and chi value has converged: "<< chi_converged << std::endl;
   }

   std::cout << std::endl;
   std::cout << "NC delta Fit||\t End of Iterative Chi2 calculation" << std::endl;
    

   std::vector<double> best_point = grid[best_fit];
   std::cout << "Best Fit Point: (" << best_point[0] << ", " << best_point[1] << ", " << best_point[2] << ")."<<std::endl;
   if(input_data){
	   std::cout << "NC delta Fit||\tGenerating comparison between data and best fit MC" << std::endl; 
	   //compare spectrum between data and the best fit point
	   SBNspec mc_best(mc_filename, xml);
	   mc_best.Scale("NCDeltaRadOverlayLEE", 0.0);
	   std::cout<< "NC delta Fit||\tBest Fit Point: (";
	   for(int i=0; i< best_point.size(); i++ ){
			auto const dimension = mygrid.f_dimensions.at(i);
			mc_best.Scale(dimension.f_name, best_point[i]);
			std::cout << best_point[i] << ", ";
	   }
	   std::cout << ")" << std::endl;
	   tag = "best_fit";
	   mc_best.CompareSBNspecs(collapsed_syst, &data_spec, tag);
   }


   std::cout << "NC delta Fit||\tPrint out delta chi square for grid points now" << std::endl;
   //delta chi2;
   for(int i=0; i< grid.size(); i++){
	 std::vector<double> point = grid[i];
	 h_chi2_raw->Fill(point[0], point[1], point[2],chi[i]);

	 //chi[i] -= best_chi;   // should i use last_best_chi ??
	 //h_chi2_delta->Fill(point[0], point[1], point[2], chi[i]);	 
	 double temp_delta_chi = chi[i] - best_chi;   // should i use last_best_chi ??
	 h_chi2_delta->Fill(point[0], point[1], point[2], temp_delta_chi);	 
	 std::cout << "DeltaChi: " << i ;
         for(int j =0;j <point.size(); j++) std::cout << " " << point[j];
         std::cout <<" || Syst chi:" << chi[i] << " || Stat chi:" << chi_stat[i] << std::endl;
   }
   h_chi2_delta->SetMinimum(-1);  // to show the zero z values
   f_output->cd();
   h_chi2_raw->Write();
   h_chi2_delta->Write();

   std::cout << "NC delta Fit||" <<  "\t Start projecting on 2D plots" << std::endl;

   //histograms saving delta chi values with one parameter being marginalized
   TH2D* h_mchi2_xy = new TH2D("h_mchi2_xy", Form("h_mchi2_xy; %s;%s",dimension_name[0].c_str(), dimension_name[1].c_str()),nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up);
   TH2D* h_mchi2_xz = new TH2D("h_mchi2_xz", Form("h_mchi2_xz; %s;%s",dimension_name[0].c_str(), dimension_name[2].c_str()),nbin_x, range_x_low,range_x_up, nbin_z, range_z_low, range_z_up);
   TH2D* h_mchi2_yz = new TH2D("h_mchi2_yz", Form("h_mchi2_yz; %s;%s",dimension_name[1].c_str(), dimension_name[2].c_str()),nbin_y, range_y_low,range_y_up, nbin_z, range_z_low, range_z_up);

   //histograms saving delta chi values with respect to global minimum
   TH2D* h_gchi2_xy = new TH2D("h_gchi2_xy", Form("h_gchi2_xy; %s;%s",dimension_name[0].c_str(), dimension_name[1].c_str()),nbin_x, range_x_low,range_x_up, nbin_y, range_y_low, range_y_up);
   TH2D* h_gchi2_xz = new TH2D("h_gchi2_xz", Form("h_gchi2_xz; %s;%s",dimension_name[0].c_str(), dimension_name[2].c_str()),nbin_x, range_x_low,range_x_up, nbin_z, range_z_low, range_z_up);
   TH2D* h_gchi2_yz = new TH2D("h_gchi2_yz", Form("h_gchi2_yz; %s;%s",dimension_name[1].c_str(), dimension_name[2].c_str()),nbin_y, range_y_low,range_y_up, nbin_z, range_z_low, range_z_up);


  TH1D* h_chi_delta = new TH1D("h_chi_delta", Form("h_chi_delta; %s;#Delta#chi{2}",dimension_name[2].c_str()), nbin_z, range_z_low, range_z_up);
  TH1D* h_chi_stat = new TH1D("h_chi_stat", Form("h_chi_stat; %s;#Delta#chi{2}",dimension_name[2].c_str()), nbin_z, range_z_low, range_z_up);
   //set the bin content to DBL_MAX
   for(int ix=1;ix <= nbin_x; ix++){
	for(int iy=1; iy <= nbin_y; iy++) h_mchi2_xy->SetBinContent(ix, iy, DBL_MAX);
	for(int iz=1; iz <= nbin_z; iz++) h_mchi2_xz->SetBinContent(ix, iz, DBL_MAX);
   }
   for(int iz=1; iz <= nbin_z; iz++){
	for(int iy=1; iy <= nbin_y; iy++)  h_mchi2_yz->SetBinContent(iy, iz, DBL_MAX);
   	h_chi_delta->SetBinContent(iz, DBL_MAX);
   	h_chi_stat->SetBinContent(iz, DBL_MAX);
   }


   
   //marginalize one parameter
   for(int ix=0; ix < nbin_x; ix++){
	for(int iy=0; iy < nbin_y; iy++){
	   for(int iz=0 ; iz< nbin_z; iz++){
		int ip = ix*nbin_y*nbin_z + iy*nbin_z + iz; // index of grid point
		std::vector<double> point = grid[ip]; 


		//marginalized minimum
		//conditional operator, saver the smaller chi.
		if(chi[ip]< h_mchi2_xy->GetBinContent(ix+1, iy+1)){
			 h_mchi2_xy->SetBinContent(ix+1, iy+1, chi[ip]);
			//std::cout << "chi2 value: " << chi[ip] << std::endl;
		}
		if(chi[ip]< h_mchi2_xz->GetBinContent(ix+1, iz+1)) h_mchi2_xz->SetBinContent(ix+1, iz+1, chi[ip]);
		if(chi[ip]< h_mchi2_yz->GetBinContent(iy+1, iz+1)) h_mchi2_yz->SetBinContent(iy+1, iz+1, chi[ip]);


		//global minimum
		if(point[2] == best_point[2]) h_gchi2_xy->Fill(point[0], point[1], chi[ip]);
		if(point[1] == best_point[1]) h_gchi2_xz->Fill(point[0], point[2], chi[ip]);
		if(point[0] == best_point[0]) h_gchi2_yz->Fill(point[1], point[2], chi[ip]);

		//marginalize over two parameters
		if(chi[ip] < h_chi_delta->GetBinContent(iz+1)) h_chi_delta->SetBinContent(iz+1, chi[ip]);
		if(chi_stat[ip] < h_chi_stat->GetBinContent(iz+1)) h_chi_stat->SetBinContent(iz+1, chi_stat[ip]);
	   }
	}
   } 

  f_output->cd();
  h_gchi2_xy->Write();
  h_gchi2_yz->Write();
  h_gchi2_xz->Write();
  h_mchi2_xy->Write();
  h_mchi2_yz->Write();
  h_mchi2_xz->Write();
  h_chi_delta->Write();
  h_chi_stat->Write();

   /*std::cout << "DeltaChi:" <<std::endl;
   for(int i =0; i< chi.size(); i++) std::cout << " " << chi[i];
   std::cout<< std::endl;
   */


   //****************** START INTERPOLATION*********************************

/*   if(interpolation_number != -99){

	//the upper range of x, y axis for interpolation
	double range_x_inter = mygrid.f_dimensions.at(0).f_max - mygrid.f_dimensions.at(0).f_step;
	double range_y_inter = mygrid.f_dimensions.at(1).f_max - mygrid.f_dimensions.at(1).f_step;
	std::cout << "range x interpolation " << range_x_inter << " Y: "<< range_y_inter <<std::endl;

	//save interpolated 2D plot
   	h_chi2_inter = new TH2D("h_chi2_interpolation", "h_chi2_interpolation", interpolation_number, range_x_low,range_x_inter, interpolation_number, range_y_low, range_y_inter);
	h_chi2_inter->SetMinimum(-1);
	//h_chi2_inter->SetAxisRange(range_x_low, range_x_inter, "X");
	//h_chi2_inter->SetAxisRange(range_y_low, range_y_inter, "Y");


	std::cout << "Fraction Fit||" << "\tStart interpolation with number "<< interpolation_number <<std::endl;
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

	// initialize interpolation 
	gsl_spline2d_init(spline,  &grid_y[0], &grid_x[0], &chi[0] , nbin_y, nbin_x);


	// interpolate N values in x and y and print out grid for plotting 
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

		  std::cout << "Interpolated value: " << zij << " ||Grid Point:(" << xi << ", " << yj << ")" << std::endl; 
		}
	}

	  f_output->cd();
	  h_chi2_inter->Write();

	  gsl_spline2d_free(spline);
	  gsl_interp_accel_free(xacc);
	  gsl_interp_accel_free(yacc);
  }
  else{ 
	h_chi2_inter = (TH3D*)h_chi2_delta->Clone();
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

   std::vector<double> contour{2.30, 4.61,6.18,11.83}; // chi2 value for 2 dof with 1 sigma, 90%, 2 sigma and 3 sigma confidence level
   std::vector<std::string> CL_string{"1sigma", "90", "2sigma", "3sigma"};
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
*/
    f_output->Close(); 
    if(add_pull_term) f_pull->Close(); 

    std::cout << "NC delta Fit||" << "\tFinished" <<std::endl;
    std::cout << "Total wall time: " << difftime(time(0), start_time)/60.0 << " Minutes.\n";
    return 0;

}

