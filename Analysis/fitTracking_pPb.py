import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.source = cms.Source("EmptySource")
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.TnP_Tracking = cms.EDAnalyzer("TagProbeFitTreeAnalyzer", 
    ## Input, output 
    #InputFileNames = cms.vstring("file:../Inputs/TnPNtuple_pPb_MC_11October_v0.root"), 
    #OutputFileName = cms.string("../ResultsFit/outputTrackingMC.root"),
    InputFileNames = cms.vstring("file:../Inputs/TnPNtuple_pPb_Data_FirstRuns_11October_v0.root"), 
    OutputFileName = cms.string("../ResultsFit/outputTrackingData.root"),
    InputTreeName = cms.string("fitter_tree"),
    InputDirectoryName = cms.string("tpTreeSta"),
    ## Variables for binning
    Variables = cms.PSet(
        mass   = cms.vstring("Tag-Probe Mass", "2.", "5.", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        eta    = cms.vstring("Probe #eta", "-2.5", "2.5", ""),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
    ),
    ## Flags you want to use to define numerator and possibly denominator
    Categories = cms.PSet(
	TM = cms.vstring("Tracker muon", "dummy[pass=1,fail=0]"),
	TrackCutsSta = cms.vstring("Track cuts", "dummy[pass=1,fail=0]"),
	Acc_JPsi= cms.vstring("Acc_JPsi", "dummy[pass=1,fail=0]"),	
    ),
    ## What to fit
    Efficiencies = cms.PSet(
        Trk_pt = cms.PSet(
            UnbinnedVariables = cms.vstring("mass"),
            EfficiencyCategoryAndState = cms.vstring("TM","pass","TrackCutsSta","pass"), ## Numerator definition
            BinnedVariables = cms.PSet(
                ## Binning in continuous variables
                eta = cms.vdouble(-2.4, 2.4),
                pt = cms.vdouble(1.5,3.,4.5,6.,9.,20.,30),
                ## flags and conditions required at the denominator, 
                Acc_JPsi = cms.vstring("pass"),
            ),
            BinToPDFmap = cms.vstring("twoGaussPlusPoly1"), ## PDF to use, as defined below
        ),
    ),

    ## PDF for signal and background (double voigtian + exponential background)
    PDFs = cms.PSet(

	    gaussPlusCubic = cms.vstring(
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.15,0.05,0.25])",
            "Chebychev::backgroundPass(mass, {c1p[0,-1,1], c2p[0,-1,1], c3p[0,-1,1]})",
            "Chebychev::backgroundFail(mass, {c1f[0,-1,1], c2f[0,-1,1], c3f[0,-1,1]})",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.5]"
        ),
        gaussPlusFloatCubic = cms.vstring(
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.15,0.05,0.40])",
            "Chebychev::backgroundPass(mass, {c1p[0,-1,1], c2p[0,-1,1], c3p[0,-1,1]})",
            "Chebychev::backgroundFail(mass, {c1f[0,-1,1], c2f[0,-1,1], c3f[0,-1,1]})",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.5]"
        ),
        gaussPlusExpo = cms.vstring(
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.15,0.01,0.40])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.0,1]",
            "signalFractionInPassing[0.4,1]"
        ),
        BWResCBExp = cms.vstring(
		    "BreitWigner::bw(mass, m0[91.2,81.2,101.2], width[2.495,1,10])",
		    "RooCBShape::res(mass, peak[0], sigma[1.7,0.01,10], alpha[1.8,0,3], n[0.8,0,10])",
		    "FCONV::signal(mass, bw, res)",
		    "Exponential::backgroundPass(mass, lp[0,-5,5])",
		    "Exponential::backgroundFail(mass, lf[0,-5,5])",
		    "efficiency[0.9,0.2,1]",
		    "signalFractionInPassing[0.9]",
        ),
        
       cbGaussPlusExpo = cms.vstring(
        "CBShape::signal1(mass, mean[3.1,3.0,3.2], sigma1[0.01,0.01,0.1], alpha[0.5, 0.2, 3.0], n[2, 0.5, 100.])",
		"Gaussian::signal2(mass, mean[3.1, 3.0, 3.2], sigma2[0.04,0.01,0.1])",
		"SUM::signal(signal1,vFrac[0.8,0,1]*signal2)",
        "Exponential::backgroundPass(mass, lp[0,-5,5])",
        "Exponential::backgroundFail(mass, lf[0,-5,5])",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),
       twoGaussPlusPoly4 = cms.vstring(
        "Gaussian::signal1(mass, mean[3.1,3.0,3.2], sigma[0.10,0.05,0.250])",
        "Gaussian::signal2(mass, mean2[3.15,3.0,3.3], sigma2[0.10,0.05,0.250])",
        "SUM::signal(vfrac[0.5,0.01,1.0]*signal1,signal2)",
        "Chebychev::backgroundPass(mass,{cP1[-0.5,-1.0,1.0],cP2[-0.1,-1.0,1.0],cP3[0.2,-1.0,1.0],cP4[-0.05,-1.0,1.0]})",
        "Chebychev::backgroundFail(mass,{cF1[-0.5,-1.0,1.0],cF2[-0.1,-1.0,1.0],cF3[0.2,-1.0,1.0],cF4[-0.05,-1.0,1.0]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),
      twoGaussPlusPoly1 = cms.vstring(
        "Gaussian::signal1(mass, mean[3.1,3.0,3.2], sigma[0.10,0.05,0.400])",
        "Gaussian::signal2(mass, mean2[3.15,3.0,3.3], sigma2[0.10,0.05,0.400])",
        "SUM::signal(vfrac[0.5,0.01,1.0]*signal1,signal2)",
        "Chebychev::backgroundPass(mass,{cP1[-0.5,-1.0,1.0],cP2[-0.1,-1.0,1.0]})",
        "Chebychev::backgroundFail(mass,{cF1[-0.5,-1.0,1.0],cF2[-0.1,-1.0,1.0]})",
        "efficiency[0.9,0,1]",
        "signalFractionInPassing[0.9]"
      ),


    ),


    ## How to do the fit
    binnedFit = cms.bool(True),
    binsForFit = cms.uint32(100),
    saveDistributionsPlot = cms.bool(True),
    NumCPU = cms.uint32(1), ## leave to 1 for now, RooFit gives funny results otherwise
    SaveWorkspace = cms.bool(True),
)

process.p = cms.Path(process.TnP_Tracking)
