#include "SBNcls.h"
using namespace sbn;

int SBNcls::SetSamplePoisson(){
    which_sample = 0;
    return which_sample;
}

int SBNcls::SetSampleCovariance(){
    which_sample = 1;
    return which_sample;
}


double SBNcls::pval2sig1sided(double pval){
    return sqrt(2)*TMath::ErfInverse(1-pval);
}

double SBNcls::pval2sig2sided(double pval){
    return sqrt(2)*TMath::ErfInverse(1-pval*2.0);
}

double SBNcls::pval2sig(double pval){
    //for backward compatability, work
    return pval2sig2sided(pval);
}

int SBNcls::setMode(int input_mode){
    which_mode = input_mode;
    return which_mode;

}

int SBNcls::CalcCLS(int numMC, std::string tag){

    
    //runConstraintTest();

    if(which_sample == 0){
        std::cout<<"SBNcls::CalcCLS\t|| Running in Poission sampling mode!"<<std::endl;
    }
    else if(which_sample ==1){ 
        std::cout<<"SBNcls::CalcCLS\t|| Running in Covariance sampling mode!"<<std::endl;
    }

    std::vector<double> ven={0};
    std::vector<double>  vec_CLs;

    time_t start_time = time(0);

    double N_h1 = h1->GetTotalEvents();
    double N_h0 = h0->GetTotalEvents();

    chi_h0.InitRandomNumberSeeds(10);
    chi_h1.InitRandomNumberSeeds(10);

    double central_value_chi = chi_h0.CalcChi(h1);
    double central_value_chi_h1 = chi_h1.CalcChi(h1);

    std::cout<<"SBNcls::CalcCLS\t|| Central Value Chi is : "<<central_value_chi<<" and "<<central_value_chi_h1<<" should be 0"<<std::endl;

    std::vector<CLSresult> h1_results;
    std::vector<CLSresult> h0_results;

    std::cout<<"SBNcls::CalcCLS\t|| Starting H1 PDF generation "<<std::endl;
    if(which_mode==0){
        //if(which_sample == 0) h1_pdf = chi_h0.SamplePoissonVaryInput(h1, numMC, central_value_chi*50);
        //else if(which_sample==1) h1_pdf = chi_h0.SampleCovarianceVaryInput(h1, numMC, central_value_chi*50);
    }else if (which_mode ==1){
        h1_results =  chi_h1.Mike_NP(h1, chi_h0, chi_h1, numMC, which_sample,1);
    }

    double sig1 = 0.5-(0.6827)/2.0;
    double sig2 = 0.5-(0.9545)/2.0;

    std::vector<double> prob_values = {1-sig2, 1-sig1, 0.5, sig1, sig2};

    for(int i=0; i< h1_results.size(); i++){
        h1_results[i].m_quantiles.resize(prob_values.size(),0.0);	
        h1_results[i].m_pdf.ComputeIntegral(); 
        h1_results[i].m_pdf.GetQuantiles(prob_values.size(), &(h1_results[i].m_quantiles)[0], &prob_values[0]);
        for(int p=0; p< prob_values.size();p++){
            std::cout<<"Quantile @ "<<prob_values[p]<<" is "<<h1_results[i].m_quantiles[p]<<" for "<<h1_results[i].m_tag<<std::endl;
        }
    }

    //Now calculate the pvalues associated with those h1 variations. 

    std::cout<<"SBNcls::CalcCLS\t|| Starting H0 PDF generation "<<std::endl;
    if(which_mode ==0){
        //if(which_sample == 0)     h0_pdf = chi_h0.SamplePoissonVaryInput(h0, numMC, &pval);
        //else if(which_sample ==1) h0_pdf = chi_h0.SampleCovarianceVaryInput(h0, numMC, &pval);
    }else if (which_mode==1){
        h0_results = chi_h0.Mike_NP(h0, chi_h0, chi_h1, numMC,which_sample,0);
    }

    //Ok now calc pvalues for h0 based on h1's quantiles!
    for(int i=0; i< h0_results.size(); i++){

        h0_results[i].m_nlower.resize(prob_values.size(),0);

        std::cout<<i<<" "<<h0_results[i].m_values.size()<<" "<<numMC<<std::endl;
        for(int m=0; m< numMC; m++){
            for(int p =0; p< prob_values.size();p++){
                if(h0_results[i].m_values[m]>=h1_results[i].m_quantiles[p]){
                    h0_results[i].m_nlower[p] += 1.0/(double(numMC));
                }
            }
        }

    std::cout<<"We have "<<h1_results[i].m_pdf.Integral()<<" integral of H1 and "<<h0_results[i].m_pdf.Integral()<<" integral of H0 for metric "<<h1_results[i].m_tag<<std::endl;
    }
    std::cout << "Total wall time: " << difftime(time(0), start_time)/1.0 << " Secs.\n";
        
    for(int i=0;i< h0_results.size();i++){
            makePlots( h0_results[i], h1_results[i], tag+std::to_string(i), which_mode);
    }


    //Constraint test
    
   


    return 0 ;
}


