#include <iostream>
#include <TSystem.h>
#include <TTree.h>
#include <TKey.h>
#include <TH1.h>
#include <TH2.h>
#include <TPave.h>
#include <TText.h>
#include <fstream>
#include <sstream>
#include <string.h>

#include <TROOT.h>
#include <TFile.h>
#include <TGraphAsymmErrors.h>
#include <TH1.h>
#include <TH2.h>
#include <TCanvas.h>
#include <TLegend.h>

#include <TStyle.h>
#include <TLatex.h>
#include <TDirectory.h>
#include <TCollection.h>
#include <TPostScript.h>

using namespace RooFit;
using namespace std;


void ConvertIntoRootFiles();
TH2F *plotEff2D(RooDataSet *a, TString b);
TGraphAsymmErrors *plotEffPt(RooDataSet *a, int aa);
TGraphAsymmErrors *plotEffEta(RooDataSet *a, int aa);

const int ptbins=7;
const int etabins=1;



void ConvertIntoRootFiles(TString id="Trg") {

  gROOT->SetStyle("Plain");
  gStyle->SetOptStat(0);
  gStyle->SetTitle(0);

  char *infileMC;
  char *infileData;
  char *rootstring;
  char *outfile;
  
  if(id=="Trg"){
   infileMC= "../ResultsFit/outputTriggerMC.root";
   infileData= "../ResultsFit/outputTriggerData.root";
   rootstring="tpTree/MuID_pt/fit_eff";
   outfile="Results/foutputTrigger.root";
  }
  
  if(id=="Trk"){
   infileMC= "../ResultsFit/outputTrackingMC.root";
   infileData= "../ResultsFit/outputTrackingData.root";
   rootstring="tpTreeSta/MuID_pt/fit_eff";
   outfile="Results/foutputTracking.root";
  }
  
  if(id=="MuonID"){
   infileMC= "../ResultsFit/outputMuonIDMC.root";
   infileData= "../ResultsFit/outputMuonIDData.root";
   rootstring="tpTree/MuID_pt/fit_eff";
   outfile="Results/foutputMuonID.root";
  }
  
  
  TFile *fMC = new TFile(infileMC);
  TFile *fData = new TFile(infileData);
  RooDataSet *daPtMC = (RooDataSet*)fMC->Get(rootstring);
  RooDataSet *daPtData = (RooDataSet*)fData->Get(rootstring);
  
  TGraphAsymmErrors *fEff_pt_MC = plotEffPt(daPtMC, 1);
  TGraphAsymmErrors *fEff_pt_Data = plotEffPt(daPtData, 1);
  TGraphAsymmErrors *fEff_eta_MC= plotEffEta(daPtMC, 1);
  TGraphAsymmErrors *fEff_eta_Data= plotEffEta(daPtData, 1);
   
  fEff_pt_MC->SetName("fEff_pt_MC");
  fEff_pt_Data->SetName("fEff_pt_Data");
  fEff_eta_MC->SetName("fEff_eta_MC");
  fEff_eta_Data->SetName("fEff_eta_Data");
  
  
 // for (int i=0;i<ptbins;i++){
 //  for (int j=0;j<etabins;j++){
 //   TCanvas *canvasMC = (TCanvas*)fMC->Get(Form("tpTree/MuID_pt/eta_bin%d_pt_bin%d_Acc_JPsi_GlobalCuts_pass_cbGaussPlusExpo/fit_canvas",j,i));
 //   canvasMC->SaveAs(Form("Plots/canvas_ptbin_%d_etabin_%d",i,j));
 //   }
 // 
 // }
    
  TFile*foutput=new TFile(outfile,"recreate");
  foutput->cd();
  fEff_pt_MC->Write();
  fEff_pt_Data->Write();
  fEff_eta_MC->Write();
  fEff_eta_Data->Write();
  
  
  

}


TGraphAsymmErrors *plotEffPt(RooDataSet *a, int aa){
    const RooArgSet *set = a->get();
    RooRealVar *xAx = (RooRealVar*)set->find("pt");
    RooRealVar *eff = (RooRealVar*)set->find("efficiency");

    //const int nbins = xAx->getBinning().numBins();
    const int nbins = 7;

    double tx[nbins], txhi[nbins], txlo[nbins];
    double ty[nbins], tyhi[nbins], tylo[nbins];

    for (int i=0; i<nbins; i++) {
        a->get(i);
        ty[i] = eff->getVal();
        tx[i] = xAx->getVal();
        txhi[i] = fabs(xAx->getErrorHi());
        txlo[i] = fabs(xAx->getErrorLo()); 
        tyhi[i] = fabs(eff->getErrorHi());
        tylo[i] = fabs(eff->getErrorLo()); 
    }

    cout<<"NBins : "<<nbins<<endl;

    const double *x = tx;
    const double *xhi = txhi;
    const double *xlo = txlo;
    const double *y = ty;
    const double *yhi = tyhi;
    const double *ylo = tylo;

    TGraphAsymmErrors *b = new TGraphAsymmErrors();
    if(aa == 1) {*b = TGraphAsymmErrors(nbins,x,y,xlo,xhi,ylo,yhi);}
    if(aa == 0) {*b = TGraphAsymmErrors(nbins,x,y,0,0,ylo,yhi);}
    b->SetMaximum(1.1);
    b->SetMinimum(0.0);
    b->SetMarkerStyle(20);
    b->SetMarkerColor(kRed+2);
    b->SetMarkerSize(1.0);
    b->SetTitle("");
    b->GetXaxis()->SetTitleSize(0.05);
    b->GetYaxis()->SetTitleSize(0.05);
    b->GetXaxis()->SetTitle("p_{T} [GeV/c]");
    b->GetYaxis()->SetTitle("Efficiency");
    b->GetXaxis()->CenterTitle();
    b->Draw("apz");

    for (int i=0; i<nbins; i++) {
        cout << x[i] << " " << y[i] << " " << yhi[i] << " " << ylo[i] << endl;
    }

    return b;

}


