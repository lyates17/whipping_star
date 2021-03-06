# Write the xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0" ?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="MeV">
  <bins
      edges="200 300 400 500 600 700 800 900 1000 1100 1200"
      />
  <subchannel name="nue"/>
  <subchannel name="bnb"/>
  <!-- <subchannel name="dirt"/> -->
  <subchannel name="extbnb"/>
  <subchannel name="lee"/>
</channel>

<channel name="1mu1p" unit="MeV">
  <bins
      edges="300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000"
      />
  <subchannel name="bnb"   />
  <subchannel name="dirt"  />
  <subchannel name="extbnb"/>
</channel>

<plotpot value=6.96e20/>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight * (bdt_score>RUN1_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( xsec_corr_weight * (bdt_score>RUN3_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="4.715e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * (bdt_score>RUN1_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="8.987e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * (bdt_score>RUN3_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="1.012e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( 1.0 * (bdt_score>RUN1_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="1.536e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( 1.0 * (bdt_score>RUN3_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*lee_weight * (bdt_score>RUN1_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*lee_weight * (bdt_score>RUN3_BDT_CUT_VALUE) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1mu1p_run1_Jun29.root" scale="0.242" maxevents="100000" pot="4.715e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1mu1p_run3_Jun29.root" scale="0.758" maxevents="100000" pot="8.988e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="1.631e21">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="1.512e21">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN1_FILE_NAME" scale="0.242" maxevents="100000" pot="1.012e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_RUN3_FILE_NAME" scale="0.758" maxevents="100000" pot="1.536e20">
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
  <!-- <whitelist>XSecShape_CCMEC_UBGenie</whitelist> -->
  <whitelist>RPA_CCQE_UBGenie</whitelist>
  <!-- <whitelist>RPA_CCQE_Reduced_UBGenie</whitelist> -->
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
  <variation pattern="_UBGenie" weight_formula="1./ub_tune_weight"/>
</WeightMaps>
"""

# step scan information
#cut_values = [ 0.5, 0.6, 0.7, 0.8, 0.9 ]
cut_values = [ 0.5, 0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95 ]
#print cut_values

# input file information
sel1e1p_run1_file_name = "input_to_sbnfit_v40_1e1p_run1_Jul08_opt.root"
sel1e1p_run3_file_name = "input_to_sbnfit_v40_1e1p_run3_Jul08_opt.root"
sel1mu1p_run1_file_name = "input_to_sbnfit_v40_1mu1p_run1_Jun29.root"
sel1mu1p_run3_file_name = "input_to_sbnfit_v40_1mu1p_run3_Jun29.root"

# Loop over everything, write the xmls...
for i in range(len(cut_values)):
        for j in range(len(cut_values)):
        
                var_xml_str = xml_str
        
                var_xml_str = var_xml_str.replace("SEL1E1P_RUN1_FILE_NAME", sel1e1p_run1_file_name)
                var_xml_str = var_xml_str.replace("SEL1E1P_RUN3_FILE_NAME", sel1e1p_run3_file_name)
                var_xml_str = var_xml_str.replace("SEL1MU1P_RUN1_FILE_NAME", sel1mu1p_run1_file_name)
                var_xml_str = var_xml_str.replace("SEL1MU1P_RUN3_FILE_NAME", sel1mu1p_run3_file_name)
                var_xml_str = var_xml_str.replace("RUN1_BDT_CUT_VALUE", "{:0.2f}".format(cut_values[i]) )
                var_xml_str = var_xml_str.replace("RUN3_BDT_CUT_VALUE", "{:0.2f}".format(cut_values[j]) )
                
                output = "./%s/%s.xml" % (outdir, "opt{:02d}-{:02d}".format( int(cut_values[i]*100.), int(cut_values[j]*100.) ))
                with open(output, 'w') as f:
                        f.write(var_xml_str)

print "Done!"
