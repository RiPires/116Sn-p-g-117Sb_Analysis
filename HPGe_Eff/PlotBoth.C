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

    // Create a histogram
    TH1D* hist = new TH1D("hist", "Ge energy scoring", 4096, 0, 1.319);
    
    // Project the variable into the histogram
    ScoringTTRee->Project("hist", "Scoring.Edep");

    // New histogram for simulated normalized yield discarding first 2 bins
    int numBinsNew = hist->GetNbinsX();
    TH1D* histNorm = new TH1D("histNorm", "Normalized Ge Energy Scoring", numBinsNew, 0., 1.320);  // Adjust bin range
    
    // Copy contents from the third bin onward from hist1 to histNorm
    for (int i = 3; i <= hist->GetNbinsX(); i++) {
        double binContent = hist->GetBinContent(i);
        histNorm->SetBinContent(i - 2, binContent);  // Shift by 2 to adjust bin indices
    }

    cout << "Sim hist nr. bins: " << hist->GetNbinsX() << endl;
    cout << "Sim norm hist nr. bins: " << histNorm->GetNbinsX() << endl;

    // Find the maximum yield (ignoring the first two bins)
    double maxYieldSim = histNorm->GetMaximum();
    std::cout << "Maximum yield (excluding first 2 bins): " << maxYieldSim << std::endl;

    // Normalize the bin content by the maximum yield
    for (int i = 1; i <= histNorm->GetNbinsX(); i++) {
        double binContent = histNorm->GetBinContent(i);
        histNorm->SetBinContent(i, binContent / maxYieldSim);
    }
    
    // Open the data file
    std::ifstream infile("Run03_152Eu_detGe_50mm.mca");

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the file and skip the first 15 lines
    std::string line;
    for (int i = 0; i < 14; i++) {
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

    // FInd experimental maximum yield
    double max = *std::max_element(dataValues.begin(), dataValues.end());

    // Energy conversion factor
    double slope = 0.0003225; // MeV/ch

    // Create a histogram for the data from the file, in channel units
    int numBins = dataValues.size();
    TH1D* hist2 = new TH1D("hist2", "Spectrum from File", numBins, 0, numBins*slope);


    // Fill the histogram with the NORMALIZED data values, with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope - 0.000149;
        hist2->SetBinContent(hist2->FindBin(energy), dataValues[i]/max);  // ROOT histograms are 1-indexed
    }

    cout << "Exp hist nr. bins: " << hist2->GetNbinsX() << endl;

    // Create a canvas to plot both histograms
    TCanvas* canvas = new TCanvas("canvas", "Overlay of Histograms", 800, 600);

    // Draw the original normalized histogram (histNorm) first
    histNorm->SetLineColor(kBlue);  // Set different color for the normalized histogram
    histNorm->SetLineWidth(1);
    histNorm->Draw("HIST");        // "HIST" option to draw as histogram
    histNorm->GetXaxis()->SetTitle("Energy (MeV)");
    histNorm->GetYaxis()->SetTitle("Counts");
    histNorm->SetStats(0);

    // Draw the new histogram (hist2) with energy x-axis on the same canvas
        // Set histogram style for hist2
    hist2->SetLineColor(kRed);
    hist2->SetLineWidth(2);
    hist2->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    legend->AddEntry(histNorm, "Simulated");
    legend->AddEntry(hist2, "Experimental");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    gPad->Update();


}