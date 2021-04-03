# Write the xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0" ?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="pi0" unit="UNIT">
  <bins
      edges="BIN_EDGES"
      />
  <subchannel name="bnb"   />
  <subchannel name="extbnb"/>
</channel>

<plotpot value=POT_VALUE/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="1.337e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="4.090e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="8.988e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="9.803e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="9.209e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="4.707e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="2.904e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN2AND3_SCALE" maxevents="100000" pot="2.488e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="6.953e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN2AND3_SCALE" maxevents="100000" pot="5.922e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="9.366e19">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_extbnb"
      additional_weight="1"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN2AND3_SCALE" maxevents="100000" pot="3.046e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_extbnb"
      additional_weight="1"
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


# POT information
run1_data_pot = float(1.746e+20)
run2_data_pot = float(2.050e+20) + float(6.507e+19)
run3_data_pot = float(4.3e+19) + float(2e+20)
total_data_pot = run1_data_pot + run2_data_pot + run3_data_pot
# scale factor information
run1_scale = run1_data_pot / total_data_pot
run2_scale = run2_data_pot / total_data_pot
run3_scale = run3_data_pot / total_data_pot
run2and3_scale = ( run2_data_pot + run3_data_pot ) / total_data_pot

# input files
run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_pi0_run1_Feb08.root"
run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_pi0_run2_Feb08.root"
run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_pi0_run3_Feb08.root"

# 6 variables...
var_list = [ "pi0_mass_reco", "Delta_mass_reco", "shower1_energy_reco", "shower2_energy_reco", "pi0_energy_reco", "pi0_momentum_reco" ]
units_list = [ "MeV", "MeV", "MeV", "MeV",  "MeV", "MeV" ]
nbins_list = [ 20, 20, 20, 20, 20, 20 ]
xlow_list  = [ 30., 1000, 80., 35., 100., 100. ]
xhigh_list = [ 350., 1400., 450., 300., 750., 700. ]

# additional weight
#additional_weight = "xsec_corr_weight"

# different selections
cv_weight_dict  = { "additional_weight": "xsec_corr_weight" }
pi0_weight_dict = { "additional_weight": "xsec_corr_weight*pi0_weight" }
sel_dict = { "cv_weighted": cv_weight_dict, "pi0_weighted": pi0_weight_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Loop over the variables...
    for i in range(len(var_list)):
        
        # Set the binning based on pre vs. post selection
        nbins = nbins_list[i]
        xlow  = float( xlow_list[i] )
        xhigh = float( xhigh_list[i] )

        var_xml_str = xml_str
        
        edges = [ xlow + ((xhigh - xlow)/nbins)*j for j in range(nbins+1) ]
        edges_str = ''
        for bin_edge in edges:
            edges_str += str(bin_edge)
            edges_str += " "
        edges_str = edges_str.strip()
        #print var_list[i], edges_str
        
        var_xml_str = var_xml_str.replace("UNIT", units_list[i])
        var_xml_str = var_xml_str.replace("BIN_EDGES", edges_str)
        var_xml_str = var_xml_str.replace("POT_VALUE", str(total_data_pot))
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name)
        var_xml_str = var_xml_str.replace("RUN2_FILE_NAME", run2_file_name)
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("RUN1_SCALE", str(run1_scale))
        var_xml_str = var_xml_str.replace("RUN2_SCALE", str(run2_scale))
        var_xml_str = var_xml_str.replace("RUN3_SCALE", str(run3_scale))
        var_xml_str = var_xml_str.replace("RUN2AND3_SCALE", str(run2and3_scale))
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i])
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", sel_dict[sel]["additional_weight"])
        
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
