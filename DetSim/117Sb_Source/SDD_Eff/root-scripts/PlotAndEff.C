#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
#include "TF1.h"
#include <iomanip>
using namespace std;

void PlotAndEff(const char* filename){

    // Energy conversion factor
    double slope = 0.000031059; // MeV/ch
    double intercept = -0.0000041372; // MeV
    int nrCh = 2048;  

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
     /*hist1->SetLineColor(kBlue);
     hist1->SetLineWidth(2);
     hist1->GetXaxis()->SetTitle("Energy (MeV)");
     hist1->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     hist1->Draw();
     // Display the canvas
     canvas->SetLogy();
     canvas->Draw();
     gPad->Update();*/


     // ROIs for each photopeak area calculation
        // L- lines
        int binMinL = hist1->FindBin(0.003044);
        int binMaxL = hist1->FindBin(0.004381);
        // Ka
        int binMinKa = hist1->FindBin(0.0250);
        int binMaxKa = hist1->FindBin(0.0253);
        // Kb
        int binMinKb = hist1->FindBin(0.0283);
        int binMaxKb = hist1->FindBin(0.0285);

    // Calculate the area under each photopeak
        double area_L = hist1->Integral(binMinL, binMaxL);
        double area_Ka = hist1->Integral(binMinKa, binMaxKa);
        double area_Kb = hist1->Integral(binMinKb, binMaxKb);

    // Calculate the detetcor efficiency for each peak energy
        double eff_L, eff_Ka, eff_Kb, nTot;
        nTot = 1e7;
        eff_L = area_L/nTot;
        eff_Ka = area_Ka/nTot;
        eff_Kb = area_Kb/nTot;

    cout << std::scientific << std::setprecision(3);
    cout << "[" << eff_Ka << ", " << eff_Kb << ", " << eff_L << "]," << endl;
}

void RunPlotAndEff_7mm(){
	PlotAndEff("../data-files_SDD/output_Ebeam32_7mm.root");
	PlotAndEff("../data-files_SDD/output_Ebeam35_7mm.root");
	PlotAndEff("../data-files_SDD/output_Ebeam39_7mm.root");
	PlotAndEff("../data-files_SDD/output_Ebeam43_7mm.root");
	PlotAndEff("../data-files_SDD/output_Ebeam47_7mm.root");
	PlotAndEff("../data-files_SDD/output_Ebeam50_7mm.root");
}

void RunPlotAndEff_9mm(){
	PlotAndEff("../data-files_SDD/output_Ebeam32_9mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam35_9mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam39_9mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam43_9mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam47_9mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam50_9mm_0Al.root");
}

void RunPlotAndEff_10mm(){
    cout << "Efficiencies: " << endl;
    cout << "[\t Ka, \t Kb, \t L-]" << endl;
	PlotAndEff("../data-files_SDD/output_Ebeam32_10mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam35_10mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam39_10mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam43_10mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam47_10mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam50_10mm_0Al.root");
}

void RunPlotAndEff_11mm(){
	PlotAndEff("../data-files_SDD/output_Ebeam32_11mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam35_11mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam39_11mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam43_11mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam47_11mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam50_11mm_0Al.root");
}

void RunPlotAndEff_12mm(){
	PlotAndEff("../data-files_SDD/output_Ebeam32_12mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam35_12mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam39_12mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam43_12mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam47_12mm_0Al.root");
	PlotAndEff("../data-files_SDD/output_Ebeam50_12mm_0Al.root");
}