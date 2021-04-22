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

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.356" maxevents="100000">
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
      additional_weight="( xsec_corr_weight_v40*lee_weight * ((RUN1_DATA_POT)/dllee_pot_weight) * (SEL1E1P_LEE_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight_v40*lee_weight * ((RUN3_DATA_POT)/dllee_pot_weight) * (SEL1E1P_LEE_BDT_CUT_VAR>=0.95) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>
"""


# fake data set list
fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]

# input file information
sel1e1p_run1_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run1_Apr07.root"
sel1e1p_run3_file_name  = "input_to_sbnfit_v40-v48_FakeData_1e1p_FinalSelection_run3_Apr07.root"

# fake data POT information
fakedata_pot_dict = {}
fakedata_pot_dict['set1'] = [ float(1.936e+20), float(3.000e+20) ]
fakedata_pot_dict['set2'] = [ float(4.013e+20), float(3.852e+20) ]
fakedata_pot_dict['set3'] = [ float(4.025e+20), float(3.969e+20) ]
fakedata_pot_dict['set4'] = [ float(3.908e+20), float(3.924e+20) ]
fakedata_pot_dict['set5'] = [ float(7.006e+20), 0. ]

# construct the 1e1p BDT variable for use with fake data that contains events that were included in the training samples
#   note: everything *except* fake data set 1 signal and fake data set 5 was used in training
Nbdts_e = 20
sel1e1p_training_sample_var = '(('
for i in range(Nbdts_e):
    sel1e1p_training_sample_var += 'dllee_bdt_score{:02d}+'.format(i)
sel1e1p_training_sample_var = sel1e1p_training_sample_var[:-1]  # remove a trailing '+'
sel1e1p_training_sample_var += ')/{})'.format(Nbdts_e)

# cut variable information
sel1e1p_bdt_cut_var_dict = {}
sel1e1p_bdt_cut_var_dict['set1'] = [ sel1e1p_training_sample_var, 'dllee_bdt_score_avg' ]
sel1e1p_bdt_cut_var_dict['set2'] = [ sel1e1p_training_sample_var, sel1e1p_training_sample_var ]
sel1e1p_bdt_cut_var_dict['set3'] = [ sel1e1p_training_sample_var, sel1e1p_training_sample_var ]
sel1e1p_bdt_cut_var_dict['set4'] = [ sel1e1p_training_sample_var, sel1e1p_training_sample_var ]
sel1e1p_bdt_cut_var_dict['set5'] = [ 'dllee_bdt_score_avg', 'dllee_bdt_score_avg' ]

# Loop over everything, write the xmls...
for tag in fakedata_list:

    outdir = tag
    subprocess.call("mkdir -p %s" % outdir, shell=True)
    
    run1_data_pot = fakedata_pot_dict[tag][0]
    run3_data_pot = fakedata_pot_dict[tag][1]
    sel1e1p_bdt_cut_var = sel1e1p_bdt_cut_var_dict[tag][0]
    sel1e1p_lee_bdt_cut_var = sel1e1p_bdt_cut_var_dict[tag][1]

    var_xml_str = xml_str
    
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
    var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
    var_xml_str = var_xml_str.replace("RUN1_DATA_POT", "{:.3e}".format(run1_data_pot) )
    var_xml_str = var_xml_str.replace("RUN3_DATA_POT", "{:.3e}".format(run3_data_pot) )
    var_xml_str = var_xml_str.replace("SEL1E1P_BDT_CUT_VAR", sel1e1p_bdt_cut_var)
    var_xml_str = var_xml_str.replace("SEL1E1P_LEE_BDT_CUT_VAR", sel1e1p_lee_bdt_cut_var)
                    
    output = os.path.join(outdir, "dllee_sens_pred_1e1p-only_{}.xml".format(tag))
    with open(output, 'w') as f:
        f.write(var_xml_str)

print "Done!"
