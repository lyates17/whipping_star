# Write the 5 xml files

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
  <subchannel name="bnb"   />
  <subchannel name="nue"   />
  <subchannel name="dirt"  />
  <subchannel name="extbnb"/>
</channel>

<plotpot value=4.4e+19/>


<MultisimFile treename="sel1mu1p_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.093367" maxevents="100000" pot="4.4e19">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.000449" maxevents="100000" pot="4.4e19">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_dirt_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.168087" maxevents="100000" pot="4.4e19">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_dirt"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.435017" maxevents="100000" pot="4.4e19">
  <branch
      name="VAR_NAME"
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
  <variation pattern="_UBGenie" weight_formula="1./ub_tune_weight"/>
</WeightMaps>
"""


# post-selection
postsel_dict = { "nbins": [ 20, 20, 20, 20, 20 ],
                 "xlow": [ 0., 0., 0., 0., 0. ],
                 "xhigh": [ 1., 1., 1., 1., 1. ],
                 "file_name": "input_to_sbnfit_v40_forMPID_Apr27.root" }
sel_dict = { "postsel": postsel_dict } 

# 21 variables...
var_list = [ "proton_score", "eminus_score", "gamma_score", "muon_score", "pion_score" ]
units = [ "", "", "", "", "" ]

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
