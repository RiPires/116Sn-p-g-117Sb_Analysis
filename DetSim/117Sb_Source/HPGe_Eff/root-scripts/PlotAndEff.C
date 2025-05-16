#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
#include "TF1.h"
using namespace std;

void PlotAndEff(const char* filename){

    // Energy conversion factor
    double slope = 0.0003225; // MeV/ch
    double intercept = -0.000149; // MeV
    int nrCh = 4096; 

     // Open the ROOT file
     TFile *InputTFile = new TFile(filename, "READ");
     // Check if the file is open successfully
     if (!InputTFile || InputTFile->IsZombie()){
          cout << "Error: Could not open ROOT file." << endl;
          return;} 
    
     /////////////////////////////////////////////////
     // Access the Energy Scoring tree in the file  //
     /////////////////////////////////////////////////
     TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring");
     ////////////////////////////////////////////////////
     // Create a canvas for plotting deposited energy  //
     ////////////////////////////////////////////////////
     //TCanvas* canvas = new TCanvas("canvas", "Energy Scoring", 800, 600);
     // Create a histogram
     TH1D* hist1 = new TH1D("hist", "Ge energy scoring", nrCh, intercept, nrCh*slope);
     // Project the variable into the histogram
     ScoringTTRee->Project("hist", "Scoring.Edep");
     // Set the histogram style and labels
     hist1->SetLineColor(kBlue);
     hist1->SetLineWidth(2);
     hist1->GetXaxis()->SetTitle("Energy (MeV)");
     hist1->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     //hist1->Draw();
     // Display the canvas
     //canvas->SetLogy();
     //canvas->Draw();
     //gPad->Update();

     // ROIs for each photopeak area calculation
        // gamma 158 keV
        int binMinGamma = hist1->FindBin(0.15853);
        int binMaxGamma = hist1->FindBin(0.15887);
        // Ka
        int binMinKa = hist1->FindBin(0.0247);
        int binMaxKa = hist1->FindBin(0.02546);
        // Kb
        int binMinKb = hist1->FindBin(0.02833);
        int binMaxKb = hist1->FindBin(0.0293);
        // gamma 511 keV
        int binMin511 = hist1->FindBin(0.5108);
        int binMax511 = hist1->FindBin(0.511); 
        // gamma 861 keV
        int binMin861 = hist1->FindBin(0.86108);
        int binMax861 = hist1->FindBin(0.86142);
        // gamma 1004 keV
        int binMin1004 = hist1->FindBin(1.00448);
        int binMax1004 = hist1->FindBin(1.00484);

    // Calculate the area under each photopeak
        double area_Gamma = hist1->Integral(binMinGamma, binMaxGamma);
        double area_Ka = hist1->Integral(binMinKa, binMaxKa);
        double area_Kb = hist1->Integral(binMinKb, binMaxKb);
        double area511 = hist1->Integral(binMin511, binMax511);
        double area861 = hist1->Integral(binMin861, binMax861);
        double area1004 = hist1->Integral(binMin1004, binMax1004);

    // Calculate the detetcor efficiency for each peak energy
        double eff_Gamma, eff_Ka, eff_Kb, eff511, eff861, eff1004, nTot;
        nTot = 1e7;
        eff_Gamma = area_Gamma/nTot;
        eff_Ka = area_Ka/nTot;
        eff_Kb = area_Kb/nTot;
        eff511 = area511/nTot;
        eff861 = area861/nTot;
        eff1004 = area1004/nTot;

    cout << "Efficiencies: " << endl;
    cout << "Gamma = \t" << eff_Gamma << endl;
    cout << "Ka = \t\t" << eff_Ka << endl;
    cout << "Kb = \t\t" << eff_Kb << endl;
    cout << "511 keV \t" << eff511 << endl;
    cout << "861 keV \t" << eff861 << endl;
    cout << "1004 keV \t" << eff1004 << endl;
}

void RunPlotAndEff10mm(){
    PlotAndEff("../data-files_HPGe/output32_10mm.root");
    PlotAndEff("../data-files_HPGe/output35_10mm.root");
    PlotAndEff("../data-files_HPGe/output39_10mm.root");
    PlotAndEff("../data-files_HPGe/output43_10mm.root");
    PlotAndEff("../data-files_HPGe/output47_10mm.root");
    PlotAndEff("../data-files_HPGe/output50_10mm.root");
}

void RunPlotAndEff12mm(){
    PlotAndEff("../data-files_HPGe/output_Ebeam32_12mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam35_12mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam39_12mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam43_12mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam47_12mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam50_12mm.root");
}

void RunPlotAndEff16mm(){
    PlotAndEff("../data-files_HPGe/output_Ebeam32_16mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam35_16mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam39_16mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam43_16mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam47_16mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam50_16mm.root");
}

void RunPlotAndEff18mm(){
    PlotAndEff("../data-files_HPGe/output_Ebeam32_18mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam35_18mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam39_18mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam43_18mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam47_18mm.root");
    PlotAndEff("../data-files_HPGe/output_Ebeam50_18mm.root");
}