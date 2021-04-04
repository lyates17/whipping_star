# Write the xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="MeV">
  <bins
      edges="200 300 400 500 600 700 800 900 1000 1100 1200"
      />
  <subchannel name="nue"/>
  <subchannel name="bnb"/>
  <!-- <subchannel name="dirt"/> -->
  <!-- <subchannel name="extbnb"/> -->
  <subchannel name="lee"/>
</channel>

<channel name="1mu1p" unit="MeV">
  <bins
      edges="200 250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1050 1100 1150 1200"
      />
  <subchannel name="bnb"   />
</channel>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN2_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN2_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.356" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN2_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=SEL1E1P_BDT_CUT_VAL) * (mpid_proton_score>=SEL1E1P_MPIDP_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN2_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN2_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( (((RUN2_DATA_POT)+(RUN3_DATA_POT))/dllee_pot_weight) * (SEL1MU1P_BDT_CUT_VAR>=SEL1MU1P_BDT_CUT_VAL) )"
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

# step scan information
sel1e1p_bdt_cut_variables  = [ "dllee_bdt_score_avg", "dllee_bdt_score_median" ]
sel1mu1p_bdt_cut_variables = [ "dllee_bdt_score_avg" ]
# TODO: if adding lower BDT values, also add extbnb sub-channel for 1e1p selection (not gonna happen though)
sel1e1p_bdt_cut_values   = [ 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
sel1mu1p_bdt_cut_values  = [ 0.5, 0.6, 0.7 ]
sel1e1p_mpidp_cut_values = [ -0.001, 0.2 ]

# input file information
sel1e1p_file_name_dict = {}
sel1e1p_file_name_dict["dllee_bdt_score_avg"]    = [ "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_avgscore_run1_Mar26.root",
                                                     "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_avgscore_run2_Mar26.root",
                                                     "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_avgscore_run3_Mar26.root" ]
sel1e1p_file_name_dict["dllee_bdt_score_median"] = [ "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_medianscore_run1_Mar26.root",
                                                     "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_medianscore_run2_Mar26.root",
                                                     "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_medianscore_run3_Mar26.root" ]
sel1mu1p_run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run1_Mar31.root"
sel1mu1p_run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run2_Mar31.root"
sel1mu1p_run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run3_Mar31.root"

# data POT information
# in theory (from docdb-26979, Table 3)...
run1_data_pot = float(1.683e+20)
run2_data_pot = float(2.674e+20)
run3_data_pot = float(0.439e+20) + float(2.166e+20)
# in practice, for summer 2020 filtered data samples...
#run1_data_pot = float(1.558e+20) + float(1.129e+17) + float(1.869e+19)
#run2_data_pot = float(1.63e+20)  + float(2.964e+19) + float(1.239e+19) + float(5.923e+19)
#run3_data_pot = float(4.3e+19)   + float(1.701e+20) + float(2.97e+19)  + float(1.524e+17)
# TODO: update with values from new filtered data samples

# Loop over everything, write the xmls...
for var_e in sel1e1p_bdt_cut_variables: 
    
    sel1e1p_run1_file_name = sel1e1p_file_name_dict[var_e][0]
    sel1e1p_run2_file_name = sel1e1p_file_name_dict[var_e][1]
    sel1e1p_run3_file_name = sel1e1p_file_name_dict[var_e][2]
    
    for var_m in sel1mu1p_bdt_cut_variables:
        
        for val_e in sel1e1p_bdt_cut_values:
            for val_m in sel1mu1p_bdt_cut_values:
                for val_p in sel1e1p_mpidp_cut_values:
                    
                    var_xml_str = xml_str
                    
                    var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
                    var_xml_str = var_xml_str.replace("SEL1E1P_RUN2_FILE_NAME", sel1e1p_run2_file_name)
                    var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
                    var_xml_str = var_xml_str.replace("SEL1MU1P_RUN1_FILE_NAME", sel1mu1p_run1_file_name)
                    var_xml_str = var_xml_str.replace("SEL1MU1P_RUN2_FILE_NAME", sel1mu1p_run2_file_name)
                    var_xml_str = var_xml_str.replace("SEL1MU1P_RUN3_FILE_NAME", sel1mu1p_run3_file_name)
                    var_xml_str = var_xml_str.replace("RUN1_DATA_POT", "{:.3e}".format(run1_data_pot) )
                    var_xml_str = var_xml_str.replace("RUN2_DATA_POT", "{:.3e}".format(run2_data_pot) )
                    var_xml_str = var_xml_str.replace("RUN3_DATA_POT", "{:.3e}".format(run3_data_pot) )
                    var_xml_str = var_xml_str.replace("SEL1E1P_BDT_CUT_VAR", var_e)
                    var_xml_str = var_xml_str.replace("SEL1E1P_BDT_CUT_VAL", "{:0.2f}".format(val_e))
                    var_xml_str = var_xml_str.replace("SEL1E1P_MPIDP_CUT_VAL", "{:0.3f}".format(val_p))
                    var_xml_str = var_xml_str.replace("SEL1MU1P_BDT_CUT_VAR", var_m)
                    var_xml_str = var_xml_str.replace("SEL1MU1P_BDT_CUT_VAL", "{:0.2f}".format(val_m))
                    
                    output = "./%s/%s.xml" % (outdir, "opt-{}-e{:02d}-{:02d}-m{:02d}".format( var_e.split('_')[-1], int(val_e*100), int(val_p*100), int(val_m*100) ))
                    with open(output, 'w') as f:
                        f.write(var_xml_str)

print "Done!"
