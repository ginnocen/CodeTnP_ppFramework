
void CompareMCData(TString id="Trg") {

  gROOT->SetStyle("Plain");
  gStyle->SetOptStat(0);
  gStyle->SetTitle(0);

  char *infile;

  if(id=="Trg"){
   infile= "Results/foutputTrigger.root";
  }
  
  if(id=="Trk"){
   infile= "Results/foutputTracking.root";
  }
  
  if(id=="MuonID"){
   infile= "Results/foutputMuonID.root";
  }
  
  
  TFile *file = new TFile(infile);

  TGraphAsymmErrors *fEff_pt_MC =(TGraphAsymmErrors*)file->Get("fEff_pt_MC");
  TGraphAsymmErrors *fEff_pt_Data =(TGraphAsymmErrors*)file->Get("fEff_pt_Data");
  TGraphAsymmErrors *fEff_eta_MC =(TGraphAsymmErrors*)file->Get("fEff_eta_MC");
  TGraphAsymmErrors *fEff_eta_Data =(TGraphAsymmErrors*)file->Get("fEff_eta_Data");



  TCanvas *canvas=new TCanvas("canvas","canvas",500,500);   
  canvas->cd();
  canvas->Range(-1.989924,-0.2917772,25.49622,2.212202);
  canvas->SetFillColor(0);
  canvas->SetBorderMode(0);
  canvas->SetBorderSize(2);
  canvas->SetLeftMargin(0.1451613);
  canvas->SetRightMargin(0.05443548);
  canvas->SetTopMargin(0.08474576);
  canvas->SetBottomMargin(0.1165254);
  canvas->SetFrameBorderMode(0);
  canvas->SetFrameBorderMode(0);

  
  TH2F* hemptyPt=new TH2F("hemptyPt","",10,0.,30,10.,0,1.1);  
  hemptyPt->GetXaxis()->SetTitle("p_{T} (GeV/c)");
  hemptyPt->GetYaxis()->SetTitle(Form("Eff %s",id.Data()));
  hemptyPt->GetXaxis()->SetTitleOffset(1.);
  hemptyPt->GetYaxis()->SetTitleOffset(1.3);
  hemptyPt->GetXaxis()->SetTitleSize(0.045);
  hemptyPt->GetYaxis()->SetTitleSize(0.045);
  hemptyPt->GetXaxis()->SetTitleFont(42);
  hemptyPt->GetYaxis()->SetTitleFont(42);
  hemptyPt->GetXaxis()->SetLabelFont(42);
  hemptyPt->GetYaxis()->SetLabelFont(42);
  hemptyPt->GetXaxis()->SetLabelSize(0.04);
  hemptyPt->GetYaxis()->SetLabelSize(0.04);  
  hemptyPt->SetMaximum(1.1);
  hemptyPt->SetMinimum(0.);
  hemptyPt->Draw();
    
  
  fEff_pt_MC->SetMarkerColor(1);
  fEff_pt_MC->SetMarkerStyle(21);  
  fEff_pt_MC->SetLineColor(1);
  fEff_pt_MC->SetLineWidth(2);
  fEff_pt_MC->Draw("epsame");
  
  fEff_pt_Data->SetMarkerColor(2);
  fEff_pt_Data->SetMarkerStyle(21);  
  fEff_pt_Data->SetLineColor(2);
  fEff_pt_Data->SetLineWidth(2);
  fEff_pt_Data->Draw("epsame");
  
  TLegend *legend=new TLegend(0.3770161,0.2881356,0.8245968,0.4194915,"");
  legend->SetBorderSize(0);
  legend->SetTextFont(42);
  legend->SetTextSize(0.04);

  TLegendEntry *ent_MC=legend->AddEntry(fEff_pt_MC,"Monte Carlo","pf");
  ent_MC->SetTextFont(42);
  ent_MC->SetLineColor(1);
  ent_MC->SetMarkerColor(1);
  
  TLegendEntry *ent_Data=legend->AddEntry(fEff_pt_Data,"Data","pf");
  ent_Data->SetTextFont(42);
  ent_Data->SetLineColor(1);
  ent_Data->SetMarkerColor(1);
  
  legend->Draw();
  canvas->SaveAs(Form("Plots/canvas%s.pdf",id.Data()));
  



}