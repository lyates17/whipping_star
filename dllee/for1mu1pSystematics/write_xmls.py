# Write the 34+3 xml files

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
  <!-- <subchannel name="dirt"    /> -->
  <subchannel name="extbnb"  />
</channel>

<plotpot value=TOTAL_POT/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="2.949e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="4.090e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="5.103e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="9.803e+22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="9.209e+22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="4.707e+22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="1.012e+20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
      additional_weight="1"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN2AND3_SCALE" maxevents="100000" pot="1.536e+20">
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
  <whitelist>RPA_CCQE_UBGenie</whitelist>
  <whitelist>AxFFCCQEshape_UBGenie</whitelist>
  <whitelist>VecFFCCQEshape_UBGenie</whitelist>
  <whitelist>DecayAngMEC_UBGenie</whitelist>
  <whitelist>XSecShape_CCMEC_UBGenie</whitelist>
  <whitelist>ThetaDelta2NRad_UBGenie</whitelist>
  <whitelist>Theta_Delta2Npi_UBGenie</whitelist>
  <whitelist>NormCCCOH_UBGenie</whitelist>
  <whitelist>NormNCCOH_UBGenie</whitelist>
  <whitelist>xsr_scc_Fa3_SCC</whitelist>
  <whitelist>xsr_scc_Fv3_SCC</whitelist>
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
run1_data_pot = float(1.558e+20) + float(1.129e+17) + float(1.869e+19)
run2_data_pot = (float(1.63e+20) + float(2.964e+19) + float(1.239e+19)) + float(5.923e+19)
run3_data_pot = (float(1.701e+20) + float(2.97e+19) + float(1.524e+17)) + float(4.3e+19)
total_data_pot = run1_data_pot + run2_data_pot + run3_data_pot
# scale factor information
run1_scale = run1_data_pot / total_data_pot
run2_scale = run2_data_pot / total_data_pot
run3_scale = run3_data_pot / total_data_pot

# file name information
run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run1_Feb08.root"
run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run2_Feb08.root"
run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1mu1p_run3_Feb08.root"

# weighting information
weight_str = "xsec_corr_weight"

# var_dict with 34 variables... (nbins, xlow, xhigh, units)
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
             #"Bjx_reco": (14,0.2,1.8,""),
             #"Bjy_reco": (14,.05,0.75,""),
             "BjxB_reco": (14,0.2,1.8,""),
             "BjyB_reco": (14,.05,0.75,""),
             "Q2_reco": (14,0.,float(6e5),"MeV^2"),
             "Q0_reco": (14,70.,600.,"MeV"),
             "Q3_reco": (14,200.,1000.,"MeV"),
             #"sph_reco": (14,0.,1000.,""),
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
             "proton_cos_theta_reco": (14,0.,1.,""),
             "mpid_eminus_score": (14,0.,1.,""),
             "mpid_muon_score": (14,0.,1.,""),
             "mpid_proton_score": (14,0.,1.,""),
             "mpid_gamma_score": (14,0.,1.,""),
             "mpid_pion_score": (14,0.,1.,""),
             "bdt_score": (14,0.,0.4,"")
}

# sel_dict
# selection name: [ total_data_pot, run1_scale, run2_scale, run3_scale ]
#sel_dict = { 'sel_total': [ total_data_pot, run1_scale, run2_scale, run3_scale ], 
#             'sel_run1':  [ run1_data_pot, 1., 0., 0. ], 
#             'sel_run2':  [ run2_data_pot, 0., 1., 0. ],
#             'sel_run3':  [ run3_data_pot, 0., 0., 1. ] }
sel_dict = { 'sel_total_withoutPi0Weights': [ total_data_pot, run1_scale, run2_scale, run3_scale, "xsec_corr_weight" ], 
             'sel_total_withPi0Weights':    [ total_data_pot, run1_scale, run2_scale, run3_scale, "xsec_corr_weight*dllee_pi0_weight" ]  }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the POT and associated scale strings
    total_pot_str = str(sel_dict[sel][0])
    run1_scale_str = str(sel_dict[sel][1])
    run2_scale_str = str(sel_dict[sel][2])
    run3_scale_str = str(sel_dict[sel][3])
    run2and3_scale_str = str( float(sel_dict[sel][2]+sel_dict[sel][3]) )
    # Set the weight string
    additional_weight = str(sel_dict[sel][4])

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
        var_xml_str = var_xml_str.replace("TOTAL_POT", total_pot_str)
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name)
        var_xml_str = var_xml_str.replace("RUN2_FILE_NAME", run2_file_name)
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("RUN1_SCALE", run1_scale_str)
        var_xml_str = var_xml_str.replace("RUN2_SCALE", run2_scale_str)
        var_xml_str = var_xml_str.replace("RUN3_SCALE", run3_scale_str)
        var_xml_str = var_xml_str.replace("RUN2AND3_SCALE", run2and3_scale_str)
        var_xml_str = var_xml_str.replace("VAR_NAME", var)
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var)
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
