import FWCore.ParameterSet.Config as cms

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')
process.options   = cms.untracked.PSet( wantSummary = cms.untracked.bool(True) )
process.MessageLogger.cerr.FwkReport.reportEvery = 100

process.source = cms.Source("PoolSource", 
    fileNames = cms.untracked.vstring(),
)
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )    


process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load("Configuration.StandardSequences.Reconstruction_cff")

import os
if   "CMSSW_5_3_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('START53_V27::All')  #for MC
    #process.GlobalTag.globaltag = cms.string( 'GR_P_V43F::All' ) #for data /PAMuon/HIRun2013-28Sep2013-v1/RECO
    #process.GlobalTag.globaltag = cms.string( 'GR_P_V43D::All' ) #for data /PAMuon/HIRun2013-PromptReco-v1/RECO
    
    process.source.fileNames = [
        'file:/afs/cern.ch/work/h/hckim/public/HIJINGemb_inclBtoPsiMuMu_5TeV_boost_RECO_STARTHI53_V27_evt600_1075_1_IAW.root', #for MC
        #'file:/afs/cern.ch/work/g/ginnocen/38291323-E567-E211-8DD9-5404A63886C5.root', #for data

    ]
elif "CMSSW_5_2_" in os.environ['CMSSW_VERSION']:
    process.GlobalTag.globaltag = cms.string('GR_P_V39_AN1::All')
    process.source.fileNames = [
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/645E9BE9-FC87-E111-9D30-5404A63886C5.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/60C36C17-0188-E111-8B3D-5404A638868F.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/5E384785-F087-E111-A8CB-BCAEC518FF80.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/5C605E9F-F887-E111-A540-00237DDC5CB0.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/5C0DCA92-CE87-E111-A539-5404A63886C6.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/5A856F46-1888-E111-A3A5-BCAEC5329700.root',
        '/store/data/Run2012A/MuOnia/AOD/PromptReco-v1/000/191/226/5271187F-DF87-E111-ADDB-BCAEC518FF7C.root',
    ]
else: raise RuntimeError, "Unknown CMSSW version %s" % os.environ['CMSSW_VERSION']


# Common offline event selection
process.load("HeavyIonsAnalysis.Configuration.collisionEventSelection_cff")

process.load("HLTrigger.HLTfilters.triggerResultsFilter_cfi")
process.triggerResultsFilter.triggerConditions = cms.vstring( 'HLT_PAMu3_v*' )
process.triggerResultsFilter.l1tResults = ''
process.triggerResultsFilter.throw = True
process.triggerResultsFilter.hltResults = cms.InputTag( "TriggerResults", "", "HLT" )
process.HLTMu   = process.triggerResultsFilter.clone(triggerConditions = [ 'HLT_PAMu3_v*' ])

## ==== Merge CaloMuons and Tracks into the collection of reco::Muons  ====
from RecoMuon.MuonIdentification.calomuons_cfi import calomuons;
process.mergedMuons = cms.EDProducer("CaloMuonMerger",
    mergeTracks = cms.bool(True),
    mergeCaloMuons = cms.bool(False), # AOD
    muons     = cms.InputTag("muons"), 
    caloMuons = cms.InputTag("calomuons"),
    tracks    = cms.InputTag("generalTracks"),
    minCaloCompatibility = calomuons.minCaloCompatibility,
    ## Apply some minimal pt cut
    muonsCut     = cms.string("track.isNonnull && pt > 1.5"),
    caloMuonsCut = cms.string("pt > 1.5"),
    tracksCut    = cms.string("pt > 1.5"),
)

## ==== Trigger matching
process.load("MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff")
## with some customization
from MuonAnalysis.MuonAssociators.patMuonsWithTrigger_cff import *
changeRecoMuonInput(process, "mergedMuons")
useExtendedL1Match(process)
addHLTL1Passthrough(process)
changeTriggerProcessName(process, "*")

IN_ACCEPTANCE = "((abs(eta) <= 1.3 && pt > 3.3) || (1.3 < abs(eta) <= 2.2 && p > 2.9) || (2.2 < abs(eta) <= 2.4 && pt > 0.8))"
TRACK_CUTS = "(isTrackerMuon) && (track.hitPattern.trackerLayersWithMeasurement > 5 && track.normalizedChi2 < 1.8 && track.hitPattern.pixelLayersWithMeasurement > 0 && abs(dB) < 3 && abs(track.dz) < 30)"
MUONID = "(muonID('TrackerMuonArbitrated') && muonID('TMOneStationTight'))"

from MuonAnalysis.TagAndProbe.common_variables_cff import *
process.load("MuonAnalysis.TagAndProbe.common_modules_cff")

