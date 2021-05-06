# Write the xml files

import math
import os,subprocess

xml_str = """<?xml version="1.0"?>

<mode name="nu"/>
<detector name="uBooNE"/>

<channel name="1e1p" unit="MeV">
  <bins
      edges="200 300 400 500 600 700 800 900 1000 1100 1200"
      />
  <subchannel name="data"/>
</channel>

<channel name="1mu1p" unit="MeV">
  <bins
      edges="250 300 350 400 450 500 550 600 650 700 750 800 850 900 950 1000 1050 1100 1150 1200"
      />
  <subchannel name="data"/>
</channel>


<MultisimFile treename="sel_run1_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_data"
      additional_weight="( dllee_bdt_score_avg>=0.95 )"
      eventweight_branch_name="weights"
      />
</MultisimFile>

<MultisimFile treename="sel_run3_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1E1P_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1e1p_data"
      additional_weight="( dllee_bdt_score_avg>=0.95 )"
      eventweight_branch_name="weights"
      />
</MultisimFile>


<MultisimFile treename="sel_run1_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_data"
      eventweight_branch_name="weights"
      />
</MultisimFile>

<MultisimFile treename="sel_run3_tree" filename="/uboone/data/users/yatesla/othersys_mcc9/input_to_sbnfit/SEL1MU1P_FILE_NAME" scale="1.0" maxevents="100000">
  <branch
      name="nu_energy_reco"
      type="double"
      associated_subchannel="nu_uBooNE_1mu1p_data"
      eventweight_branch_name="weights"
      />
</MultisimFile>
"""


# fake data set list
fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5', 'set7' ]

# input file information
sel1e1p_file_name  = "input_to_sbnfit_fakedata_{}_1e1p_Apr14.root"
sel1mu1p_file_name = "input_to_sbnfit_fakedata_{}_1mu1p_Apr20.root"

# Loop over everything, write the xmls...
for tag in fakedata_list:

    outdir = tag
    subprocess.call("mkdir -p %s" % outdir, shell=True)
    
    var_xml_str = xml_str
    
    var_xml_str = var_xml_str.replace("SEL1E1P_FILE_NAME", sel1e1p_file_name.format(tag))
    var_xml_str = var_xml_str.replace("SEL1MU1P_FILE_NAME", sel1mu1p_file_name.format(tag))
    
    output = os.path.join(outdir, "dllee_sens_fakedata_{}.xml".format(tag))
    with open(output, 'w') as f:
        f.write(var_xml_str)

print "Done!"
