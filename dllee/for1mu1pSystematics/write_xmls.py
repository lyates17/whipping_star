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
  <subchannel name="nue"     />
  <subchannel name="dirt"    />
  <subchannel name="extbnb"  />
</channel>

<plotpot value=1e19/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="BNB_POT">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_lowE_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="BNB_LOWE_POT">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="NUE_POT">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_dirt_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="DIRT_POT">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_dirt"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="EXT_POT">
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
xlow = [ 15., -101.5, 15., 0.6, 0., 1.5, 0., 300., 0., 0., 0., 0., 0.2, 0.05, 0., 0., 70., 200.,
         -math.pi, 0.2, 20., 50., -1., -math.pi, 0., 5., 50., -1. ]
xhigh = [ 241.25, 101.5, 1021.8, 2.8, 6.3, 4., 800., 1000., 1., math.pi, 320., 0.4, 1.8, 0.75, 6e5, 2000., 600., 1000.,
          math.pi, 2.8, 200., 600., 1., math.pi, 2., 100., 500., 1. ]
nbins = [ 14 for i in range(len(xlow)) ]
weight_str = "xsec_corr_weight"

# Run-specific information
run1_dict = { "file_name": "input_to_sbnfit_v40_1mu1p_run1_May27.root",
              "bnb_pot": 4.71579e+20,
              "bnb_lowE_pot": 1.63103516179e+21,
              "nue_pot": 9.80259e+22,
              "dirt_pot": 2.61947e+20,
              "extbnb_pot": 1.0121450159021741e+20
}
run3_dict = { "file_name": "input_to_sbnfit_v40_1mu1p_run3_May27.root",
              "bnb_pot": 8.98773223801e+20,
              "bnb_lowE_pot": 1.51234621011e+21,
              "nue_pot": 4.70704675581e+22,
              "dirt_pot": 2.61947e+20,  # there isn't actually a Run 3 dirt sample, this is just a dummy value...
              "extbnb_pot": 1.5357641809380714e+20
}
sel_dict = { "run1": run1_dict, "run3": run3_dict } 

# 29 variables...
var_list = [ "x_reco", "y_reco", "z_reco",
             "openang_reco", "sum_thetas_reco", "sum_phis_reco",
             "charge_near_trunk_reco",
             "nu_energy_reco",
             "phiT_reco", "alphaT_reco", "pT_reco", "pT_ratio_reco",
             "Bjx_reco", "Bjy_reco",
             "Q2_reco", "sph_reco", "Q0_reco", "Q3_reco",
             "lepton_phi_reco", "lepton_theta_reco", "lepton_length_reco", "lepton_KE_reco", "lepton_cos_theta_reco",
             "proton_phi_reco", "proton_theta_reco", "proton_length_reco", "proton_KE_reco", "proton_cos_theta_reco" ]
units = [ "cm", "cm", "cm", "rad", "rad", "rad", "ADC", "MeV", "", "", "MeV", "", "", "", "MeV^2", "", "MeV", "MeV",
          "rad", "rad", "cm", "MeV", "", "rad", "rad", "cm", "MeV", "" ]

# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the input file name and POT information based on the Run
    file_name    = sel_dict[sel]["file_name"]
    bnb_pot      = sel_dict[sel]["bnb_pot"]
    bnb_lowE_pot = sel_dict[sel]["bnb_lowE_pot"]
    nue_pot      = sel_dict[sel]["nue_pot"]
    dirt_pot     = sel_dict[sel]["dirt_pot"]
    extbnb_pot   = sel_dict[sel]["extbnb_pot"]
    # Also set the weight string
    additional_weight = weight_str

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
        var_xml_str = var_xml_str.replace("BNB_POT", str(bnb_pot))
        var_xml_str = var_xml_str.replace("BNB_LOWE_POT", str(bnb_lowE_pot))
        var_xml_str = var_xml_str.replace("NUE_POT", str(nue_pot))
        var_xml_str = var_xml_str.replace("DIRT_POT", str(dirt_pot))
        var_xml_str = var_xml_str.replace("EXT_POT", str(extbnb_pot))
            
        output = "./auto/%s__%s.xml" % (sel, var_list[i])
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