int SBNcls::makePlots(CLSresult &h0_result, CLSresult & h1_result, std::string tag, int which_mode){

    double max_plot = std::max(h0_result.m_max_value,h1_result.m_max_value)*1.5;
    double min_plot = std::min(h0_result.m_min_value,h1_result.m_min_value);

    TH1D h0_pdf((tag+"h0").c_str(),(tag+"h0").c_str(),250,min_plot,max_plot);
    TH1D h1_pdf((tag+"h1").c_str(),(tag+"h1").c_str(),250,min_plot,max_plot);

    for(int i=0; i<h0_result.m_values.size(); i++){
        h0_pdf.Fill(h0_result.m_values[i]);
        h1_pdf.Fill(h1_result.m_values[i]);
    }

    std::vector<double>  vec_CLs;
    std::vector<double> pval = h0_result.m_nlower; 

    double sig1 = 0.5-(0.6827)/2.0;
    double sig2 = 0.5-(0.9545)/2.0;

    std::vector<double> prob_values = {1-sig2, 1-sig1, 0.5, sig1, sig2};
    std::vector<double> quantiles(prob_values.size());	
    quantiles = h1_result.m_quantiles;

    //lets do CLs
    for(int p=0; p<pval.size();p++){
        vec_CLs.push_back(pval.at(p)/(1-prob_values.at(p)) );
    }

    TFile * fp = new TFile(("SBNfit_CLs_"+tag+".root").c_str(),"recreate");
    fp->cd();
    TCanvas *cp=new TCanvas();

    h0_pdf.SetStats(false);
    h1_pdf.SetStats(false);

    h0_pdf.Scale(1.0/h0_pdf.Integral("width"));
    h1_pdf.Scale(1.0/h1_pdf.Integral("width"));

    h0_pdf.SetLineColor(kRed-7);
    h1_pdf.SetLineColor(kBlue-4);
    h0_pdf.SetFillColor(kRed-7);
    h1_pdf.SetFillColor(kBlue-4);
    h0_pdf.SetFillStyle(3445);
    h1_pdf.SetFillStyle(3454);

    h0_pdf.Draw("hist");

    double maxval =std::max(  h0_pdf.GetMaximum(),h1_pdf.GetMaximum());
    double minval = 0;
    std::cout<<"SBNcls::CalcCLS() || Minimum value: "<<minval<<" Maximum value: "<<maxval<<std::endl;
    h0_pdf.SetMinimum(minval);
    h0_pdf.SetMaximum(maxval*1.35);

    double maxbin = max_plot;
    double minbin = min_plot;
    std::cout<<"SBNcls::CalcCLS() || Minimum Bin: "<<minbin<<" Maximum bin: "<<maxbin<<std::endl;
    //h0_pdf.GetXaxis()->SetRangeUser(minbin<0 ? minbin*1.2: minbin*0.8, maxbin*0.8);
    h0_pdf.GetXaxis()->SetRangeUser(min_plot,max_plot);


    bool draw_both = true;

    std::vector<std::string> quantile_names = {"-2#sigma","-1#sigma","Median","+1#sigma","+2#sigma"};
    std::vector<int> cols ={kYellow-7, kGreen+1, kBlack,kGreen+1, kYellow-7};	

    if(draw_both){
        for(int i=0; i< quantiles.size(); i++){
            if(quantiles.size()!=pval.size() || quantiles.size() != prob_values.size() || quantiles.size() != vec_CLs.size()){
             //   std::cout<<quantiles.size()<<" "<<pval.size()<<" "<<prob_values.size()<<" "<<vec_CLs.size()<<std::endl;
             //   std::cout<<"Something Amiss"<<std::endl;
            }
            TLine *l = new TLine(quantiles.at(i),0.0, quantiles.at(i),maxval*1.05);
            l->SetLineColor(cols.at(i));
            l->SetLineWidth(2);
            TLatex * qnam = new TLatex();
            qnam->SetTextSize(0.045);
            qnam->SetTextAlign(12);  //align at top
            qnam->SetTextAngle(-90);
            qnam->DrawLatex(quantiles.at(i), maxval*1.3 ,quantile_names.at(i).c_str());
            l->Draw("same");

            TLatex * qvals = new TLatex();
            qvals->SetTextSize(0.03);
            qvals->SetTextAlign(32);
            double sigma_val = pval2sig(pval.at(i));
            std::string whatsigma = to_string_prec(sigma_val,1)+"#sigma";
            if(sigma_val==0.0){
                whatsigma = "inf ";
            }

            std::string a_string;
            if(pval[i]>0.001){
                a_string = to_string_prec(pval.at(i),3);
            }else{
                a_string = "10^{"+to_string_prec(log10(pval[i]),2)+"}";
            }

            std::string details =  ("#splitline{"+quantile_names.at(i)+"}{1-#beta(" +to_string_prec(1-prob_values.at(i),3) + ") #alpha("+ a_string +" | "+whatsigma+ ") CL_{s}("+to_string_prec(vec_CLs.at(i),3)+")}");
            std::string details2 =  ("#splitline{"+quantile_names.at(i)+"}{1-#beta(" +to_string_prec(1-prob_values.at(i),10) + ") #alpha("+ to_string_prec(pval.at(i),10) +" | "+to_string_prec(pval2sig(pval.at(i)),1)+ "#sigma) CL_{s}("+to_string_prec(vec_CLs.at(i),10)+")}");
            std::cout<<details2<<std::endl;
            qvals->DrawLatexNDC(0.875, 0.2+i*0.1,details.c_str()  );
        }
    }

    /*
       TLine *lcv = new TLine(central_value_chi,minval,central_value_chi, maxval);
       lcv->SetLineColor(kBlack);
       lcv->SetLineStyle(2);
       lcv->SetLineWidth(2);
       TLatex * cvnam = new TLatex();
       cvnam->SetTextSize(0.045);
       cvnam->SetTextAlign(12);  //align at top    
       cvnam->SetTextAngle(-90);
       cvnam->DrawLatex(central_value_chi, maxval*1.3 ,"CV");
       lcv->Draw("same");
       */

//    std::string cv_details =  ("#splitline{CV}{#alpha("+ to_string_prec(pval.back(),5) +" | "+to_string_prec(pval2sig(pval.back()),5)+ "#sigma)}");
 //   std::cout<<cv_details<<std::endl;	

    //chi^2 prob bit
    std::vector<double> analytical_chi;
    std::vector<double> analytical_prob;

    double analytical_sum =0;
    for(double t=0; t< maxbin*10; t+=0.01){
        analytical_chi.push_back(t);
        analytical_prob.push_back( gsl_ran_chisq_pdf(t,h1->num_bins_total_compressed)   );
        analytical_sum +=0.01*analytical_prob.back();
    }

    for(auto &p:analytical_prob){
        //        p =p/analytical_sum;
    }

    TGraph *analytical_graph = new TGraph(analytical_chi.size(),&analytical_chi[0],&analytical_prob[0]);
    analytical_graph->SetLineColor(kRed);
    if(which_mode==0)analytical_graph->Draw("same");


    TLegend *leg = new TLegend(0.7,0.7,0.89,0.89);
    leg->SetLineWidth(0);
    leg->SetFillStyle(0);
    leg->AddEntry(&h0_pdf,"H_{0}","lf");
    if(draw_both)leg->AddEntry(&h1_pdf,"H_{1}","lf");
    if(which_mode==0)leg->AddEntry(analytical_graph,("#chi^{2} PDF "+std::to_string(h0->num_bins_total_compressed)+" dof").c_str(),"l");
    leg->Draw();

    if(which_mode==0){
        h0_pdf.GetXaxis()->SetTitle("#chi^{2}");
    }else if(which_mode==1){
        h0_pdf.GetXaxis()->SetTitle("#Delta #chi^{2} = #chi^{2}_{H0} - #chi^{2}_{H1} ");
    }
    h0_pdf.GetYaxis()->SetTitle("PDF");

    if(draw_both) h1_pdf.Draw("hist same");	


    cp->Write();	
    cp->SaveAs(("SBNfit_Cls_"+tag+".pdf").c_str(),"pdf");	
    fp->Close();

    return 0;

}