process.tagMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string(TRACK_CUTS+ "&&"+ IN_ACCEPTANCE +"&&"+ MUONID+ "&& (!triggerObjectMatchesByPath('HLT_PAMu3_v*',1,0).empty())"),
)

process.oneTag  = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tagMuons"), minNumber = cms.uint32(1))

process.probeMuons = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTrigger"),
    cut = cms.string("track.isNonnull")
)

process.tpPairs = cms.EDProducer("CandViewShallowCloneCombiner",
    cut = cms.string('2.8 < mass < 3.4 && abs(daughter(0).vz - daughter(1).vz) < 1'),
    decay = cms.string('tagMuons@+ probeMuons@-')
)
process.onePair = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairs"), minNumber = cms.uint32(1))

#process.tagMuonsMCMatch = cms.EDProducer("MCTruthDeltaRMatcherNew",
#    src = cms.InputTag("tagMuons"),
#    matched = cms.InputTag("genParticles"),
#    pdgId = cms.vint32(13),
#    distMin = cms.double(0.3),
#)
#process.probeMuonsMCMatch = process.tagMuonsMCMatch.clone(src = "probeMuons")

from MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cff import ExtraIsolationVariables

process.tpTree = cms.EDAnalyzer("TagProbeFitTreeProducer",
    # choice of tag and probe pairs, and arbitration
    tagProbePairs = cms.InputTag("tpPairs"),
    arbitration   = cms.string("None"),
    # probe variables: all useful ones
    variables = cms.PSet(
        KinematicVariables,
        IsolationVariables,
	    MuonIDVariables,
	    TrackQualityVariables,
	    GlobalTrackQualityVariables,
	    TriggerVariables,
	    dxyBS = cms.InputTag("muonDxyPVdzmin","dxyBS"),
        dxyPVdzmin = cms.InputTag("muonDxyPVdzmin","dxyPVdzmin"),
        dzPV = cms.InputTag("muonDxyPVdzmin","dzPV"),
        nSplitTk  = cms.InputTag("splitTrackTagger"),

    ),
    flags = cms.PSet(
       TrackQualityFlags,
       HFHIPhysicsFlagsTrigger,
       MuonIDFlags,
       Acc_JPsi = cms.string(IN_ACCEPTANCE),
       TrackCuts	= cms.string(TRACK_CUTS),
       MuonID	= cms.string(MUONID),
    ),
    tagVariables = cms.PSet(
        pt  = cms.string('pt'),
        eta = cms.string('eta'),
        phi = cms.string('phi'),
        nVertices = cms.InputTag("nverticesModule"),
        l1rate = cms.InputTag("l1rate"),
        bx     = cms.InputTag("l1rate","bx"),
    ),
    tagFlags     = cms.PSet(
        HFHIPhysicsFlagsTrigger,
    ),
    pairVariables = cms.PSet(
        pt = cms.string("pt"),
        dphiVtxTimesQ = cms.InputTag("tagProbeSeparation", "dphiVtxTimesQ"),
        drM1          = cms.InputTag("tagProbeSeparation", "drM1"),
        dphiM1        = cms.InputTag("tagProbeSeparation", "dphiM1"),
        distM1        = cms.InputTag("tagProbeSeparation", "distM1"),
        drM2          = cms.InputTag("tagProbeSeparation", "drM2"),
        dphiM2        = cms.InputTag("tagProbeSeparation", "dphiM2"),
        distM2        = cms.InputTag("tagProbeSeparation", "distM2"),
        drVtx         = cms.InputTag("tagProbeSeparation", "drVtx"),
        dz            = cms.string("daughter(0).vz - daughter(1).vz"),
        probeMultiplicity = cms.InputTag("probeMultiplicity"),
    ),
    pairFlags = cms.PSet(),
    isMC           = cms.bool(False),
    #tagMatches       = cms.InputTag("tagMuonsMCMatch"),
    #probeMatches     = cms.InputTag("probeMuonsMCMatch"),
    #motherPdgId      = cms.vint32(443),
    #makeMCUnbiasTree       = cms.bool(False),
    checkMotherInUnbiasEff = cms.bool(True),
    allProbes              = cms.InputTag("probeMuons"),
)

process.load("MuonAnalysis.TagAndProbe.muon.tag_probe_muon_extraIso_cfi")

process.tnpSimpleSequence = cms.Sequence(
    #process.tagMuons   * process.tagMuonsMCMatch   +
    process.tagMuons    +
    process.oneTag     +
    #process.probeMuons * process.probeMuonsMCMatch +
    process.probeMuons +
    process.tpPairs    +
    process.onePair    +
    process.muonDxyPVdzmin +
    process.nverticesModule +
    process.tagProbeSeparation +
    process.computeCorrectedIso + 
    process.probeMultiplicity + 
    process.splitTrackTagger +
    process.l1rate +
    process.tpTree
)

