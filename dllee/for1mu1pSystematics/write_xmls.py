# Write the 2*28 xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0" ?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1mu1p" unit="UNIT">
  <bins
      edges="BIN_EDGES"
      />
  <subchannel name="bnb"     />
  <subchannel name="dirt"    />
  <subchannel name="extbnb"  />
</channel>

<plotpot value=6.82e20/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="4.715e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="0.744" maxevents="100000" pot="8.988e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="1.631e+21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="0.744" maxevents="100000" pot="1.512e+21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="9.803e+22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="0.744" maxevents="100000" pot="4.707e+22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_dirt_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000" pot="2.619e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_dirt"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="0.256" maxevents="100000" pot="1.012e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
      additional_weight="1"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="0.744" maxevents="100000" pot="1.536e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
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
  <!-- <whitelist>XSecShape_CCMEC_UBGenie</whitelist> -->
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
  <variation pattern="_UBGenie" weight_formula="1./ub_tune_weight"/>
</WeightMaps>
"""


# file name information
run1_file_name = "input_to_sbnfit_v40_1mu1p_run1_Jul15.root"
run3_file_name = "input_to_sbnfit_v40_1mu1p_run3_Jul15.root"

# weighting information
weight_str = "xsec_corr_weight"

# var_dict with 31 variables... (nbins, xlow, xhigh, units)
var_dict = { "x_reco": (14,15.,241.25,"cm"),
             "y_reco": (14,-101.5,101.5,"cm"),
             "z_reco": (14,15,1021.8,"cm"),
             "openang_reco": (14,0.6,2.8,"rad"),
             "sum_thetas_reco": (14,0.,math.pi,"rad"),
             "sum_phis_reco": (14,1.5,4.,"rad"),
             "charge_near_trunk_reco": (14,0.,600.,"ADC"),
             "nu_energy_reco": (20,200.,1200.,"MeV"),
             "phiT_reco": (14,0.,1.,""),
             "alphaT_reco": (14,0,math.pi,""),
             "pT_reco": (14,0.,320.,"MeV"),
             "pT_ratio_reco": (14,0.,0.4,""),
             "Bjx_reco": (14,0.2,1.8,""),
             "Bjy_reco": (14,.05,0.75,""),
             "BjxB_reco": (14,0.2,1.8,""),
             "BjyB_reco": (14,.05,0.75,""),
             "Q2_reco": (14,0.,6e5,"MeV^2"),
             "Q0_reco": (14,70.,600.,"MeV"),
             "Q3_reco": (14,200.,1000.,"MeV"),
             "sph_reco": (14,0.,1000.,""),
             "sphB_reco": (14,0.,1000.,""),
             "lepton_phi_reco": (14,-math.pi,math.pi,"rad"),
             "lepton_theta_reco": (14,0.2,2.8,"rad"),
             "lepton_length_reco": (14,20.,200.,"cm"),
             "lepton_KE_reco": (14,50.,600.,"MeV"),
             "lepton_cos_theta_reco": (14,-1.,1.,""),
             "proton_phi_reco": (14,-math.pi,math.pi,"rad"),
             "proton_theta_reco": (14,0.,2.,"rad"),
             "proton_length_reco": (14,5.,100.,"cm"),
             "proton_KE_reco": (14,50.,500.,"MeV"),
             "proton_cos_theta_reco": (14,0.,1.,"")
}

# dummy sel_dict
sel_dict = { 'sel': [] }

# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the weight string
    additional_weight = weight_str

    # Loop over the variables...
    for var in var_dict:
        
        var_xml_str = xml_str
        
        nbins = int(var_dict[var][0])
        xlow  = float(var_dict[var][1])
        xhigh = float(var_dict[var][2])
        units = var_dict[var][3]

        edges = [ xlow + ((xhigh-xlow)/nbins)*i for i in range(nbins+1) ]
        edges_str = ''
        for bin_edge in edges:
            edges_str += str(bin_edge)
            edges_str += " "
        edges_str = edges_str.strip()
        
        var_xml_str = var_xml_str.replace("UNIT", units)
        var_xml_str = var_xml_str.replace("BIN_EDGES", edges_str)
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name)
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("VAR_NAME", var)
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var)
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
