# Write the 30 xml files

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

<plotpot value=7e20/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="4.72e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="8.99e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)||(nu_interaction_ccnc==1)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="9.80e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * (nu_energy_true>400) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="4.71e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="( ADDITIONAL_WEIGHT * (nu_energy_true>400) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_SCALE" maxevents="100000" pot="4.3e23">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_SCALE" maxevents="100000" pot="4.3e23">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
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


# variable and bin information
#var_list = [ 'Enu_1e1p','Eta','PT_1e1p','AlphaT_1e1p','SphB_1e1p','PzEnu_1e1p','ChargeNearTrunk','Q0_1e1p','Q3_1e1p','Thetas','Phis',
#             'PTRat_1e1p','Proton_ThetaReco','Proton_PhiReco','MinShrFrac','MaxShrFrac','BjXB_1e1p','BjYB_1e1p','Proton_Edep','Electron_Edep',
#             'Lepton_ThetaReco','Lepton_PhiReco','OpenAng','Xreco','Yreco','Zreco','BDTscore_1e1p','Muon MPID','Proton MPID','Electron MPID' ]
var_list = [ 'nu_energy_reco', 'eta_reco', 'pT_reco', 'alphaT_reco', 'sphB_reco', 'pzEnu_reco', 'charge_near_trunk_reco', 'Q0_reco','Q3_reco', 'sum_thetas_reco','sum_phis_reco',
             'pT_ratio_reco', 'proton_theta_reco', 'proton_phi_reco', 'min_shr_frac_reco', 'max_shr_frac_reco', 'BjxB_reco', 'BjyB_reco', 'proton_KE_reco', 'lepton_KE_reco',
             'lepton_theta_reco', 'lepton_phi_reco', 'openang_reco', 'x_reco', 'y_reco', 'z_reco', 'bdt_score', 'mpid_muon_score', 'mpid_proton_score', 'mpid_electron_score' ]
N_bins = [ 10 for x in var_list ]
N_bins[0] = 12
bin_list = [ (0,1200),(0,0.6),(0,800),(0,math.pi),(0,5000),(-1500,300),(0,800),(100,700),(0,1400),(0,2*math.pi),(0,2*math.pi),
             (0,1),(0,math.pi),(-math.pi,math.pi),(0,1),(0,1),(0,3),(0,1),(60,500),(0,1000),(math.pi/5,math.pi),
             (-math.pi,math.pi),(0,math.pi),(0,256),(-117,117),(0,1036),(0,1),(0,1),(0,1),(0,1) ]

# input file information
run1_file_name = "input_to_sbnfit_v40_1e1p_run1_Jul15.root"
run3_file_name = "input_to_sbnfit_v40_1e1p_run3_Jul15.root"

# set the CV weights
additional_weight = "xsec_corr_weight"

# selection-specific information
final_dict = {}
final_dict['run1_scale'] = 0.242  # for Run 1, using standard numbers from Pawel
final_dict['run3_scale'] = 0.758  # for Run 2+3, again using standard numbers from Pawel
highE_dict = {}
highE_dict['run1_scale'] = 1.56 / (1.56 + 1.63 + 1.70)           # for Run 1, using numbers from Jarrett  (July 16th)
highE_dict['run3_scale'] = (1.63 + 1.70) / (1.56 + 1.63 + 1.70)  # for Run 2+3, using numbers from Jarrett (July 16th)
sel_dict = { "final": final_dict, "highE": highE_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the POT scale factors
    run1_scale = sel_dict[sel]['run1_scale']
    run3_scale = sel_dict[sel]['run3_scale']

    # Loop over the variables...
    for i in range(len(var_list)):
        
        var_xml_str = xml_str
        
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
        var_xml_str = var_xml_str.replace("RUN3_FILE_NAME", run3_file_name)
        var_xml_str = var_xml_str.replace("RUN1_SCALE", str(run1_scale))
        var_xml_str = var_xml_str.replace("RUN3_SCALE", str(run3_scale))
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i] )
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
