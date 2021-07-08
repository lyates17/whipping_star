# Write the N xml files

import math
import subprocess
import numpy as np

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="UNIT">
  <bins
      edges="BIN_EDGES"
      />
  <subchannel name="nue"/>
  <subchannel name="bnb"/>
  <!-- <subchannel name="dirt"/> -->
  <subchannel name="extbnb"/>
</channel>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN2_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN2_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( ADDITIONAL_WEIGHT * (((RUN2_POT)+(RUN3_POT))/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<variation_list>
  <whitelist>expskin_FluxUnisim</whitelist>
  <whitelist>horncurrent_FluxUnisim</whitelist>
  <whitelist>kminus_PrimaryHadronNormalization</whitelist>
  <whitelist>kplus_PrimaryHadronFeynmanScaling</whitelist>
  <whitelist>kzero_PrimaryHadronSanfordWang</whitelist>
  <whitelist>nucleoninexsec_FluxUnisim</whitelist>
  <whitelist>nucleonqexsec_FluxUnisim</whitelist>
  <whitelist>nucleontotxsec_FluxUnisim</whitelist>
  <whitelist>piminus_PrimaryHadronSWCentralSplineVariation</whitelist>
  <whitelist>pioninexsec_FluxUnisim</whitelist>
  <whitelist>pionqexsec_FluxUnisim</whitelist>
  <whitelist>piontotxsec_FluxUnisim</whitelist>
  <whitelist>piplus_PrimaryHadronSWCentralSplineVariation</whitelist>
  <whitelist>All_UBGenie</whitelist>
  <whitelist>XSecShape_CCMEC_UBGenie</whitelist>
  <whitelist>RPA_CCQE_UBGenie</whitelist>
  <whitelist>AxFFCCQEshape_UBGenie</whitelist>
  <whitelist>VecFFCCQEshape_UBGenie</whitelist>
  <whitelist>DecayAngMEC_UBGenie</whitelist>
  <whitelist>xsr_scc_Fa3_SCC</whitelist>
  <whitelist>xsr_scc_Fv3_SCC</whitelist>
  <whitelist>NormCCCOH_UBGenie</whitelist>
  <whitelist>NormNCCOH_UBGenie</whitelist>
  <whitelist>ThetaDelta2NRad_UBGenie</whitelist>
  <whitelist>Theta_Delta2Npi_UBGenie</whitelist>
  <whitelist>reinteractions_piminus_Geant4</whitelist>
  <whitelist>reinteractions_piplus_Geant4</whitelist>
  <whitelist>reinteractions_proton_Geant4</whitelist>
</variation_list>

<WeightMaps>
  <variation pattern="All_UBGenie" weight_formula="1.0/ub_tune_weight"/>
  <variation pattern="RPA_CCQE_UBGenie" weight_formula="1.0/ub_tune_weight"/>
  <variation pattern="AxFFCCQEshape_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="VecFFCCQEshape_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="DecayAngMEC_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="XSecShape_CCMEC_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="ThetaDelta2NRad_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="Theta_Delta2Npi_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="NormCCCOH_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
  <variation pattern="NormNCCOH_UBGenie" weight_formula="1.0/ub_tune_weight" mode="minmax"/>
</WeightMaps>
"""


# input file information
run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_FinalSelection_run1_Jul07.root"
run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_FinalSelection_run2_Jul07.root"
run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_FinalSelection_run3_Jul07.root"

# variable and bin information
var_list = [ 'nu_energy_reco', 'eta_reco', 'pT_reco', 'alphaT_reco', 'sphB_reco', 'pzEnu_reco', 'charge_near_trunk_reco',
             'Q0_reco','Q3_reco', 'sum_thetas_reco','sum_phis_reco', 'pT_ratio_reco', 'proton_theta_reco', 'proton_phi_reco',
             'min_shr_frac_reco', 'max_shr_frac_reco', 'BjxB_reco', 'BjyB_reco', 'proton_KE_reco', 'lepton_KE_reco',
             'lepton_theta_reco', 'lepton_phi_reco', 'openang_reco', 'x_reco', 'y_reco', 'z_reco',
             'dllee_bdt_score_avg', 'mpid_muon_score', 'mpid_proton_score', 'mpid_electron_score', 'shr_charge_ratio_reco', 'shr_consistency_reco',
             'nu_energy_QE_lepton_reco', 'nu_energy_QE_proton_reco', 'proton_length_reco', 'lepton_length_reco' ]

# POT information -- using numbers from Josh (June 29th), which correspond to near sideband filter
run1_pot = float(1.631e+20)
run2_pot = float(2.749e+20)
run3_pot = float(2.291e+20)

# selection-specific information
# Sample #1: 500 < Enu_1e1p < 1200, sigprob > 0.95
samp1_dict = {}
samp1_dict['weight'] = "xsec_corr_weight*dllee_pi0_weight * (nu_energy_reco>=500.)*(nu_energy_reco<1200.)*(dllee_bdt_score_avg>=0.95)"
samp1_dict['bin_ranges'] = [ (0,1200),(0,0.6),(0,800),(0,np.pi),(0,5000),(-800,300),
                             (0,800),(100,700),(0,1400),(0,2*np.pi),(0,2*np.pi),
                             (0,1),(0,np.pi),(-np.pi,np.pi),(-1,1),(-1,1),(0,3),
                             (0,1),(60,500),(35,1200),(0,np.pi),
                             (-np.pi,np.pi),(0,np.pi),(0,256),(-117,117),(0,1036),
                             (0.95,1.0),(0,1),(0,1),(0,1),(0,3),(0,5),
                             (0,1200),(0,1200),(0,100),(0,200) ]
samp1_dict['N_bins'] = [ 10 for x in var_list ]
for i in [0, 32, 33]:
    # using 12 bins for energies...
    samp1_dict['N_bins'][i] = 12
# Sample #2: 500 < Enu_1e1p < 700, sigprob > 0.95
samp2_dict = {}
samp2_dict['weight'] = "xsec_corr_weight*dllee_pi0_weight * (nu_energy_reco>=500.)*(nu_energy_reco<700.)*(dllee_bdt_score_avg>=0.95)"
samp2_dict['bin_ranges'] = samp1_dict['bin_ranges']
samp2_dict['N_bins'] = [ x/2 for x in samp1_dict['N_bins'] ]
# Sample #3: 0.7 < sigprob < 0.95, Enu_1e1p < 1200
samp3_dict = {}
samp3_dict['weight'] = "xsec_corr_weight*dllee_pi0_weight * (nu_energy_reco<1200.)*(dllee_bdt_score_avg>=0.7)*(dllee_bdt_score_avg<0.95)"
samp3_dict['bin_ranges'] = [ (0,1200),(0,0.6),(0,800),(0,np.pi),(0,5000),(-800,300),
                             (0,800),(100,700),(0,1400),(0,2*np.pi),(0,2*np.pi),
                             (0,1),(0,np.pi),(-np.pi,np.pi),(-1,1),(-1,1),(0,3),
                             (0,1),(60,500),(35,1200),(0,np.pi),
                             (-np.pi,np.pi),(0,np.pi),(0,256),(-117,117),(0,1036),
                             (0.7,0.95),(0,1),(0,1),(0,1),(0,3),(0,5),
                             (0,1200),(0,1200),(0,100),(0,200) ]
samp3_dict['N_bins'] = samp1_dict['N_bins']
sel_dict = { "samp1": samp1_dict , "samp2": samp2_dict, "samp3": samp3_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set additional weight
    additional_weight = sel_dict[sel]['weight']

    # Loop over the variables...
    for i in range(len(var_list)):
        
        var_xml_str = xml_str

        # Get the bin edges
        xlow  = float(sel_dict[sel]['bin_ranges'][i][0])
        xhigh = float(sel_dict[sel]['bin_ranges'][i][1])
        nbins = int(sel_dict[sel]['N_bins'][i])
        edges = [ xlow + ((xhigh - xlow)/nbins)*j for j in range(nbins+1) ]
        edges_str = ''
        for bin_edge in edges:
            edges_str += str(bin_edge)
            edges_str += " "
        edges_str = edges_str.strip()
        
        var_xml_str = var_xml_str.replace("UNIT", "unit")
        var_xml_str = var_xml_str.replace("BIN_EDGES", edges_str)
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name)
        var_xml_str = var_xml_str.replace("RUN2_FILE_NAME", run2_file_name)
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("RUN1_POT", str(run1_pot))
        var_xml_str = var_xml_str.replace("RUN2_POT", str(run2_pot))
        var_xml_str = var_xml_str.replace("RUN3_POT", str(run3_pot))
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i])
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
