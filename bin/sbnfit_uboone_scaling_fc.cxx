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
#include "TLine.h"
#include "TChain.h"
#include "TMath.h"
#include "TSystem.h"
#include "TMatrixT.h"
#include "TRandom.h"
#include "TError.h"
#include "TCanvas.h"
#include "TH2F.h"
#include "TGraph.h"
#include "TMultiGraph.h"

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
void runHelp(){
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"Modified single subchannel scaling feldman_cousins confidence belt constructor"<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;
                std::cout<<"--- Required arguments: ---"<<std::endl;
                std::cout<<"\t-x\t--xml\t\tInput configuration .xml file for SBNconfig"<<std::endl;
                std::cout<<"\t-t\t--tag\t\tA unique tag to identify the inputs/outputs [Default to TEST]"<<std::endl;
                std::cout<<"\t-i\t--input\t\tInput subchannel to scale (no default, required argument)"<<std::endl;
                std::cout<<"\t-g\t--grid\t\tGrid to scan, in the form 'min max num_steps' (default '1e-4 10.0 20')"<<std::endl;
                std::cout<<"\t-m\t--mode\t\tWhat mode you want to run in. Arguments are:"<<std::endl;
                std::cout<<"\t\t\t--\t feldman : Perform the pseudo universe grid scan (run first)"<<std::endl;  
                std::cout<<"\t\t\t--\t belt: Constructs the confidence belts, must be run after'feldman'"<<std::endl;
                std::cout<<"--- Optional arguments: ---"<<std::endl;
                std::cout<<"\t-s\t--stat\t\tStatistical error only mode, will ignore any covariance matrix passed in"<<std::endl;
                std::cout<<"\t-n\t--number\t\tNumber of pseudo-experiments to simulate (default 2500)"<<std::endl; 
                std::cout<<"\t-r\t--randomseed\t\tRandomNumber Seed (default from machine)"<<std::endl; 
                std::cout<<"\t-c\t--cnp\t\tuse a Combined Newman Pearson chi2 (default false)"<<std::endl;
                std::cout<<"\t-h\t--help\t\tThis help menu."<<std::endl;
                std::cout<<"---------------------------------------------------"<<std::endl;
    return;
}

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
        {"stat", 		no_argument, 		0, 's'},
        {"number", 		required_argument,	0,'n'},
        {"cnp", 		no_argument,	0,'c'},
        {"grid", 		required_argument,	0,'g'},
        {"tag", 		required_argument,	0, 't'},
        {"mode",        required_argument, 0 ,'m'},
        {"input",       required_argument, 0 ,'i'},
        {"randomseed",        required_argument, 0 ,'r'},
        {"help", 		no_argument,	0, 'h'},
        {0,			    no_argument, 		0,  0},
    };

    int iarg = 0;
    opterr=1;
    int index;

    //a tag to identify outputs and this specific run. defaults to EXAMPLE1
    std::string tag = "TEST";
    std::string mode_option;
    bool bool_stat_only = false;
    int number = 2500;
    double random_number_seed = -1;
    bool use_cnp = false;
        
    std::string grid_string = "1e-4 8.0 33";
    std::string input_scale_subchannel = "unset";

    while(iarg != -1)
    {
        iarg = getopt_long(argc,argv, "x:t:m:n:r:p:i:g:sch", longopts, &index);

        switch(iarg)
        {
            case 'x':
                xml = optarg;
                break;
            case 'n':
                number = (int)strtod(optarg,NULL);
                break;
            case 't':
                tag = optarg;
                break;
            case 'g':
                grid_string = optarg; 
                break;
            case 'i':
                input_scale_subchannel = optarg;
                break;
            case 'm':
                mode_option = optarg;
                break;
            case 'c':
                use_cnp = true;
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
                runHelp(); 
                return 0;
        }
    }



    /*************************************************************
     *************************************************************
     *			Main Program Flow
     ************************************************************
     ************************************************************/
    time_t start_time = time(0);

    std::cout<<"Begining SBNfit uboone subchannel scaling Feldman Cousins confidence belt constructor for tag: "<<tag<<std::endl;

    if(input_scale_subchannel=="unset"){
        std::cout<<"Error! you must set a value for which input subchannel to scale, e.g using --input/ -i 'nu_uBooNE_1g1p_ncdelta'"<<std::endl;
        std::cout<<"Please see...."<<std::endl;
        runHelp();
        return 0;
    }
    

    NGrid mygrid;
    mygrid.AddDimension("scale",grid_string);
    
    mygrid.Print();
    SBNfeld myfeld(mygrid,tag,xml);

    if(mode_option == "feldman"){

        std::cout<<"Begininning a full Feldman-Cousins analysis for tag : "<<tag<<std::endl;

        myfeld.SetFractionalCovarianceMatrix(tag+".SBNcovar.root","frac_covariance");
        //myfeld.SetFractionalCovarianceMatrix(Msys);
        //myfeld.SetStatOnly();
        myfeld.m_subchannel_to_scale = input_scale_subchannel;

        myfeld.SetCoreSpectrum(tag+"_CV.SBNspec.root");
        myfeld.SetBackgroundSpectrum(tag+"_CV.SBNspec.root",input_scale_subchannel,0.0);
        myfeld.GenerateScaledSpectra();

        std::cout<<"Setting random seed "<<random_number_seed<<std::endl;
        myfeld.SetRandomSeed(random_number_seed);
        myfeld.SetNumUniverses(number);

        std::cout<<"Calculating the necessary SBNchi objects"<<std::endl;
        myfeld.CalcSBNchis();
        std::cout <<"DONE calculating the necessary SBNchi objects at : " << difftime(time(0), start_time)/60.0 << " Minutes.\n";

        std::cout<<"Beginning to peform FullFeldmanCousins analysis"<<std::endl;
        myfeld.FullFeldmanCousins();

    }else if(mode_option == "belt"){

        if(bool_stat_only){
            myfeld.SetEmptyFractionalCovarianceMatrix();
            myfeld.SetStatOnly();
            std::cout<<"RUNNING Statistics uncertainty only!"<<std::endl;
        }else{
            myfeld.SetFractionalCovarianceMatrix(tag+".SBNcovar.root","frac_covariance");
        }
        myfeld.m_subchannel_to_scale = input_scale_subchannel;

        if(use_cnp) myfeld.UseCNP();

        myfeld.SetCoreSpectrum(tag+"_CV.SBNspec.root");
        myfeld.SetBackgroundSpectrum(tag+"_CV.SBNspec.root",input_scale_subchannel,0.0);
        myfeld.GenerateScaledSpectra();

        std::cout<<"Calculating the necessary SBNchi objects"<<std::endl;
        myfeld.CalcSBNchis();
        std::cout <<"DONE calculating the necessary SBNchi objects at : " << difftime(time(0), start_time)/60.0 << " Minutes.\n";

        TFile *f = new TFile("scan.root","recreate");
        f->cd();
        std::cout<<"Starting to peform a globalScan analysis"<<std::endl;
        std::vector<std::vector<double>> vec_grid = mygrid.GetGrid();

        TFile *fin = new TFile(("SBNfeld_output_"+tag+".root").c_str(),"read");

        int plotting_true_gridpoint = 5;
        std::vector<double> plotting_pvals = {0.6827, 0.90, 0.9545, 0.9973};
        std::vector<std::string> plotting_strs = {"1#sigma","90%","2#sigma","3#sigma"};

        std::vector<double> v_median;
        std::vector<double> v_true;
        std::vector<double> v_1sigma_p;
        std::vector<double> v_1sigma_m;
        std::vector<std::vector<double>> v_min;v_min.resize(plotting_pvals.size());
        std::vector<std::vector<double>> v_max;v_max.resize(plotting_pvals.size());

        std::cout<<"MPrinting stuff"<<std::endl;
        TH2D * f_FC = new TH2D("f_FC","f_FC",vec_grid.size(),vec_grid.front()[0],vec_grid.back()[0],vec_grid.size(),vec_grid.front()[0],vec_grid.back()[0]);

        for(int i=0; i< vec_grid.size(); i++){

            v_true.push_back(vec_grid[i][0]);

            //Whats the critical value?
            TTree *t =  (TTree*)fin->Get(("ttree_"+std::to_string(i)).c_str());
            TH1D * cumul = (TH1D*)fin->Get(("delta_chi2_"+std::to_string(i)+"_cumulative").c_str());

            for(int p =0; p< plotting_pvals.size(); ++p){
                double plotting_pval = plotting_pvals[p];

                //First lets find a critical chi^2 for this confidence level
                double critical_delta_chi2 = 0;
                for(int c = cumul->GetNbinsX()-1;  c>0 ; --c){
                    if(cumul->GetBinContent(c+1) >= plotting_pval && cumul->GetBinContent(c)< plotting_pval){
                        critical_delta_chi2 = cumul->GetBinCenter(c);
                        break;
                    }
                }

                std::cout<<"Grid point "<<i<<" has a critical delta chi of "<<critical_delta_chi2<<" for a pval of "<<plotting_pval<<std::endl; 

                std::string nam = std::to_string(i)+"bfhist";
                int Nentries = t->GetEntries(); 

                const unsigned nentries = t->Draw("bf_gridvalue", ("delta_chi2<="+std::to_string(critical_delta_chi2)).c_str());
                if (nentries) {
                    double* x = t->GetV1();
                    //std::cout << "min :" << *(std::min_element(x, x+nentries)) << std::endl;
                    //std::cout << "max :" << *(std::max_element(x, x+nentries)) << std::endl;
                    v_min[p].push_back( *(std::min_element(x, x+nentries)) );
                    v_max[p].push_back( *(std::max_element(x, x+nentries)) );
                }
            }//end pval loop
            delete cumul;
        }


        TCanvas *c3 = new TCanvas("hope3");
        c3->SetFillStyle(0);

        TPad *pad = new TPad("pad", "pad", 0, 0, 0.8, 1.0);
        pad->SetRightMargin(0); // Upper and lower plot are joined
        pad->Draw();             // Draw the upper pad: pad
        pad->cd();               // pad becomes the current pad

        std::vector<TGraph*> gmaxs;
        std::vector<TGraph*> gmins;
        std::vector<TGraph*> grshades;

        std::vector<int> gcols = {kGreen+3,kGreen+2,kGreen-3,kGreen-6};
        TLegend * l_probs = new TLegend(0.11,0.11,0.89,0.89);

        TMultiGraph *mg = new TMultiGraph();
        mg->SetTitle("Feldman Cousins Corrected Confidence Belts");

        for(int p=plotting_pvals.size()-1; p>=0;--p){
            pad->cd();
            
            gmins.push_back(new TGraph(v_true.size(),&(v_min[p])[0], &v_true[0]));
            gmaxs.push_back(new TGraph(v_true.size(),&(v_max[p])[0], &v_true[0]));
            grshades.push_back( new TGraph(2*v_true.size()));
            for (int i=0;i<v_true.size();i++) {
                int n = v_true.size();
                grshades.back()->SetPoint(i,v_min[p][i],v_true[i]);
                grshades.back()->SetPoint(n+i,v_max[p][n-i-1],v_true[n-i-1]);
            }
            grshades.back()->SetFillColor(gcols[p]);
            gmins.back()->SetLineWidth(2);
            gmins.back()->SetLineColor(kBlack);
            gmaxs.back()->SetLineWidth(2);
            gmaxs.back()->SetLineColor(kBlack);

            l_probs->AddEntry(grshades.back(), plotting_strs[p].c_str() ,"f");
        }

        for(auto &g:grshades)mg->Add(g);
        pad->cd();
        mg->Draw("ALF");
        
        mg->GetXaxis()->SetTitle("Measured signal strength (#hat{#mu})");
        mg->GetYaxis()->SetTitle("True signal strength (#mu)");
        mg->SetMinimum(v_true.front());
        mg->SetMinimum(v_true.front());

        mg->GetXaxis()->SetLimits(v_true.front(),v_true.back());      
        mg->GetHistogram()->SetMaximum(v_true.back());          
        mg->GetHistogram()->SetMinimum(v_true.front());     
 
        for(auto &g:gmins)g->Draw("l same");
        for(auto &g:gmaxs)g->Draw("l same");

        c3->cd();
        TPad *padl = new TPad("padl", "padl", 0.8, 0, 1, 1);
        padl->SetBottomMargin(0.2);
        padl->Draw();
        padl->cd();       // padl becomes the current pad
        l_probs->SetTextSize(0.0775);
        l_probs->Draw();
        l_probs->SetLineColor(kWhite);
        l_probs->SetLineWidth(0);
        
        c3->SaveAs(("FC_confidence_belt_"+tag+".pdf").c_str(),"pdf");

        std::cout<<"**************** Feldman Cousins 1D Confidence Intervals  **********************"<<std::endl;
        for(int i=0; i<v_true.size(); i++){
            std::cout<<"Grid Pt: "<<i<<", ScaleFactor: "<<vec_grid[i][0]<<std::endl;
            for(int p=0; p< plotting_pvals.size();++p){
                double measured_val = vec_grid[i][0];
                std::vector<double> reg = myfeld.getConfidenceRegion(gmins[plotting_pvals.size()-p-1],gmaxs[plotting_pvals.size()-p-1],measured_val);
                std::cout<<"-- CL: "<<plotting_pvals[p]<<"  Sigma: "<<sqrt(2)*TMath::ErfInverse(plotting_pvals[p])<<"  ConfidenceInterval: ["<<reg[0]<<" -> "<<reg[1]<<"]"<<std::endl;
            }
        }
    }else{
        std::cout<<"The mode you asked for ("<<mode_option<<") is not available, the available options are.."<<std::endl;
        runHelp();

    }
    std::cout << "Fin. Total wall time: " << difftime(time(0), start_time)/60.0 << " Minutes.\n";

    return 0;

}


