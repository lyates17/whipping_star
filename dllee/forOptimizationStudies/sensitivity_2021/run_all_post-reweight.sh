#! /bin/bash

# Save a copy of the environment (for debugging)
env > env.txt

# This script runs the full sensitivity scan chain, up to scraping
for script in run_all_total-covar.py run_all_constraint.py run_all_freq.py
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