process.tagAndProbe = cms.Path( 
    process.PAcollisionEventSelection *
    process.HLTMu    +
    process.mergedMuons                 *
    process.patMuonsWithTriggerSequence *
    process.tnpSimpleSequence
)

##    _____               _    _             
##   |_   _| __ __ _  ___| | _(_)_ __   __ _ 
##     | || '__/ _` |/ __| |/ / | '_ \ / _` |
##     | || | | (_| | (__|   <| | | | | (_| |
##     |_||_|  \__,_|\___|_|\_\_|_| |_|\__, |
##                                     |___/ 

## Then make another collection for standalone muons, using standalone track to define the 4-momentum
process.muonsSta = cms.EDProducer("RedefineMuonP4FromTrack",
    src   = cms.InputTag("muons"),     #IT WAS "muons TO BE CHECKED WITH MUON POG"
    track = cms.string("outer"),
)

## Match to trigger, to measure the efficiency of HLT tracking
from PhysicsTools.PatAlgos.tools.helpers import *
process.patMuonsWithTriggerSequenceSta = cloneProcessingSnippet(process, process.patMuonsWithTriggerSequence, "Sta")
process.muonMatchHLTL2Sta.maxDeltaR = 0.5
process.muonMatchHLTL3Sta.maxDeltaR = 0.5
massSearchReplaceAnyInputTag(process.patMuonsWithTriggerSequenceSta, "mergedMuons", "muonsSta")

## Define probes and T&P pairs
process.probeMuonsSta = cms.EDFilter("PATMuonSelector",
    src = cms.InputTag("patMuonsWithTriggerSta"),
    cut = cms.string("outerTrack.isNonnull"), 
)

#process.probeMuonsMCMatchSta = process.tagMuonsMCMatch.clone(src = "probeMuonsSta")
process.tpPairsSta = process.tpPairs.clone(decay = "tagMuons@+ probeMuonsSta@-", cut = "2 < mass < 5")

process.onePairSta = cms.EDFilter("CandViewCountFilter", src = cms.InputTag("tpPairsSta"), minNumber = cms.uint32(1))

process.tpTreeSta = process.tpTree.clone(
    tagProbePairs = "tpPairsSta",
    variables = cms.PSet(
        KinematicVariables, 
        StaOnlyVariables,
        ## track matching variables
        tk_deltaR     = cms.InputTag("staToTkMatch","deltaR"),
        tk_deltaEta   = cms.InputTag("staToTkMatch","deltaEta"),
        tk_deltaR_NoJPsi     = cms.InputTag("staToTkMatchNoJPsi","deltaR"),
        tk_deltaEta_NoJPsi   = cms.InputTag("staToTkMatchNoJPsi","deltaEta"),
        tk_deltaR_NoBestJPsi     = cms.InputTag("staToTkMatchNoBestJPsi","deltaR"),
        tk_deltaEta_NoBestJPsi   = cms.InputTag("staToTkMatchNoBestJPsi","deltaEta"),
    ),
    flags = cms.PSet(
        MuonIDFlags,
        outerValidHits = cms.string("outerTrack.numberOfValidHits > 0"),
        Acc_JPsi = cms.string(IN_ACCEPTANCE),
        TrackCuts	= cms.string(TRACK_CUTS),
        l2muonobject = cms.string("!triggerObjectMatchesByCollection('hltL2MuonCandidates').empty()"),
    ),
    tagVariables = cms.PSet(
        nVertices = cms.InputTag("nverticesModule"),
    ),
    tagFlags = cms.PSet(

    ),
    pairVariables = cms.PSet(),
    pairFlags     = cms.PSet(),
    allProbes     = "probeMuonsSta",
    #probeMatches  = "probeMuonsMCMatchSta",
)


process.tnpSimpleSequenceSta = cms.Sequence(
    #process.tagMuons   * process.tagMuonsMCMatch   +
    process.tagMuons   +
    process.oneTag     +
    #process.probeMuonsSta * process.probeMuonsMCMatchSta +
    process.probeMuonsSta +
    process.tpPairsSta      +
    process.onePairSta      +
    process.nverticesModule +
    process.staToTkMatchSequenceJPsi +
    process.l1rate +
    process.tpTreeSta
)


process.tagAndProbeSta = cms.Path( 
    process.PAcollisionEventSelection *
    process.HLTMu      +
    process.muonsSta                       +
    process.patMuonsWithTriggerSequenceSta +
    process.tnpSimpleSequenceSta
)

process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJPsi_MC.root"))
#process.TFileService = cms.Service("TFileService", fileName = cms.string("tnpJPsi_Data.root")) #for data
