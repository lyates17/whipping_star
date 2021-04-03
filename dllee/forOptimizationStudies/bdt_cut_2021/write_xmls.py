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
      edges="250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1050 1100 1150 1200"
      />
  <subchannel name="bnb"   />
  <!-- <subchannel name="nue"   /> -->
  <!-- <subchannel name="dirt"  /> -->
  <subchannel name="extbnb"/>
</channel>

<plotpot value=6.818e20/>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN2_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN2_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN1_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.356" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN3_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN1_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight  * ((RUN3_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN2_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight*lee_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (BDT_CUT_VAR>=BDT_CUT_VAL) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="2.949e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN2_FILE_NAME" scale="0.388" maxevents="100000" pot="4.090e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.356" maxevents="100000" pot="5.103e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight*dllee_pi0_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight*dllee_pi0_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN2_FILE_NAME" scale="0.388" maxevents="100000" pot="9.209e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight*dllee_pi0_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.356" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight*dllee_pi0_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="1.012e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.744" maxevents="100000" pot="1.536e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
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
cut_variables = [ "dllee_bdt_score_median", "dllee_bdt_score_avg" ]
# TODO: if adding lower BDT values, also add extbnb sub-channel for 1e1p selection
#cut_values = [ 0.95, 0.9, 0.85, 0.8 ]
cut_values = [ 0.7, 0.725, 0.75, 0.775, 0.8, 0.825, 0.85, 0.875, 0.9, 0.925, 0.95, 0.975 ]
#cut_values = [ 0.98, 0.985, 0.99, 0.995, 0.996, 0.997, 0.998, 0.999 ]
#print cut_values

# input file information
sel1e1p_run1_file_name  = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run1_Mar04.root"
sel1e1p_run2_file_name  = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run2_Mar04.root"
sel1e1p_run3_file_name  = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run3_Mar04.root"
sel1mu1p_run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run1_Feb08.root"
sel1mu1p_run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run2_Feb08.root"
sel1mu1p_run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run3_Feb08.root"

# data POT information
run1_data_pot = float(1.558e+20) + float(1.129e+17) + float(1.869e+19)
run2_data_pot = float(1.63e+20)  + float(2.964e+19) + float(1.239e+19) + float(5.923e+19)
run3_data_pot = float(4.3e+19)   + float(1.701e+20) + float(2.97e+19)  + float(1.524e+17)

# Loop over everything, write the xmls...
for var in cut_variables: 
        for val in cut_values:
                
                var_xml_str = xml_str
        
                var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
                var_xml_str = var_xml_str.replace("SEL1E1P_RUN2_FILE_NAME", sel1e1p_run2_file_name)
                var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
                var_xml_str = var_xml_str.replace("RUN1_DATA_POT", "{:.3e}".format(run1_data_pot) )
                var_xml_str = var_xml_str.replace("RUN2_DATA_POT", "{:.3e}".format(run2_data_pot) )
                var_xml_str = var_xml_str.replace("RUN3_DATA_POT", "{:.3e}".format(run3_data_pot) )
                var_xml_str = var_xml_str.replace("SEL1MU1P_RUN1_FILE_NAME", sel1mu1p_run1_file_name)
                var_xml_str = var_xml_str.replace("SEL1MU1P_RUN2_FILE_NAME", sel1mu1p_run2_file_name)
                var_xml_str = var_xml_str.replace("SEL1MU1P_RUN3_FILE_NAME", sel1mu1p_run3_file_name)
                var_xml_str = var_xml_str.replace("BDT_CUT_VAR", var)
                var_xml_str = var_xml_str.replace("BDT_CUT_VAL", "{:0.3f}".format(val))
                
                output = "./%s/%s.xml" % (outdir, "opt-{}-{:03d}".format( var.split('_')[-1], int(val*1000.) ))
                with open(output, 'w') as f:
                        f.write(var_xml_str)

print "Done!"
