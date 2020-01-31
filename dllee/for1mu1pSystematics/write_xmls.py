# Write the 2*3*21 xml files

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

<plotpot value=3.456e+19/>


<MultisimFile treename="sel1mu1p_bnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="1.219e21">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_bnb"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_nue_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="1.314e23">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_nue"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_dirt_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="3.257e20">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_dirt"
      additional_weight="ADDITIONAL_WEIGHT"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>

<MultisimFile treename="sel1mu1p_extbnb_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/FILE_NAME" scale="1.0" maxevents="100000" pot="5.524e19">
  <branch
      name="VAR_NAME"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_extbnb"
      eventweight_branch_name="sys_weights"
      />
</MultisimFile>


<variation_list>
  GENIE_WHITELIST_STR
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
</variation_list>

<WeightMaps>
  <variation pattern="_Genie" weight_formula="1./ub_tune_weight"/>
</WeightMaps>
"""


# 2 selections...
# pre-selection
presel_dict = { "nbins": [ 40, 40, 40, 20, 20, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40 ],
                "xlow": [ 10., -106., 0., 250., 0., 0., 0., 0., 0.1, 0., 75., 0., 0., -1*math.pi, 5., 20., 0., -1*math.pi, 5., 40., 0. ],
                "xhigh": [ 250., 106., 1006., 1250., math.pi, 1400., math.pi, 4., 0.9, 1.0e6, 1.0e3, 1.4e3, math.pi, math.pi, 500., 700., math.pi, math.pi, 150., 1000., 1. ],
                "file_name": "input_to_sbnfit_v33_MaMvRES_Jan31_presel.root" }
# post-selection
postsel_dict = { "nbins": [ 12, 12, 12, 10, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12, 12 ],
                 "xlow": [ 10., -106., 0., 250., 0.8, 0., 0., 0., 0.1, 0., 75., 0., 0., -1*math.pi, 5., 20., 0., -1*math.pi, 5., 40., 0. ],
                 "xhigh": [ 250., 106., 1006., 1150., 3., 800., math.pi, 2., 0.8, 0.75e6, 0.65e3, 1.3e3, 3., math.pi, 500., 700., 3., math.pi, 150., 600., 1. ], 
                 "file_name": "input_to_sbnfit_v33_MaMvRES_Jan31.root" }
#sel_dict = { "presel": presel_dict, "postsel": postsel_dict }
sel_dict = { "postsel": postsel_dict } 

# 3 sets of plots...
# (1) untuned MCC9 (spline weight only), flux systematics
set1_dict = { "additional_weight": "spline_weight",
              "genie_whitelist_str": "<!-- <whitelist>All_Genie</whitelist> -->" }
# (2) tuned MCC9, flux systematics
set2_dict = { "additional_weight": "xsec_corr_weight",
              "genie_whitelist_str": "<!-- <whitelist>All_Genie</whitelist> -->" }
# (3) tuned MCC9, flux and All_Genie systematics
set3_dict = { "additional_weight": "xsec_corr_weight",
              "genie_whitelist_str": "<whitelist>All_Genie</whitelist>" }
set_dict = { "set1": set1_dict, "set2": set2_dict, "set3": set3_dict }


# 21 variables...
var_list = [ "x_reco", "y_reco", "z_reco",
             "nu_energy_reco",
             "openang_reco",
             "pT_reco", "alphaT_reco",
             "Bjx_reco", "Bjy_reco",
             "Q2_reco","Q0_reco", "Q3_reco",
             "lepton_theta_reco", "lepton_phi_reco", "lepton_length_reco", "lepton_KE_reco",
             "proton_theta_reco", "proton_phi_reco", "proton_length_reco", "proton_KE_reco",
             "pT_ratio_reco" ]
units = [ "cm", "cm", "cm", "MeV", "rad", "MeV", "", "", "", "MeV^2", "MeV", "MeV", "rad", "rad", "cm", "MeV", "rad", "rad", "cm", "MeV", "" ]

# Loop over everything, write the xmls...
for sel in sel_dict:

    # Set the binning based on pre vs. post selection
    nbins = sel_dict[sel]["nbins"]
    xlow  = sel_dict[sel]["xlow"]
    xhigh = sel_dict[sel]["xhigh"]
    # Also set the input file name
    file_name = sel_dict[sel]["file_name"]

    for plot_set in set_dict:
        
        # Set the weights and toggle genie systematics based on plot set
        additional_weight   = set_dict[plot_set]["additional_weight"]
        genie_whitelist_str = set_dict[plot_set]["genie_whitelist_str"]

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
            var_xml_str = var_xml_str.replace("GENIE_WHITELIST_STR", genie_whitelist_str)
            
            output = "./auto/%s_%s__%s.xml" % (sel, plot_set, var_list[i])
            with open(output, 'w') as f:
                f.write(var_xml_str)
                

print "Done!"
