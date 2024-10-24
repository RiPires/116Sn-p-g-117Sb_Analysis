#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"

using namespace std;

void PlotBoth(const char *filename) {
    
    // Open the ROOT file
    TFile *InputTFile = new TFile(filename, "READ");
    // Check if the file is open successfully
    if (!InputTFile || InputTFile->IsZombie()){
        cout << "Error: Could not open ROOT file." << endl;
        return;}

    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring"); 

    // Energy conversion factor
    double slope = 0.0003225; // MeV/ch
    double intercept = -0.000149; // MeV
    int nrCh = 4096; 

    // Create a histogram
    TH1D* hist = new TH1D("hist", "HPGe simulated 152Eu @ 8 mm", nrCh, intercept, nrCh*slope);
    
    // Project the variable into the histogram
    ScoringTTRee->Project("hist", "Scoring.Edep");
    
    // Open the experimental data file
    std::ifstream infile("152Eu_8mm_BgRemovedRate.mca");

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the file and skip the first 15 lines
    std::string line;
    for (int i = 0; i < 0; i++) {
        std::getline(infile, line);
    }

    // Vector to store data values (from the <<DATA>> section)
    std::vector<double> dataValues;

    // Now read the spectrum data starting from line 15
    double value;
    while (infile >> value) {
        dataValues.push_back(value);
    }

    infile.close();  // Close the file after reading

    // Create a histogram for the data from the file, in channel units
    int numBins = dataValues.size();
    TH1D* hist2 = new TH1D("hist2", "Spectrum from File", numBins, 0, numBins*slope);


    // Fill the histogram with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope + intercept;
        hist2->SetBinContent(hist2->FindBin(energy), dataValues[i]);  // ROOT histograms are 1-indexed
    }
    
    // Create a canvas to plot both histograms
    TCanvas* canvas = new TCanvas("canvas", "Overlay of Histograms", 800, 600);

    // Draw the original normalized histogram (histNorm) first
    hist->SetLineColor(kBlue);  // Set different color for the normalized histogram
    hist->SetLineWidth(1);
    hist->Draw("HIST");        // "HIST" option to draw as histogram
    hist->GetXaxis()->SetTitle("Energy (MeV)");
    hist->GetYaxis()->SetTitle("Count Rate (s^{-1})");
    hist->SetStats(0);

    // Draw the new histogram (hist2) with energy x-axis on the same canvas
        // Set histogram style for hist2
    hist2->SetLineColor(kRed);
    hist2->SetLineWidth(2);
    hist2->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    legend->AddEntry(hist, "Simulated");
    legend->AddEntry(hist2, "Experimental");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    gPad->Update();


}