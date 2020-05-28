# Write the 31 xml files

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


<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_BNB_SCALE" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_BNB_SCALE" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_bnb"
      additional_weight="( ADDITIONAL_WEIGHT * ((nu_pdg==14)||(nu_pdg==-14)) )"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN1_FILE_NAME" scale="RUN1_NUE_SCALE" maxevents="100000">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/RUN3_FILE_NAME" scale="RUN3_NUE_SCALE" maxevents="100000">
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
N_vars = 31
N_bins = 10
bin_list = [(700,2700),(0,0.6),(0,1200),(0,math.pi),(0,3000),(-1750,400),(0,1000),(100,1000),(100,1000),(0.5,5.0),(0,2*math.pi),(0,1),(0,math.pi),(-math.pi,math.pi),(0,1),
            (0.2,1),(0,3),(0,1),(60,500),(0,1400),(20,140),(10,80),(0,math.pi),(-math.pi,math.pi),(0,math.pi),(0,256),(-117,117),(0,1036),(0,3),(0,math.pi),(0.9,1)]

# input file information
run1_file_name = "input_to_sbnfit_v40_1e1p_run1_May21.root"
run3_file_name = "input_to_sbnfit_v40_1e1p_run3_May21.root"

# set the CV weights
additional_weight = "xsec_corr_weight"

# selection-specific information
opendata_dict = {}
opendata_dict['run1_bnb_scale'] = float(4.4e19) / float(4.715e20)
opendata_dict['run1_nue_scale'] = float(4.4e19) / float(9.803e22)
opendata_dict['run3_bnb_scale'] = float(8.8e18) / float(8.987e20)
opendata_dict['run3_nue_scale'] = float(8.8e18) / float(4.707e22)
sideband_dict = {}
sideband_dict['run1_bnb_scale'] = float(1.558e20) / float(4.715e20)
sideband_dict['run1_nue_scale'] = float(1.558e20) / float(9.803e22)
sideband_dict['run3_bnb_scale'] = (float(1.70e20) + float(1.63e20)) / float(8.987e20)  # scaling Run 3 prediction to Run 2+3
sideband_dict['run3_nue_scale'] = (float(1.70e20) + float(1.63e20)) / float(4.707e22)
sel_dict = { "opendata": opendata_dict, "sideband": sideband_dict }


# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the POT scale factors
    run1_bnb_scale = sel_dict[sel]['run1_bnb_scale']
    run1_nue_scale = sel_dict[sel]['run1_nue_scale']
    run3_bnb_scale = sel_dict[sel]['run3_bnb_scale']
    run3_nue_scale = sel_dict[sel]['run3_nue_scale']

    # Loop over the variables...
    for i in range(N_vars):
        
        var_xml_str = xml_str
        
        xlow  = float(bin_list[i][0])
        xhigh = float(bin_list[i][1])
        nbins = N_bins
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
        var_xml_str = var_xml_str.replace("RUN1_BNB_SCALE", str(run1_bnb_scale))
        var_xml_str = var_xml_str.replace("RUN1_NUE_SCALE", str(run1_nue_scale))
        var_xml_str = var_xml_str.replace("RUN3_BNB_SCALE", str(run3_bnb_scale))
        var_xml_str = var_xml_str.replace("RUN3_NUE_SCALE", str(run3_nue_scale))
        var_xml_str = var_xml_str.replace("VAR_NAME", "var{:02d}".format(i) )
        var_xml_str = var_xml_str.replace("ADDITIONAL_WEIGHT", additional_weight)
            
        output = "./auto/%s__%s.xml" % (sel, "var{:02d}".format(i))
        with open(output, 'w') as f:
            f.write(var_xml_str)
        

print "Done!"
