# Write the N xml files

import math
import subprocess

outdir = "auto"
subprocess.call("mkdir -p %s" % outdir, shell=True)

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="UNIT">
  <bins
      edges="BIN_EDGES"
      />
  <subchannel name="nue"/>
  <subchannel name="bnb"/>
  <!-- <subchannel name="dirt"/> -->
  <subchannel name="extbnb"/>
</channel>


<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN2_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN2_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN2_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ncpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="0.356" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_ccpi0_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN3_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( ADDITIONAL_WEIGHT  * ((RUN1_POT)/dllee_pot_weight) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_extbnb"
      additional_weight="( ADDITIONAL_WEIGHT  * (((RUN2_POT)+(RUN3_POT))/dllee_pot_weight) )"
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


# input file information
run1_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_{}_run1_Apr07.root"
run2_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_{}_run2_Apr07.root"
run3_file_name = "input_to_sbnfit_v48_Sep24_withExtraGENIE_1e1p_{}_run3_Apr07.root"

# variable and bin information
var_list = [ 'nu_energy_reco', 'eta_reco', 'pT_reco', 'alphaT_reco', 'sphB_reco', 'pzEnu_reco', 'charge_near_trunk_reco', 'Q0_reco','Q3_reco', 'sum_thetas_reco','sum_phis_reco',
             'pT_ratio_reco', 'proton_theta_reco', 'proton_phi_reco', 'min_shr_frac_reco', 'max_shr_frac_reco', 'BjxB_reco', 'BjyB_reco', 'proton_KE_reco', 'lepton_KE_reco',
             'lepton_theta_reco', 'lepton_phi_reco', 'openang_reco', 'x_reco', 'y_reco', 'z_reco', 'mpid_muon_score', 'mpid_proton_score', 'mpid_electron_score',
             'shr_charge_ratio_reco', 'shr_consistency_reco', 'nu_energy_QE_lepton_reco', 'nu_energy_QE_proton_reco', 'dllee_bdt_score_avg' ]
N_bins = [ 10 for x in var_list ]
N_bins[0]  = 12  # using 12 bins for energies...
N_bins[31] = 12
N_bins[32] = 12
bin_list = [ (0,1200),(0,0.6),(0,800),(0,math.pi),(0,5000),(-800,300),
             (0,800),(100,700),(0,1400),(0,2*math.pi),(0,2*math.pi),
             (0,1),(0,math.pi),(-math.pi,math.pi),(-1,1),(-1,1),(0,3),
             (0,1),(60,500),(35,1200),(0,math.pi),
             (-math.pi,math.pi),(0,math.pi),(0,256),(-117,117),(0,1036),
             (0,1),(0,1),(0,1),(0,3),(0,5),
             (0,1200),(0,1200),(0,1) ]

# POT information -- using nuumbers from Nick (April 7th)
C1_POT = float(1.558e+20) + float(1.129e+17) + float(1.869e+19)
D2_POT = float(1.63e+20)  + float(2.964e+19) + float(1.239e+19)
E1_POT = float(5.923e+19)
F1_POT = float(4.3e+19)
G1_POT = float(1.701e+20) + float(2.97e+19)  + float(1.524e+17)

# selection-specific information
final_dict = {}
# using numbers from summer 2020 filtered data samples
final_dict['run1_pot'] = C1_POT
final_dict['run2_pot'] = D2_POT + E1_POT
final_dict['run3_pot'] = F1_POT + G1_POT
final_dict['weight']   = "xsec_corr_weight*dllee_pi0_weight * (dllee_bdt_score_avg>=0.95)"
final_dict['bdt_xlow'] = 0.95
highE_dict = {}
highE_dict['run1_pot'] = C1_POT
highE_dict['run2_pot'] = D2_POT + E1_POT
highE_dict['run3_pot'] = F1_POT + G1_POT
highE_dict['weight']   = "xsec_corr_weight*dllee_pi0_weight * (dllee_bdt_score_avg>=0.95)"
highE_dict['bdt_xlow'] = 0.95
lowBDT_dict = {}
lowBDT_dict['run1_pot'] = C1_POT
lowBDT_dict['run2_pot'] = D2_POT + E1_POT
lowBDT_dict['run3_pot'] = G1_POT  # lowBDT is missing F1
lowBDT_dict['weight']   = "xsec_corr_weight*dllee_pi0_weight"
lowBDT_dict['bdt_xlow'] = 0.
loose_dict = {}
loose_dict['run1_pot'] = float(4.403e+19)  # open 5e19
loose_dict['run2_pot'] = 0.
loose_dict['run3_pot'] = float(8.786e+18)  # open 1e19
loose_dict['weight']   = "xsec_corr_weight*dllee_pi0_weight"
loose_dict['bdt_xlow'] = 0.
sel_dict = { "FinalSelection": final_dict , "HighE": highE_dict, "LowBDT": lowBDT_dict, "KinCut": loose_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the POT for each run
    run1_pot = sel_dict[sel]['run1_pot']
    run2_pot = sel_dict[sel]['run2_pot']
    run3_pot = sel_dict[sel]['run3_pot']
    # Set additional weight
    additional_weight = sel_dict[sel]['weight']

    # Loop over the variables...
    for i in range(len(var_list)):
        
        var_xml_str = xml_str

        # Get the bin edges
        xlow  = float(bin_list[i][0])
        if 'bdt' in var_list[i]:
            xlow = float(sel_dict[sel]['bdt_xlow'])
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
        var_xml_str = var_xml_str.replace("RUN1_FILE_NAME", run1_file_name.format(sel))
        var_xml_str = var_xml_str.replace("RUN2_FILE_NAME", run2_file_name.format(sel))
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name.format(sel))
        var_xml_str = var_xml_str.replace("RUN1_POT", str(run1_pot))
        var_xml_str = var_xml_str.replace("RUN2_POT", str(run2_pot))
        var_xml_str = var_xml_str.replace("RUN3_POT", str(run3_pot))
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i] )
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
