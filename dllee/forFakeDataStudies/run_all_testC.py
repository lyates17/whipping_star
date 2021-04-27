import os,subprocess

topdir = os.getcwd()

fakedata_list = [ 'set1', 'set2', 'set3', 'set4', 'set5' ]

grid_min = '1e-4'
grid_max_dict = {}
grid_max_dict['set1'] = '10'
grid_max_dict['set2'] = '5'
grid_max_dict['set3'] = '5'
grid_max_dict['set4'] = '5'
grid_max_dict['set5'] = '5'

#Npes = 2500  # SBNfit default
Npes = 10000

for tag in fakedata_list:

    workdir = os.path.join(topdir, tag)
    os.chdir(workdir)
    
    grid_str = '{} {} {:d}'.format( grid_min, grid_max_dict[tag], 20*int(round(float(grid_max_dict[tag]))) )
    cmd_base = "$SBNFIT_LIBDIR/bin/sbnfit_uboone_scaling_fc_eLEE --xml dllee_sens_pred_1e1p-only_{}.xml -t h1_constr -i lee -g '{}' -n {:d} -c -m ".format(tag, grid_str, Npes)

    # run Feldman-Cousins calculations
    cmd = cmd_base + "feldman > log_testC_feldman.txt"
    print cmd
    subprocess.call(cmd, shell=True)
    # construct the confidence belts
    cmd = cmd_base + "belt > log_testC_belt.txt"
    print cmd
    subprocess.call(cmd, shell=True)
    # compare to data
    cmd = cmd_base + "data -d data_1e1p-only.SBNspec.root > log_testC_data.txt"
    print cmd
    subprocess.call(cmd, shell=True)
    
os.chdir(topdir)

print "Done!"
