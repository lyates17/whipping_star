#ifndef SBNCHI_H_
#define SBNCHI_H_

#include <cmath>
#include <vector>
#include <iostream>
#include <ctime>
#include <random>

#include "SBNspec.h"
#include "SBNconfig.h"

#include "TH1.h"
#include "TH2.h"
#include "TMatrixT.h"
#include "TMatrixTSym.h"
#include "TVectorT.h"
#include "TRandom3.h"
#include "TFile.h"
#include "TStyle.h"
#include "TLine.h"

#include "params.h"

#include "TDecompChol.h"
#include "TDecompSVD.h"
#include "TMatrixDEigen.h"
#include "TMatrixDSymEigen.h"
#include <Eigen/Dense>
#include <Eigen/SVD>

namespace sbn{

struct CLSresult{

    public:
    std::string m_tag;
    TH1D m_pdf;
    float m_min_value;
    float m_max_value;
    std::vector<float> m_values;
    std::vector<double> m_quantiles; 
    std::vector<double> m_nlower; 
    std::vector<float> m_pvalues; 
    
    CLSresult(){
        m_tag = "Default";
        m_min_value = 9999999;
        m_max_value = -999999;
    }
};


class SBNchi : public SBNconfig{

	public:

	//Either initilize from a SBNspec (and use its .xml file)
	SBNchi(SBNspec);
	//Either initilize from a SBNspec and another xml file
	SBNchi(SBNspec,std::string);
	//Either initilize from a SBNspec  a TMatrix you have calculated elsewhere
	SBNchi(SBNspec,TMatrixT<double>);
	SBNchi(SBNspec,TMatrixT<double>,bool);
	SBNchi(SBNspec,TMatrixT<double>,std::string, bool);
	SBNchi(SBNspec in, TMatrixT<double> matrix_systematicsin, std::string inxml, bool is_verbose, double random_seed);

    //Initialise a stat_only one;
	SBNchi(SBNspec, bool is_stat_only);
	SBNchi(std::string);
	

	//This is the core spectra that you are comparing too. This is used to calculate covariance matrix and in a way is on the 'bottom' of the chi^2.
	SBNspec core_spectrum;
	bool is_stat_only;

	//always contains the last chi^2 value calculated
	double last_calculated_chi;
	std::vector<std::vector<double>> vec_last_calculated_chi;



	TMatrixT<double> matrix_systematics;
	TMatrixT<double> m_matrix_systematics_collapsed;
	TMatrixT<double> matrix_fractional_covariance;
	TMatrixT<double> matrix_collapsed;

	//Used in cholosky decompositions
	bool cholosky_performed;
	TMatrixT<float> matrix_lower_triangular;
	std::vector<std::vector<float>> vec_matrix_lower_triangular;

	//Some reason eventually store the reuslt in vectors, I think there was memory issues.
	std::vector<std::vector<double >> vec_matrix_inverted;
	std::vector<std::vector<double >> vec_matrix_collapsed;

    /***** Random Number Generation ****/
    std::random_device random_device_seed;
    std::mt19937 *rangen_twister; //merseinne twister
    std::minstd_rand * rangen_linear;
    std::ranlux24_base * rangen_carry;
    void InitRandomNumberSeeds();
    void InitRandomNumberSeeds(double);
    TRandom3 * rangen;
    std::normal_distribution<float>* m_dist_normal;

	/*********************************** Member Functions ********************************/	




	int ReloadCoreSpectrum(SBNspec *bkgin);

	//load up systematic covariabnce matrix from a rootfile, location in xml
	//These are pretty obsolete.
	TMatrixT<double> FillSystematicsFromXML(std::string, std::string);
	TMatrixT<double> FillSystematicsFromXML();

	void FakeFillMatrix(TMatrixT <double>&  M);
	void FillStatsMatrix(TMatrixT <double>&  M, std::vector<double> diag);

	// These are the powerhouse of of the SBNchi, the ability to collapse any number of modes,detectors,channels and subchannels down to a physically observable subSet
	// layer 1 is the cheif bit, taking each detector and collapsing the subchannels
	void CollapseSubchannels(TMatrixT <double> & M, TMatrixT <double> & Mc);
	//layer 2 just loops layer_1 over all detectors in a given mode
	void CollapseDetectors(TMatrixT <double> & M, TMatrixT <double> & Mc);
	//layer 3 just loops layer_2 over all modes we have Setup
	void CollapseModes(TMatrixT <double> & M, TMatrixT <double> & Mc);

