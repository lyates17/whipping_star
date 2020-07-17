import subprocess
from ROOT import TFile
import math

outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = ['Enu_1e1p','Eta','PT_1e1p','AlphaT_1e1p','SphB_1e1p','PzEnu_1e1p','ChargeNearTrunk','Q0_1e1p','Q3_1e1p','Thetas','Phis',
            'PTRat_1e1p','Proton_ThetaReco','Proton_PhiReco','MinShrFrac','MaxShrFrac','BjXB_1e1p','BjYB_1e1p',
            'Proton_Edep','Electron_Edep','Lepton_ThetaReco','Lepton_PhiReco','OpenAng','Xreco','Yreco','Zreco','BDTscore_1e1p']
            #'MuonPID_int_v[2]','ProtonPID_int_v[2]','EminusPID_int_v[2]']  # not doing MPID yet
var_dict = {'Enu_1e1p': 'nu_energy_reco',
            'Eta': 'eta_reco',
            'PT_1e1p': 'pT_reco',
            'AlphaT_1e1p': 'alphaT_reco',
            'SphB_1e1p': 'sphB_reco',
            'PzEnu_1e1p': 'pzEnu_reco',
            'ChargeNearTrunk': 'charge_near_trunk_reco',
            'Q0_1e1p': 'Q0_reco',
            'Q3_1e1p': 'Q3_reco',
            'Thetas': 'sum_thetas_reco',
            'Phis': 'sum_phis_reco',
            'PTRat_1e1p': 'pT_ratio_reco',
            'Proton_ThetaReco': 'proton_theta_reco',
            'Proton_PhiReco': 'proton_phi_reco',
            'MinShrFrac': 'min_shr_frac_reco',
            'MaxShrFrac': 'max_shr_frac_reco',
            'BjXB_1e1p': 'BjxB_reco',
            'BjYB_1e1p': 'BjyB_reco',
            'Proton_Edep': 'proton_KE_reco',
            'Electron_Edep': 'lepton_KE_reco',
            'Lepton_ThetaReco': 'lepton_theta_reco',
            'Lepton_PhiReco': 'lepton_phi_reco',
            'OpenAng': 'openang_reco',
            'Xreco': 'x_reco',
            'Yreco': 'y_reco',
            'Zreco': 'z_reco',
            'BDTscore_1e1p': 'bdt_score' }
            #'MuonPID_int_v[2]','ProtonPID_int_v[2]','EminusPID_int_v[2]'  # not doing MPID yet


for sel in ["final", "highE"]:
    for var in var_list:
        
        # Get reweightable covariance matrix
        tag = "%s__%s" % (sel, var_dict[var])
        rewgt_input_file = "auto/%s.SBNcovar.root" % tag
        rewgt_input_f = TFile(rewgt_input_file, "READ")
        rewght_covar = rewgt_input_f.Get("collapsed_frac_covariance")

        # Get detsys covariance matrix
        # ... flat is the only thing that works for now...
        detsys_input_file = "detsys/flat/frac_covar_detsys__%s.txt" % var
        detsys_covar = []
        with open(detsys_input_file, "r") as detsys:
            for l in detsys:
                l = l.strip()
                row = l.split()
                for i in range(len(row)):
                    x = float(row[i])
                    #if ( math.isinf(x) or math.isnan(x) ): x = 1.
                    row[i] = x
                detsys_covar.append(row)
        #print detsys_covar

        # Add them together
        covar = rewght_covar
        for i in range(covar.GetNrows()):
            for j in range(covar.GetNcols()):
                covar[i][j] += detsys_covar[i][j]

        # Write everything out...
        outtag = "%s__%s" % (sel, var)
        
        with open("%s/frac_covar_%s.txt" % (outdir, outtag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(' ')
                out.write('\n')
        
        with open("%s/frac_errors_%s.txt" % (outdir, outtag), "w") as out:
            for i in range(covar.GetNrows()):
                out.write( str(math.sqrt(covar[i][i])) )
                if i != range(covar.GetNcols())[-1]: out.write(' ')
            out.write('\n')

print "Done!"
