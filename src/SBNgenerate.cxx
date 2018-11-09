#include "SBNgenerate.h"
//#include "MCEventWeight.h"

using namespace sbn;

SBNgenerate::SBNgenerate(std::string xmlname) {
	NeutrinoModel nullModel;
	SBNgenerate(xmlname, nullModel);
}

SBNgenerate::SBNgenerate(std::string xmlname, NeutrinoModel inModel ) : SBNconfig(xmlname), nu_model(inModel) {

//	gROOT->ProcessLine("#include <map>");
//	gROOT->ProcessLine("#include <vector>");
//	gROOT->ProcessLine("#include <string>");

	//gSystem->Load("../src/libranch_weightsMapDict.so");

//	std::string dict_location = "../../dict/AutoDict_map_string__vector_double____cxx.so";
//	gSystem->Load(  (dict_location).c_str());

	//	gSystem->Load("/uboone/app/users/markrl/sbnfit/whipping_star/src/mdict_h.so");
	//
	//std::cout<<"Trying to load dictionary: "<<dict_location<<std::endl;
	//

	std::map<std::string, int> parameter_sims;

	//Initialise the central value SBNspec.
	SBNspec tm(xmlname,-1,false);
	spec_central_value = tm;
	spec_osc_sin  = tm;
	spec_osc_sinsq  = tm;

	int num_files = multisim_file.size();

	for(auto &fn: multisim_file){
		files.push_back(new TFile(fn.c_str()));
	}


	for(int i=0; i<multisim_name.size(); i++){
		trees.push_back((TTree*)files.at(i)->Get(multisim_name.at(i).c_str()) );
	}

  for(int i=0; i<multisim_file.size(); i++){

  	if( multisim_file_friend_treename_map.count(multisim_file.at(i))>0){
			for(int k=0; k< multisim_file_friend_treename_map.at(multisim_file.at(i)).size(); k++){

	  		std::string treefriendname = (multisim_file_friend_treename_map.at(multisim_file.at(i))).at(k);
	  		std::string treefriendfile = (multisim_file_friend_map.at(multisim_file.at(i))).at(k);

				std::cout<<"SBNmultisim::SBNmultisim\t|| Adding a friend tree  "<< treefriendfile<<" to file "<<multisim_file.at(i)<<std::endl;

       	trees.at(i)->AddFriend( treefriendname.c_str()   ,  treefriendfile.c_str()   );
			}
    }
  }

	std::vector<int> nentries;
	for(auto &t: trees){
		nentries.push_back(t->GetEntries());
	}

	f_weights = new std::vector<std::map<std::string, std::vector<double>>* >(num_files,0);


	for(int i=0; i< num_files; i++){
		delete f_weights->at(i);	f_weights->at(i) = 0;
		trees.at(i)->SetBranchAddress("weights", &f_weights->at(i) );
		delete f_weights->at(i);	f_weights->at(i) = 0;
		for(int k=0; k<branch_variables.at(i).size(); k++){
			std::cout<<"Setting Branch: "<<branch_variables.at(i).at(k)->name<<std::endl;
			trees.at(i)->SetBranchAddress( branch_variables.at(i).at(k)->name.c_str(), branch_variables.at(i).at(k)->GetValue() );

			if(branch_variables.at(i).at(k)->GetOscillate()){
				trees.at(i)->SetBranchAddress( branch_variables.at(i).at(k)->true_param_name.c_str(), branch_variables.at(i).at(k)->GetTrueValue() );
				trees.at(i)->SetBranchAddress( branch_variables.at(i).at(k)->true_L_name.c_str(), branch_variables.at(i).at(k)->GetTrueL() );
			}
		}
	}

	std::cout<<"SBNgenerate::SBNgenerate\t|| -------------------------------------------------------------\n";
	std::cout<<"SBNgenerate::SBNgenerate\t|| -------------------------------------------------------------\n";
	std::vector<double> base_vec (spec_central_value.num_bins_total,0.0);

	for(int j=0;j<num_files;j++){

		delete f_weights->at(j);
		f_weights->at(j)=0;

		for(int i=0; i< std::min(  multisim_maxevents.at(j)  ,nentries.at(j)); i++){
			trees.at(j)->GetEntry(i);
			std::map<std::string, std::vector<double>> * thisfWeight = f_weights->at(j);

			if(i%100==0) std::cout<<"SBNgenerate::SBNgenerate\t|| On event: "<<i<<" of "<<nentries[j]<<" from File: "<<multisim_file[j]<<std::endl;

			double global_weight = 1;
			global_weight = global_weight*multisim_scale.at(j);

			if(thisfWeight->count("bnbcorrection_FluxHist")>0){
				global_weight = global_weight*thisfWeight->at("bnbcorrection_FluxHist").front();
			}

			if(std::isinf(global_weight) || global_weight != global_weight){
				std::cout<<"SBNgenerate::SBNgenerate\t|| ERROR  error @ "<<i<<" in File "<<multisim_file.at(j)<<" as its either inf/nan: "<<global_weight<<std::endl;
				exit(EXIT_FAILURE);
			}

			if( this->EventSelection(j) ){
				for(int t=0; t<branch_variables.at(j).size();t++){
					std::cout<<"Starting branch : "<<branch_variables.at(j).at(t)->name<<" "<<branch_variables.at(j).at(t)->associated_hist<<std::endl;
					//Need the histogram index, the value, the global bin...
					int ih = spec_central_value.map_hist.at(branch_variables.at(j).at(t)->associated_hist);
					double reco_var = *(static_cast<double*>(branch_variables.at(j).at(t)->GetValue()));
					int reco_bin = spec_central_value.GetGlobalBinNumber(reco_var,ih);

					//Find if this event should be oscillated
					if(branch_variables.at(j).at(t)->GetOscillate()){
						//Working
						double true_var = *(static_cast<double*>(branch_variables.at(j).at(t)->GetTrueValue()));
						double true_L = *(static_cast<double*>(branch_variables.at(j).at(t)->GetTrueL()));

						double osc_Probability_sin = nu_model.oscProbSin(true_var, true_L);
						double osc_Probability_sinsq = nu_model.oscProbSinSq(true_var, true_L);

						spec_osc_sinsq.hist.at(ih).Fill(reco_var, global_weight*osc_Probability_sinsq);
						spec_osc_sin.hist.at(ih).Fill(reco_var, global_weight*osc_Probability_sin);
						spec_central_value.hist.at(ih).Fill(reco_var,global_weight);
						std::cout<<"Reco: "<<reco_var<<" True: "<<true_var<<" L: "<<true_L<<" "<<osc_Probability_sin<<" "<<osc_Probability_sinsq<<" glob: "<<global_weight<<std::endl;
					}else{
						std::cout<<"Not Oscillated"<<std::endl;
						spec_central_value.hist.at(ih).Fill(reco_var,global_weight);
						spec_osc_sinsq.hist.at(ih).Fill(reco_var, global_weight);
						spec_osc_sin.hist.at(ih).Fill(reco_var, global_weight);
					//	std::cout<<reco_var<<" "<<std::endl;
					}
				}
			}
		} //end of entry loop
	}//end of file loop

	delete f_weights;

	/***************************************************************
	 *		Now some clean-up and Writing
	 * ************************************************************/

	for(auto &f: files){
		f->Close();
	}

}
/***************************************************************
 *		Some virtual functions for selection and histogram filling
 * ************************************************************/

int SBNgenerate::WritePrecomputedOscSpecs(std::string tag){
	spec_osc_sinsq.WriteOut(tag+"_SINSQ_dm_"+nu_model.mass_tag);
	spec_osc_sin.WriteOut(tag+"_SIN_dm_"+nu_model.mass_tag);

	return 0;
}


bool SBNgenerate::EventSelection(int which_file){
	return true;
}

int SBNgenerate::FillHistograms(int file, int uni, double wei){
	return 0;
}
