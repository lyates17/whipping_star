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
#include "TLatex.h"

#include "params.h"
#include "SBNconfig.h"
#include "SBNchi.h"
#include "SBNspec.h"
#include "SBNosc.h"
#include "SBNfit.h"
#include "SBNfit3pN.h"
#include "SBNcovariance.h"
#include "SBNsinglephoton.h"

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


    /*************************************************************
     *************************************************************
     *		Command Line Argument Reading
     ************************************************************
     ************************************************************/
    const struct option longopts[] =
    {
        {"xml", 		required_argument, 	0, 'x'},
        {"tag", 		required_argument, 	0, 't'},
        {"stat", 		no_argument, 		0, 's'},
        {"mode", 		required_argument,	0, 'm'},
        {"data", 		required_argument,	0, 'd'},
	{"covariancematrix",    required_argument,      0, 'c'},
	{"geniematrix",         required_argument,      0, 'g'},
	{"flat",                required_argument,      0 ,'f'},
	{"edependent",          no_argument,            0 ,'e'},
	{"interpolation",       required_argument,      0, 'i'},
        //{"randomseed",        required_argument, 0 ,'r'},
        {"help", 		no_argument,	0, 'h'},
        {0,			    no_argument, 		0,  0},
    };

    int iarg = 0;
    opterr=1;
    int index;

    std::string xml = "Whatt.xml";
    //a tag to identify outputs and this specific run. defaults to EXAMPLE1
    std::string tag = "NoTag";
    std::string mode = "fit";
    int interpolation_number = -99;  //number of points for chi2 value interpolation
    //double random_number_seed = -1;

    bool bool_stat_only = false;
    bool bool_edependent = false;   //energy/momentum dependent fit or not
    bool input_data = false;
    std::string data_filename;
    std::string covmatrix_file;  //root file containing total covariance matrix
    std::string genie_matrix_file;  //root file containing flux/XS covariance matrix
    std::string det_matrix_file; //root file containing each det syst covar matrix;

    bool bool_flat_sys = false;
    double flat_sys_percent = 0.0;

    while(iarg != -1)
    {
        iarg = getopt_long(argc,argv, "x:m:t:d:c:g:i:e:f:sh", longopts, &index);

        switch(iarg)
        {
            case 'x':
                xml = optarg;
                break;
	    case 't':
		tag = optarg;
		break;
            case 'd':
                input_data = true;
                data_filename = optarg;
                break;
	    case 'm':
		mode = optarg;
		break;
	    case 'c':
		covmatrix_file = optarg;
		break;
	    case 'g':
		genie_matrix_file = optarg;
		break;
            case 'f':
                bool_flat_sys = true;
                flat_sys_percent = (double)strtod(optarg,NULL);
                break;
            //case 'r':
            //    random_number_seed = (double)strtod(optarg,NULL);
            //    std::cout<<"Reading in random seed argument: "<<random_number_seed<<std::endl;
            //    break;
            case 's':
                bool_stat_only = true;
                break;
	    case 'e':
		bool_edependent = true;
		break;
	    case 'i':
		interpolation_number = (int)strtod(optarg, NULL);
		break;
            case '?':
            case 'h':
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"sbnfit_fraction_fit is a work in progress."<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"--- Required arguments: ---"<<std::endl;
                std::cout<<"\t-x\t--xml\t\tInput configuration .xml file for SBNconfig"<<std::endl;
                std::cout<<"\t-d\t--data\t\tInput observed data for fit to real data"<<std::endl;
                std::cout<<"\t-m\t--mode\t\tInput running mode, default is 'fit' mode"<<std::endl;
                std::cout<<"\t-m\t--option\t\t gen --- generate energy/momentum dependent pre-scaling file "<<std::endl;
		std::cout<<"\t-c\t--covariance matrix\t\tInput fractional covariance matrix"<< std::endl;
		std::cout<<"\t-g\t--FluxXS covariance matrix\t\tInput FluxXS covariance matrix to extract genie matrix"<< std::endl;
                std::cout<<"\t-f\t--flat\t\t Input flat systematic fractional covariance matrix"<<std::endl;
		std::cout<<"\t-i\t--interpolation\t\tInput number of points for interpolation"<< std::endl;
                std::cout<<"--- Optional arguments: ---"<<std::endl;
                std::cout<<"\t-s\t--stat\t\tStat only runs"<<std::endl;
                //std::cout<<"\t-r\t--randomseed\t\tRandomNumber Seed (default from machine)"<<std::endl; 
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

    std::cout<<"Begining Single Photon module"<<std::endl;

    NGrid mygrid, poly_grid;

    //now only available for 2 subchannels only
    //mygrid.AddFixedDimension("NCPi0Coh", 1.0);   //fixed
    mygrid.AddDimension("NCPi0NotCoh", 0.5, 1.25, 0.01);   //0.1 FULL
    mygrid.AddDimension("NCPi0Coh", 0., 5., 0.05); //0.1full

    poly_grid.AddDimension("NCPi0NotCoh", 0.5, 2, 0.05);  //first order
    poly_grid.AddFixedDimension("NCPi0NotCoh", 0.0); // second order 

    if(mode == "gen"){
	if(bool_edependent){
	    SBNsinglephoton sp(xml, tag, mygrid, poly_grid, true);
	    sp.GeneratePreScaledSpectra();	
	}else{
	    SBNsinglephoton sp(xml, tag, mygrid);
	    sp.GeneratePreScaledSpectra();
	}
    }
    else if(mode =="fit"){
	SBNsinglephoton sp(xml, tag, mygrid);
	if(bool_edependent){   //setup poly grid if it's an energy-dependent fit
	    sp.SetPolyGrid(poly_grid);
	}

	//load CV, data and prescaled spectra
	sp.LoadCV();
	if(input_data) sp.LoadData(data_filename);
	sp.LoadSpectraApplyFullScaling();

	//setup systematic fractional covariance matrix
	if(bool_stat_only) sp.SetStatOnly();
	else if(bool_flat_sys) sp.SetFlatFullFracCovarianceMatrix(flat_sys_percent);
	else  sp.SetFullFractionalCovarianceMatrix(covmatrix_file, "frac_covariance");

	if(bool_stat_only) sp.SetStatOnly();
	if(tag == "NCpi0"){
		//NCpi0 fit need extra flux+XS syst covar matrix
		if(!bool_stat_only){
		    sp.SetGenieFractionalCovarianceMatrix(genie_matrix_file);
		    sp.CalcFullButGenieFractionalCovarMatrix();
		}
		sp.CalcChiGridScanShapeOnlyFit();
		sp.SaveHistogram();
	}else if(tag == "NCDelta"){
		sp.CalcChiGridScan();
		sp.SaveHistogram();
	}
    }
    else{
	std::cout << "Mode input is not identified, please try with a valid input.." << std::endl;
	std::cout << "Mode options: 'fit'|| Perform fit" << std::endl;
	std::cout << "Mode options: 'gen'|| Generate energy/momentum dependent pre-scaling root files" << std::endl;
    }
    std::cout << "Single Photon module||" << "\tFinished" <<std::endl;
    std::cout << "Total wall time: " << difftime(time(0), start_time)/60.0 << " Minutes.\n";
    return 0;

}

