#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
#include "TF1.h"
using namespace std;

void PlotAndEff(const char* filename){

    // Energy conversion factor
    double slope = 0.0010564; // MeV/ch
    double intercept = -0.014021; // MeV
    int nrCh = 1024; 

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
     TCanvas* canvas = new TCanvas("canvas", "Energy Scoring", 800, 600);
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
     hist1->Draw();
     // Display the canvas
     canvas->SetLogy();
     canvas->Draw();
     gPad->Update();


     // ROIs for each photopeak area calculation
        // gamma 158 keV
        int binMinGamma = hist1->FindBin(0.1580);
        int binMaxGamma = hist1->FindBin(0.1591);
        // Ka
        int binMinKa = hist1->FindBin(0.0242);
        int binMaxKa = hist1->FindBin(0.0254);
        // Kb
        int binMinKb = hist1->FindBin(0.0275);
        int binMaxKb = hist1->FindBin(0.0296);

    // Calculate the area under each photopeak
        double area_Gamma = hist1->Integral(binMinGamma, binMaxGamma);
        double area_Ka = hist1->Integral(binMinKa, binMaxKa);
        double area_Kb = hist1->Integral(binMinKb, binMaxKb);

    // Calculate the detetcor efficiency for each peak energy
        double eff_Gamma, eff_Ka, eff_Kb, nTot;
        nTot = 1e7;
        eff_Gamma = area_Gamma/nTot;
        eff_Ka = area_Ka/nTot;
        eff_Kb = area_Kb/nTot;

    cout << "Efficiencies: " << endl;
    cout << "Gamma = \t" << eff_Gamma << endl;
    cout << "Ka = \t\t" << eff_Ka << endl;
    cout << "Kb = \t\t" << eff_Kb << endl;
}