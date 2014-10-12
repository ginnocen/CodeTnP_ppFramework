void CompareMethods(TString id="Trg", TString idpt="Pt", TString data="MC") {

   gROOT->SetStyle("Plain");	
   gStyle->SetOptStat(0);
   gStyle->SetOptStat(0000);
   gStyle->SetPalette(0);
   gStyle->SetCanvasColor(0);
   gStyle->SetFrameFillColor(0);
   gStyle->SetOptTitle(0);

  TString infile;
  TString infileBfinder;
  TString infileKisoo;
  TString graphnameBfinder;
  TString graphnameKisoo;
  TString namePPcode;
  TString nameBfinder;

    
  if(id=="Trg"){   
    infile= "Results/foutputTrigger.root";
    if(idpt=="Pt"){
      nameBfinder="EffTrig";
      if(data=="MC"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputMC.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_MC_MuTrgNew2CS_CBGpExp_All_Eff_20140927.root";
        namePPcode="fEff_pt_MC";
        graphnameKisoo="Trg_pt_All"; 
      }
      if(data=="Data"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputData.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_RD_MuTrgNew2CS_CBGpExp_1st_Run_Eff_20140927.root";
        namePPcode="fEff_pt_Data";
        graphnameKisoo="Trg_pt_All";
      }
    }
  }
  
  
  if(id=="Trk"){   
    infile= "Results/foutputTracking.root";
    if(idpt=="Pt"){
      graphnameKisoo="Trk_pt_All"; 
      if(data=="MC"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputMC.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_MC_MuTrk2_2GpP4_p1_Eff_20140927.root";
        namePPcode="fEff_pt_MC";
        nameBfinder="EffTrk";
      }
      if(data=="Data"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputData.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_RD_MuTrk2_CBpPoly_1st_Run_Eff_for_B_20140927.root";
        namePPcode="fEff_pt_Data";
        nameBfinder="EffTrk";
      }
    }
  }
  
  if(id=="MuID"){   
    infile= "Results/foutputMuonID.root";
    if(idpt=="Pt"){
      graphnameKisoo="MuId_pt_All"; 
      if(data=="MC"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputMC.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_MC_MuIdNew2CS_CBpPoly_Eff_20140927.root";
        namePPcode="fEff_pt_MC";
        nameBfinder="EffMuId";
      }
      if(data=="Data"){
        infileBfinder= "InputOtherMethod/Bfinder/foutputData.root";
        infileKisoo= "InputOtherMethod/Kisoo/Jpsi_pPb_RD_MuIdNew2CS_CBpPoly_1st_Run_Eff_20140927.root";
        namePPcode="fEff_pt_Data";
        nameBfinder="EffMuId";
      }
    }
  }

  TFile *file = new TFile(infile);
  TFile *fileBfinder = new TFile(infileBfinder);
  TFile *fileKisoo = new TFile(infileKisoo);

  TGraphAsymmErrors *fEff_PPCode =(TGraphAsymmErrors*)file->Get(namePPcode.Data());
  TGraphAsymmErrors *fEff_Kisoo =(TGraphAsymmErrors*)fileKisoo->Get(graphnameKisoo.Data());
  TH1F *hEff_Bfinder=(TH1F*)fileBfinder->Get(nameBfinder.Data());

  TCanvas *canvas=new TCanvas("canvas","canvas",500,400);   
  canvas->Divide(2,1);
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

  
  TH2F* hempty=new TH2F("hempty","",10,0.,30,10.,0,1.1);  
  hempty->GetXaxis()->SetTitle("p_{T} (GeV/c)");
  hempty->GetYaxis()->SetTitle(Form("Eff %s",id.Data()));
  hempty->GetXaxis()->SetTitleOffset(1.);
  hempty->GetYaxis()->SetTitleOffset(1.3);
  hempty->GetXaxis()->SetTitleSize(0.045);
  hempty->GetYaxis()->SetTitleSize(0.045);
  hempty->GetXaxis()->SetTitleFont(42);
  hempty->GetYaxis()->SetTitleFont(42);
  hempty->GetXaxis()->SetLabelFont(42);
  hempty->GetYaxis()->SetLabelFont(42);
  hempty->GetXaxis()->SetLabelSize(0.04);
  hempty->GetYaxis()->SetLabelSize(0.04);  
  hempty->SetMaximum(1.1);
  hempty->SetMinimum(0.);
  hempty->Draw();
  
  
  fEff_PPCode->SetMarkerColor(1);
  fEff_PPCode->SetMarkerStyle(21);  
  fEff_PPCode->SetLineColor(1);
  fEff_PPCode->SetLineWidth(2);
  fEff_PPCode->Draw("epsame");
  
  fEff_Kisoo->SetMarkerColor(2);
  fEff_Kisoo->SetMarkerStyle(21);  
  fEff_Kisoo->SetLineColor(2);
  fEff_Kisoo->SetLineWidth(2);
  fEff_Kisoo->Draw("epsame");

  hEff_Bfinder->SetLineColor(4);
  hEff_Bfinder->SetMarkerColor(4);
  hEff_Bfinder->SetLineWidth(2);
  hEff_Bfinder->Draw("same");
  
  TLegend *legend=new TLegend(0.3770161,0.2881356,0.8245968,0.4194915,"");
  legend->SetBorderSize(0);
  legend->SetFillStyle(0);
  legend->SetBorderSize(0);
  legend->SetTextFont(42);
  legend->SetTextSize(0.035);

  TLegendEntry *ent_ppcode=legend->AddEntry(fEff_PPCode,"pp code","pf");
  ent_ppcode->SetTextFont(42);
  ent_ppcode->SetLineColor(1);
  ent_ppcode->SetMarkerColor(1);
  
  TLegendEntry *ent_Kisoo=legend->AddEntry(fEff_Kisoo,"Kisoo","pf");
  ent_Kisoo->SetTextFont(42);
  ent_Kisoo->SetLineColor(2);
  ent_Kisoo->SetMarkerColor(2);
  
  TLegendEntry *ent_Bfinder=legend->AddEntry(hEff_Bfinder,"Bfinder","pf");
  ent_Bfinder->SetTextFont(42);
  ent_Bfinder->SetLineColor(4);
  ent_Bfinder->SetMarkerColor(4);

  legend->Draw();
  canvas->SaveAs(Form("Plots/canvasComparison_%s_%s_%s.pdf",id.Data(),idpt.Data(),data.Data()));
  



}