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
  <subchannel name="nue"/>
  <subchannel name="bnb"/>
  <subchannel name="lee"/>
</channel>

<channel name="1mu1p" unit="MeV">
  <bins
      edges="250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1050 1100 1150 1200"
      />
  <subchannel name="bnb"/>
</channel>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight_v40 * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight_v40 * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight_v40*lee_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight_v40*lee_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((RUN1_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight_v40 * ((RUN3_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (dllee_bdt_score_avg>=0.5) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>
"""


# fake data set list
fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5', 'set7' ]

# input file information
sel1e1p_run1_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run1_Apr07.root"
sel1e1p_run3_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run3_Apr07.root"
sel1mu1p_run1_file_name = "input_to_sbnfit_v40-v48_FakeData_1mu1p_run1_May05.root"
sel1mu1p_run3_file_name = "input_to_sbnfit_v40-v48_FakeData_1mu1p_run3_May05.root"

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
    
    run1_data_pot = fakedata_pot_dict[tag][0]
    run3_data_pot = fakedata_pot_dict[tag][1]
    
    var_xml_str = xml_str
    
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
    var_xml_str = var_xml_str.replace("SEL1MU1P_RUN1_FILE_NAME", sel1mu1p_run1_file_name)
    var_xml_str = var_xml_str.replace("SEL1MU1P_RUN3_FILE_NAME", sel1mu1p_run3_file_name)
    var_xml_str = var_xml_str.replace("RUN1_DATA_POT", "{:.3e}".format(run1_data_pot) )
    var_xml_str = var_xml_str.replace("RUN3_DATA_POT", "{:.3e}".format(run3_data_pot) )
    var_xml_str = var_xml_str.replace("SEL1E1P_BDT_CUT_VAR", sel1e1p_bdt_cut_var)
    
    output = os.path.join(outdir, "dllee_sens_pred_{}.xml".format(tag))
    with open(output, 'w') as f:
        f.write(var_xml_str)

print "Done!"
