import subprocess
from ROOT import TFile
import math

outdir = "output"
subprocess.call("mkdir -p %s" % outdir, shell=True)

var_list = ['Enu_1e1p','Eta','PT_1e1p','AlphaT_1e1p',
            'SphB_1e1p','PzEnu_1e1p','ChargeNearTrunk',
            'Q0_1e1p','Q3_1e1p','Thetas','Phis','PTRat_1e1p',
            'Proton_ThetaReco','Proton_PhiReco',
            'MinShrFrac','MaxShrFrac',
            'BjXB_1e1p','BjYB_1e1p','Proton_Edep',
            'Electron_Edep','Lepton_ThetaReco','Lepton_PhiReco',
            'OpenAng','Xreco','Yreco','Zreco',
            'BDTscore_1e1p','MuonPID_int',
            'ProtonPID_int','EminusPID_int',
            'shower_charge_ratio','Shower_Consistency']
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
            'BDTscore_1e1p': 'bdt_score',
            'MuonPID_int': 'mpid_muon_score',
            'ProtonPID_int': 'mpid_proton_score',
            'EminusPID_int': 'mpid_electron_score',
            'shower_charge_ratio': 'shr_charge_ratio_reco',
            'Shower_Consistency': 'shr_consistency_reco'
}


for sel in ["lowBDT"]:
    for var in var_list:
        
        # Get reweightable covariance matrix
        tag = "%s__%s" % (sel, var_dict[var])
        input_file = "auto/%s.SBNcovar.root" % tag
        input_f = TFile(input_file, "READ")
        covar = input_f.Get("collapsed_frac_covariance")

        # Write everything out...
        #outtag = "%s__%s" % (sel, var)
        outtag = "rewgt__%s" % var
        
        with open("%s/frac_covar_%s.txt" % (outdir, outtag), "w") as out:
            for i in range(covar.GetNrows()):
                for j in range(covar.GetNcols()):
                    out.write( str(covar[i][j]) )
                    if j != range(covar.GetNcols())[-1]: out.write(' ')
                out.write('\n')
        
        #with open("%s/frac_errors_%s.txt" % (outdir, outtag), "w") as out:
        #    for i in range(covar.GetNrows()):
        #        out.write( str(math.sqrt(covar[i][i])) )
        #        if i != range(covar.GetNcols())[-1]: out.write(' ')
        #    out.write('\n')

print "Done!"