    TMatrixT<double> InvertMatrix(TMatrixT<double> &M);
    TMatrixT<double> CalcCovarianceMatrix(TMatrixT<double>*M, TVectorT<double>& spec);
    TMatrixT<double> CalcCovarianceMatrix(TMatrixT<double>*M, std::vector<double>& spec);
    TMatrixT<double> CalcCovarianceMatrixCNP(TMatrixT<double> M, std::vector<double>& spec, std::vector<double>& spec_collapse, const std::vector<double>& datavec );
    TMatrixT<double> CalcCovarianceMatrixCNP(TMatrixT<double>* M, std::vector<double>& spec, const std::vector<float>& datavec );
    




	TMatrixT<double> * GetCollapsedMatrix();
	int FillCollapsedCovarianceMatrix(TMatrixT<double>*);
	int FillCollapsedCorrelationMatrix(TMatrixT<double>*);
	int FillCollapsedFractionalMatrix(TMatrixT<double>*);

	//Return chi^2 from eith a SBnspec (RECCOMENDED as it checks to make sure xml compatable)
	//double CalcChi(SBNspec sigSpec);
	double CalcChi(SBNspec *sigSpec);
	// Or a vector
	double CalcChi(std::vector<double> );
	//Or you are taking covariance from one, and prediciton from another
	double CalcChi(SBNspec *sigSpec, SBNspec *obsSpec);
	//or a log ratio (miniboone esque)
	double CalcChiLog(SBNspec *sigSpec);

	double CalcChi(std::vector<double> * sigVec);
	float  CalcChi(std::vector<float> * sigVec);
	double CalcChi(double* sigVec);

	double CalcChi(double ** inv, double *, double *);
	float CalcChi(float ** inv, float *, float *);

    float PoissonLogLiklihood(float * h0_corein, float *collapsed);
    float CalcChi_CNP(float * pred, float* data);
	double CalcChi(TMatrixT<double> M, std::vector<double>& spec, std::vector<double>& data);
	
    std::vector<std::vector<double >> TMatrixDToVector(TMatrixT <double> McI);
	

	//Cholosky related
	int PerformCholoskyDecomposition(SBNspec *specin);

//	SBNspec SampleCovariance(SBNspec *specin); 
    std::vector<float> SampleCovariance(SBNspec *specin); 

    //

	TH1D SamplePoissonVaryCore(SBNspec *specin, int num_MC);
	TH1D SamplePoissonVaryInput(SBNspec *specin, int num_MC, double maxchi);
	TH1D SamplePoissonVaryInput(SBNspec *specin, int num_MC, std::vector<double>*);
	TH1D SampleCovarianceVaryInput(SBNspec *specin, int num_MC, double maxchi);
	TH1D SampleCovarianceVaryInput(SBNspec *specin, int num_MC, std::vector<double>*);



    std::vector<CLSresult> Mike_NP(SBNspec *specin, SBNchi &chi_h0, SBNchi & chi_h1, int num_MC, int which_sample,int id);
    TH1D SamplePoisson_NP(SBNspec *specin, SBNchi &chi_h0, SBNchi & chi_h1, int num_MC, std::vector<double> *chival,int which_sample);
    TH1D SamplePoisson_NP(SBNspec *specin, SBNchi &chi_h0, SBNchi & chi_h1, int num_MC, double,int which_sample);



    double max_sample_chi_val;

	int CollapseVectorStandAlone(std::vector<double> * full_vector, std::vector<double> *collapsed_vector);

	int CollapseVectorStandAlone(double* full_vector, double* collapsed_vector);
	int CollapseVectorStandAlone(float* full_vector, float* collapsed_vector);



    int SingleValueDecomposition(double ** matrix, double ** U, double**V, double *single_values );

    bool pseudo_from_collapsed;
    std::vector<float> GeneratePseudoExperiment();


		//some plotting things
	TH2D* GetChiogram();
	int PrintMatricies(std::string);
    int DrawSampleCovariance(std::string);

};


};
#endif
