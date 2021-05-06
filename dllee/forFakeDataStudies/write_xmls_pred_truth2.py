# Write the xml files

import math
import os,subprocess

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="MeV">
  <bins
      edges="200 300 400 500 600 700 800 900 1000 1100 1200"
      />
  <subchannel name="nueCCQE"/>
  <subchannel name="nueOther"/>
  <subchannel name="numuCCQE"/>
  <subchannel name="numuMEC"/>
  <subchannel name="numuPi0"/>
  <subchannel name="numuPiCh"/>
  <subchannel name="numuOther"/>
  <subchannel name="offVtx"/>
  <subchannel name="lee"/>
</channel>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nueCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nueCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nueOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type!=1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nueOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type!=1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuCCQE"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1001)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuMEC"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_mode==10)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1004||nu_interaction_type==1006||nu_interaction_type==1008||nu_interaction_type==1011||nu_interaction_type==1013||nu_interaction_type==1015||nu_interaction_type==1080||nu_interaction_type==1086||nu_interaction_type==1090)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPi0"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuPiCh"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*(nu_interaction_type==1003||nu_interaction_type==1005||nu_interaction_type==1007||nu_interaction_type==1009||nu_interaction_type==1010||nu_interaction_type==1012||nu_interaction_type==1014||nu_interaction_type==1016||nu_interaction_type==1017||nu_interaction_type==1021||nu_interaction_type==1028||nu_interaction_type==1032||nu_interaction_type==1079||nu_interaction_type==1085)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_numuOther"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * ((dllee_scedr<5.0)*((nu_interaction_type==1000*nu_interaction_mode!=10)||(nu_interaction_type==1002)||(nu_interaction_type>1032*nu_interaction_type<1079)||(nu_interaction_type>1090))) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_offVtx"
      additional_weight="( SET_TUNE_WEIGHT * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) * (dllee_scedr>5.0) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( SET_TUNE_WEIGHT*SET_LEE_SCALE*lee_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( SET_TUNE_WEIGHT*SET_LEE_SCALE*lee_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>
"""


# fake data set list
fakedata_list = [ 'set1', 'set2', 'set3', 'set4' ] #, 'set5', 'set7' ]
# ... for set5, just read it off Nick's plot

# input file information
sel1e1p_run1_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run1_Apr07.root"
sel1e1p_run3_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run3_Apr07.root"

# fake data tune information
fakedata_tune_dict = {}
fakedata_tune_dict['set1'] = 'spline_weight*rootino_weight'
fakedata_tune_dict['set2'] = 'set2_comb_weight*rootino_weight'
fakedata_tune_dict['set3'] = 'set3_comb_weight*rootino_weight'
fakedata_tune_dict['set4'] = 'set3_comb_weight*rootino_weight'

# fake data LEE signal scaling information
fakedata_lee_scale_dict = {}
fakedata_lee_scale_dict['set1'] = 3.5
fakedata_lee_scale_dict['set2'] = 0.0
fakedata_lee_scale_dict['set3'] = 0.0
fakedata_lee_scale_dict['set4'] = 1.0

# fake data POT information
fakedata_pot_dict = {}
fakedata_pot_dict['set1'] = [ float(1.936e+20), float(3.000e+20) ]
fakedata_pot_dict['set2'] = [ float(4.013e+20), float(3.852e+20) ]
fakedata_pot_dict['set3'] = [ float(4.025e+20), float(3.969e+20) ]
fakedata_pot_dict['set4'] = [ float(3.908e+20), float(3.924e+20) ]
fakedata_pot_dict['set5'] = [ float(7.006e+20), 0. ]
fakedata_pot_dict['set7'] = [ float(1.838e+20), float(2.05e+20)  ]

# cut variable information
sel1e1p_bdt_cut_var = 'dllee_bdt_score_avg'


# Loop over everything, write the xmls...
for tag in fakedata_list:

    outdir = tag
    subprocess.call("mkdir -p %s" % outdir, shell=True)
    
    set_tune_weight = fakedata_tune_dict[tag]
    set_lee_scale = fakedata_lee_scale_dict[tag]
    run1_data_pot = fakedata_pot_dict[tag][0]
    run3_data_pot = fakedata_pot_dict[tag][1]
    
    var_xml_str = xml_str
    
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
    var_xml_str = var_xml_str.replace("SET_TUNE_WEIGHT", set_tune_weight)
    var_xml_str = var_xml_str.replace("SET_LEE_SCALE", "{:.1f}".format(set_lee_scale) )
    var_xml_str = var_xml_str.replace("RUN1_DATA_POT", "{:.3e}".format(run1_data_pot) )
    var_xml_str = var_xml_str.replace("RUN3_DATA_POT", "{:.3e}".format(run3_data_pot) )
    var_xml_str = var_xml_str.replace("SEL1E1P_BDT_CUT_VAR", sel1e1p_bdt_cut_var)
                        
    output = os.path.join(outdir, "dllee_sens_pred_truth2_{}.xml".format(tag))
    with open(output, 'w') as f:
        f.write(var_xml_str)

print "Done!"
