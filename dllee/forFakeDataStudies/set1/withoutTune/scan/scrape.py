import subprocess,os

topdir = os.getcwd()
autodir = os.path.join(topdir,"auto")
outdir = os.path.join(topdir,"output")
subprocess.call("mkdir -p %s" % outdir, shell=True)

#scale_list = [0, 1, 3, 5, 6]
scale_list = [ 0.05*i for i in range(121) ]

output = os.path.join(outdir,"output.txt")
with open(output, "w") as out:
    for scale in scale_list:

        tag = "{:03d}".format(int(scale*100))
        sens_file = os.path.join(autodir,tag,"log.txt")
        data_file = os.path.join(autodir,tag,"log_fakedata.txt")
    
        ctr = 0
        with open(sens_file, "r") as sens_in:
            for l in sens_in:
                if "Quantile" not in l: continue
                if "0.97725" in l:
                    ctr += 1
                # Pull out Delta chi2 CNP, which is third
                if ctr == 3:
                    x = float(l.split()[-3])
                    if "0.97725" in l: minus2sig = x
                    if "0.84135" in l: minus1sig = x
                    if "0.5" in l: median = x
                    if "0.15865" in l: plus1sig = x
                    if "0.02275" in l: plus2sig = x
        
        with open(data_file, "r") as data_in:
            data = float(data_in.readlines()[-1].strip().split()[-1])
        
        out.write( "{:0.2f},".format(float(scale)) + "%s,%s,%s,%s,%s,%s\n" % ( minus2sig, minus1sig, median, plus1sig, plus2sig, data ) )

print "Done!"
