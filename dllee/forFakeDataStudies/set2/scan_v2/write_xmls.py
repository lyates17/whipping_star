# Write the xml files

import math
import subprocess,os

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="MeV">
  <bins
      edges="200 300 400 500 600 700 800 900 1000 1100 1200"
      />
  <subchannel name="bnb"/>
  <subchannel name="lee"/>
</channel>

<channel name="1mu1p" unit="MeV">
  <bins
      edges="250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1050 1100 1150 1200"
      />
  <subchannel name="bnb"/>
</channel>

<plotpot value=7.458e20/>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run1_Jul15.root" scale="0.485" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run3_Jul15.root" scale="0.515" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run1_Jul15.root" scale="0.485" maxevents="100000" pot="4.715e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run3_Jul15.root" scale="0.515" maxevents="100000" pot="8.987e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( xsec_corr_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run1_Jul15.root" scale="0.485" maxevents="100000" pot="9.803e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*lee_weight*LEE_SCALE )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1e1p_run3_Jul15.root" scale="0.515" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_lee"
      additional_weight="( xsec_corr_weight*lee_weight*LEE_SCALE )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1mu1p_run3_Jul30.root" scale="0.515" maxevents="100000" pot="8.987e20">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * (nu_energy_true>400) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1mu1p_run3_Jul30.root" scale="0.515" maxevents="100000" pot="1.512e21">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="( xsec_corr_weight * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/input_to_sbnfit_v40_1mu1p_run3_Jul30.root" scale="0.515" maxevents="100000" pot="4.707e22">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="xsec_corr_weight"
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

scale_list = [ 0.02*i for i in range(101) ]


# Loop over everything, write the xmls...
for scale in scale_list:

    var_xml_str = xml_str
    var_xml_str = var_xml_str.replace("LEE_SCALE", str(float(scale)))

    var_dir = os.path.join(outdir, "{:03d}".format(int(scale*100)))
    subprocess.call("mkdir -p %s" % var_dir, shell=True)

    output = os.path.join(var_dir, "sens.xml")
    with open(output, 'w') as f:
        f.write(var_xml_str)

print "Done!"
