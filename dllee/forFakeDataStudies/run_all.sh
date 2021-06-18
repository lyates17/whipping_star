#! /bin/bash

# Save a copy of the environment (for debugging)
env > env.txt

# This script runs the full sensitivity scan chain, up to scraping
# sticking with run_all_total-covar_v2.py over run_all_total-covar.py for now
for script in run_all_spec.py run_all_total-covar_v2.py run_all_constraint.py run_all_testAandB.py run_all_testC.py
do
  log=`basename $script .py`.log
  cmd="python $script"
  echo $cmd
  $cmd > $log
  stat=$?
  echo "Script finished with status $stat"
  #if [ $stat -ne 0 ]; then
  #  exit $stat
  #fi
done

# Done (success)
echo "Done!"
