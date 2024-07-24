#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
#include "TF1.h"
using namespace std;

double PlotAndFit(const char* filename, double fitMin, double fitMax){

     // Open the ROOT file
     TFile *InputTFile = new TFile(filename, "READ");
     // Check if the file is open successfully
     if (!InputTFile || InputTFile->IsZombie()){
          cout << "Error: Could not open ROOT file." << endl;
          return 0;} 
    
     /////////////////////////////////////////////////
     // Access the Energy Scoring tree in the file  //
     /////////////////////////////////////////////////
     TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring");
     ////////////////////////////////////////////////////
     // Create a canvas for plotting deposited energy  //
     ////////////////////////////////////////////////////
     TCanvas* canvas = new TCanvas("canvas", "Energy Scoring", 800, 600);
     // Create a histogram
     TH1D* hist1 = new TH1D("hist", "Ge energy scoring", 500, 0., 1.);
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

    cout << "fitMin = " << fitMin << endl;
    cout << "fitMax = " << fitMax << endl;

    int binMin = hist1->FindBin(fitMin);
    int binMax = hist1->FindBin(fitMax);

    cout << "binMin = " << binMin << endl;
    cout << "binMax = " << binMax << endl;

    // Calculate and print the area under the Photopeak
    double area = hist1->Integral(binMin,binMax);
    cout << "Area under the Photo-peak: " << area << endl;

    cout << area << endl;
    // Calculate det efficiency at this energy
    double detEff, nTot;
    nTot = 1000000.;
    detEff = area/nTot * 100; // %
    cout << "Detector efficiency = " << detEff << " %" << endl;

    return detEff;
}   