TGraphAsymmErrors *plotEffEta(RooDataSet *a, int aa){
    const RooArgSet *set = a->get();
    RooRealVar *xAx = (RooRealVar*)set->find("eta");
    RooRealVar *eff = (RooRealVar*)set->find("efficiency");

    //const int nbins = xAx->getBinning().numBins();
    const int nbins = 1;

    double tx[nbins], txhi[nbins], txlo[nbins];
    double ty[nbins], tyhi[nbins], tylo[nbins];

    for (int i=0; i<nbins; i++) {
        a->get(i);
        ty[i] = eff->getVal();
        tx[i] = xAx->getVal();
        txhi[i] = fabs(xAx->getErrorHi());
        txlo[i] = fabs(xAx->getErrorLo()); 
        tyhi[i] = fabs(eff->getErrorHi());
        tylo[i] = fabs(eff->getErrorLo()); 
    }

    cout<<"NBins : "<<nbins<<endl;

    const double *x = tx;
    const double *xhi = txhi;
    const double *xlo = txlo;
    const double *y = ty;
    const double *yhi = tyhi;
    const double *ylo = tylo;

    TGraphAsymmErrors *b = new TGraphAsymmErrors();
    if(aa == 1) {*b = TGraphAsymmErrors(nbins,x,y,xlo,xhi,ylo,yhi);}
    if(aa == 0) {*b = TGraphAsymmErrors(nbins,x,y,0,0,ylo,yhi);}
    b->SetMaximum(1.1);
    b->SetMinimum(0.0);
    b->SetMarkerStyle(20);
    b->SetMarkerColor(kRed+2);
    b->SetMarkerSize(1.0);
    b->SetTitle("");
    b->GetXaxis()->SetTitleSize(0.05);
    b->GetYaxis()->SetTitleSize(0.05);
    b->GetXaxis()->SetTitle("#eta");
    b->GetYaxis()->SetTitle("Efficiency");
    b->GetXaxis()->CenterTitle();
    b->Draw("apz");

    for (int i=0; i<nbins; i++) {
        cout << x[i] << " " << y[i] << " " << yhi[i] << " " << ylo[i] << endl;
    }

    return b;

}

TH2F *plotEff2D(RooDataSet *a, TString b){
    const RooArgSet *set = a->get();
    RooRealVar *yAx = (RooRealVar*)set->find("pt");
    RooRealVar *xAx = (RooRealVar*)set->find("eta");
    RooRealVar *eff = (RooRealVar*)set->find("efficiency");

    //const int xnbins = xAx->getBinning().numBins();
    //const int ynbins = yAx->getBinning().numBins();

    const double *xvbins = xAx->getBinning().array();
    const double *yvbins = yAx->getBinning().array();

    TH2F* h = new TH2F(b, "", xAx->getBinning().numBins(), xvbins, yAx->getBinning().numBins(), yvbins);

    gStyle->SetPaintTextFormat("5.2f");
    gStyle->SetPadRightMargin(0.12);
    gStyle->SetPalette(1);
    h->SetOption("colztexte");
    h->GetZaxis()->SetRangeUser(-0.001,1.001);
    h->SetStats(kFALSE);
    h->GetYaxis()->SetTitle("p_{T} [GeV/c]");
    h->GetXaxis()->SetTitle("#eta");
    h->GetXaxis()->CenterTitle();
    h->GetYaxis()->CenterTitle();
    h->GetXaxis()->SetTitleSize(0.05);
    h->GetYaxis()->SetTitleSize(0.05);
    h->GetYaxis()->SetTitleOffset(0.8);
    h->GetXaxis()->SetTitleOffset(0.9);
    for(int i=0; i<a->numEntries(); i++){
        a->get(i);
        h->SetBinContent(h->FindBin(xAx->getVal(), yAx->getVal()), eff->getVal());
        h->SetBinError(h->FindBin(xAx->getVal(), yAx->getVal()), (eff->getErrorHi()-eff->getErrorLo())/2.);
    }

    return h;

}