int SBNcls::runConstraintTest(){

    double N_h1 = h1->GetTotalEvents();
    double N_h0 = h0->GetTotalEvents();

    chi_h0.InitRandomNumberSeeds(10);
    chi_h1.InitRandomNumberSeeds(10);
   
    
    //Get 3 matricies
    TMatrixD frac_cov_zerod = chi_h0.matrix_fractional_covariance;
    for(int i=0; i< h0->num_bins_total ; i++){
        for(int j=0; j< h0->num_bins_total ; j++){
           if(i!=j) frac_cov_zerod(i,j)=0; 
        }
    }

    TMatrixD frac_cov_stat = chi_h0.matrix_fractional_covariance;
    frac_cov_stat.Zero();

    SBNchi chi_h0_zerod(*h0, frac_cov_zerod);
    SBNchi chi_h0_stat(*h0);
    

    float *h0_corein = new float[h0->num_bins_total_compressed];
    float *h1_corein = new float[h0->num_bins_total_compressed];

    for(int i=0; i< h0->num_bins_total_compressed; i++) {
        h0_corein[i] = chi_h0.core_spectrum.collapsed_vector[i];
        h1_corein[i] = chi_h1.core_spectrum.collapsed_vector[i];
    }

    std::vector<double> sx;
    std::vector<double> c_norm;
    std::vector<double> c_zerod;
    std::vector<double> c_stat;

    for(double s=0.001; s< 5; s+=0.1){
        sx.push_back(s);

        SBNspec tmp = (*h1);
        tmp.Scale("nu_uBooNE_1g1p_ncdelta",s);
        tmp.CollapseVector();
    
        for(int i=0; i< h0->num_bins_total_compressed; i++) {
            h1_corein[i] = tmp.collapsed_vector[i];
        }

        double chi = chi_h0.CalcChi_CNP(h0_corein , h1_corein);
        double chi_zerod = chi_h0_zerod.CalcChi_CNP(h0_corein , h1_corein);
        double chi_stat = chi_h0_stat.CalcChi_CNP(h0_corein , h1_corein);
        std::cout<<s<<" "<<chi<<" "<<chi_zerod<<" "<<chi_stat<<std::endl;

        c_norm.push_back(chi);
        c_zerod.push_back(chi_zerod);
        c_stat.push_back(chi_stat);

    }

    TCanvas *c = new TCanvas();
    c->cd();

    TGraph *g_norm = new TGraph(sx.size(),&sx[0],&c_norm[0]);
    TGraph *g_zerod = new TGraph(sx.size(),&sx[0],&c_zerod[0]);
    TGraph *g_stat = new TGraph(sx.size(),&sx[0],&c_stat[0]);

    g_stat->Draw("ac");
    g_stat->SetLineColor(kRed);
    g_norm->Draw("c same");
    g_norm->SetLineColor(kBlue);
    g_zerod->Draw("c same");
    g_zerod->SetLineColor(kGreen);

    c->Draw();
    c->SaveAs("cons_test.pdf","pdf");

    return 0;

}



/*double SBNcls::NPCalculator(SBNchi * chi_H0, SBNchi *chi_H1, SBNspec * spec_H0, SBNspec * spec_H1){
  return 0;
  }*/
