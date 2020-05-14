# Write the 29 xml files

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
  <subchannel name="bnb_main"/>
  <subchannel name="bnb_lowE"/>
  <subchannel name="nue"     />
  <subchannel name="dirt"    />
  <subchannel name="extbnb"  />
</channel>

<plotpot value=4.4e+19/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="4.72e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb_main"
      additional_weight="( ADDITIONAL_WEIGHT * (nu_energy_true>400) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="1.63e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb_lowE"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="9.8e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_dirt_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="2.62e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_dirt"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.435" maxevents="100000" pot="4.4e19">
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


# post-selection
postsel_dict = { "nbins": [ 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18, 18 ],
                 "xlow": [ 15., -101.5, 15., 0., 0.6, 0., 0., 0., 300., 0., 0., 0., 0., 0., 0., 0., 0., 70., 50.,
                           -math.pi, 0., 5., 20., -1., -math.pi, 0., 5., 50., -1. ], 
                 "xhigh": [ 241.25, 101.5, 1021.8, 0.6, 2.8, 6.3, 6.3, 800., 1200., 1., math.pi, 400., 0.4, 2., 0.8, 6e5, 2000., 600., 1000.,
                            math.pi, math.pi, 200., 600., 1., math.pi, math.pi, 150., 500., 1. ], 
                 "file_name": "input_to_sbnfit_v40_1mu1p_run1_May13.root" }
sel_dict = { "postsel": postsel_dict } 

# 29 variables...
var_list = [ "x_reco", "y_reco", "z_reco",
             "eta_reco",
             "openang_reco", "sum_thetas_reco", "sum_phis_reco",
             "charge_near_trunk_reco",
             "nu_energy_reco",
             "phiT_reco", "alphaT_reco", "pT_reco", "pT_ratio_reco",
             "Bjx_reco", "Bjy_reco",
             "Q2_reco", "sph_reco", "Q0_reco", "Q3_reco",
             "lepton_phi_reco", "lepton_theta_reco", "lepton_length_reco", "lepton_KE_reco", "lepton_cos_theta_reco",
             "proton_phi_reco", "proton_theta_reco", "proton_length_reco", "proton_KE_reco", "proton_cos_theta_reco" ]
units = [ "cm", "cm", "cm", "", "rad", "rad", "rad", "ADC", "MeV", "", "", "MeV", "", "", "", "MeV^2", "", "MeV", "MeV",
          "rad", "rad", "cm", "MeV", "", "rad", "rad", "cm", "MeV", "" ]

# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the binning based on pre vs. post selection
    nbins = sel_dict[sel]["nbins"]
    xlow  = sel_dict[sel]["xlow"]
    xhigh = sel_dict[sel]["xhigh"]
    # Also set the input file name
    file_name = sel_dict[sel]["file_name"]

    # Set the weights
    additional_weight = "xsec_corr_weight"

    # Loop over the variables...
    for i in range(len(var_list)):
        
        var_xml_str = xml_str
        
        edges = [ xlow[i] + ((xhigh[i] - xlow[i])/nbins[i])*j for j in range(nbins[i]+1) ]
        edges_str = ''
        for bin_edge in edges:
            edges_str += str(bin_edge)
            edges_str += " "
        edges_str = edges_str.strip()
        #print var_list[i], edges_str
        
        var_xml_str = var_xml_str.replace("UNIT", units[i])
        var_xml_str = var_xml_str.replace("BIN_EDGES", edges_str)
        var_xml_str = var_xml_str.replace("FILE_NAME", file_name)
        var_xml_str = var_xml_str.replace("VAR_NAME", var_list[i])
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
