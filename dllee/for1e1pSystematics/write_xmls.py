# Write the N xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0" ?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="UNIT">
  <bins
      edges="BIN_EDGES"
      />
  <subchannel name="bnb"/>
  <subchannel name="nue"/>
</channel>

<plotpot value=6.818e20/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="4.716e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="4.090e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="8.882e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="8.977e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="RUN2_SCALE" maxevents="100000" pot="9.209e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="4.719e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="2.908e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="2.489e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="6.914e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="5.913e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT )"
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


# variable and bin information
var_list = [ 'nu_energy_reco', 'eta_reco', 'pT_reco', 'alphaT_reco', 'sphB_reco', 'pzEnu_reco', 'charge_near_trunk_reco', 'Q0_reco','Q3_reco', 'sum_thetas_reco','sum_phis_reco',
             'pT_ratio_reco', 'proton_theta_reco', 'proton_phi_reco', 'min_shr_frac_reco', 'max_shr_frac_reco', 'BjxB_reco', 'BjyB_reco', 'proton_KE_reco', 'lepton_KE_reco',
             'lepton_theta_reco', 'lepton_phi_reco', 'openang_reco', 'x_reco', 'y_reco', 'z_reco', 'bdt_score', 'mpid_muon_score', 'mpid_proton_score', 'mpid_electron_score',
             'shr_charge_ratio_reco', 'shr_consistency_reco', 'nu_energy_QE_lepton_reco', 'nu_energy_QE_proton_reco' ]
N_bins = [ 10 for x in var_list ]
N_bins[0] = 12  # using 12 bins for energy
bin_list = [ (0,1200),(0,0.6),(0,800),(0,math.pi),(0,5000),(-800,300),
             (0,800),(100,700),(0,1400),(0,2*math.pi),(0,2*math.pi),
             (0,1),(0,math.pi),(-math.pi,math.pi),(-1,1),(-1,1),(0,3),
             (0,1),(60,500),(35,1200),(0,math.pi),
             (-math.pi,math.pi),(0,math.pi),(0,256),(-117,117),(0,1036),
             (0,1),(0,1),(0,1),(0,1),(0,3),(0,5),
             (0,1200),(0,1200) ]

# input file information
run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run1_Feb09.root"
run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run2_Feb09.root"
run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_run3_Feb09.root"

# set the CV weights

# selection-specific information
final_dict = {}
final_dict['run1_scale'] = 0.256  # using numbers from Nick, I think...
final_dict['run2_scale'] = 0.388
final_dict['run3_scale'] = 0.356
final_dict['weight'] = "xsec_corr_weight*dllee_pi0_weight"
#highE_dict = {}
#highE_dict['run1_scale'] = 1.746 / (1.746 + 5.072)  # for Run 1, using numbers from Nick (August 12th)
#highE_dict['run3_scale'] = 5.072 / (1.746 + 5.072)  # for Run 2+3, using numbers from Nick (August 12th)
#highE_dict['weight'] = "xsec_corr_weight * (nu_energy_reco>700)"
#blind_dict = {}
#blind_dict['run1_scale'] = 25 / float(15+39+35)       # for Run 1, using numbers from Jarrett (July 19th)
#blind_dict['run3_scale'] = (39+35) / float(15+39+35)  # for Run 2+3, using numbers from Jarrett (July 19th)
#blind_dict['weight'] = "xsec_corr_weight"
sel_dict = { "final": final_dict } #, "highE": highE_dict, "blind": blind_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the POT scale factors
    run1_scale = sel_dict[sel]['run1_scale']
    run2_scale = sel_dict[sel]['run2_scale']
    run3_scale = sel_dict[sel]['run3_scale']
    # Set additional weight
    additional_weight = sel_dict[sel]['weight']

    # Loop over the variables...
    for i in range(len(var_list)):
        
        var_xml_str = xml_str

        # Get the bin edges
        xlow  = float(bin_list[i][0])
        xhigh = float(bin_list[i][1])
        nbins = N_bins[i]
        edges = [ xlow + ((xhigh - xlow)/nbins)*j for j in range(nbins+1) ]
        edges_str = ''
        for bin_edge in edges:
            edges_str += str(bin_edge)
            edges_str += " "
        edges_str = edges_str.strip()
        
        var_xml_str = var_xml_str.replace("UNIT", "unit")
        var_xml_str = var_xml_str.replace("BIN_EDGES", edges_str)
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name)
        var_xml_str = var_xml_str.replace("RUN2_FILE_NAME", run2_file_name)
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("RUN1_SCALE", str(run1_scale))
        var_xml_str = var_xml_str.replace("RUN2_SCALE", str(run2_scale))
        var_xml_str = var_xml_str.replace("RUN3_SCALE", str(run3_scale))
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i] )
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
