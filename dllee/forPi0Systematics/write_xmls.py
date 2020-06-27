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
  <subchannel name="nue"   />
  <subchannel name="extbnb"/>
</channel>

<plotpot value=4.403e19/>


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="4.72e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="9.8e22">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_pi0_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="0.435" maxevents="100000" pot="4.4e19">
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
postsel_dict = { "nbins": [ 20, 30 ],
                 "xlow": [ 0., 900. ],
                 "xhigh": [ 400., 1800. ],
                 "file_name": "input_to_sbnfit_v40_pi0_run1_May20.root",
                 "weight_str": "xsec_corr_weight"
}
sel_dict = { "postsel": postsel_dict } 

# 2 variables...
var_list = [ "pi0_mass_reco", "Delta_mass_reco" ]
units = [ "MeV", "MeV" ]

# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the input file name and the weights
    file_name = sel_dict[sel]["file_name"]
    additional_weight = sel_dict[sel]["weight_str"]

    # Loop over the variables...
    for i in range(len(var_list)):
        
        # Set the binning based on pre vs. post selection
        nbins = sel_dict[sel]["nbins"][i]
        xlow  = float( sel_dict[sel]["xlow"][i] )
        xhigh = float( sel_dict[sel]["xhigh"][i] )

        var_xml_str = xml_str
        
        edges = [ xlow + ((xhigh - xlow)/nbins)*j for j in range(nbins+1) ]
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
