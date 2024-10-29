#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TRandom3.h"

using namespace std;

void PlotBoth(const char *filename) {
    
    // Initialize random number generator
    TRandom3 rng(0);

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

    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring"); 
    // Create a histogram
    TH1D* hist = new TH1D("hist", "HPGe 152Eu @ 8 mm", nrCh, intercept, nrCh*slope);
    // Project the variable into the histogram
    ScoringTTRee->Project("hist", "Scoring.Edep");

    // Detector resolution parameters
    double a = 0.002162;
    double b = -0.002756;
    double c = 0.003346;

    // New histgram for resolution broadened spectrum
    TH1D *histRes = (TH1D*)hist->Clone("histRes");
    histRes->Reset();

    // Loop over each bin in the original simulated histogram
    for (int i = 1; i <= hist->GetNbinsX(); ++i){
        
        double E = hist->GetBinCenter(i);           // Energy
        double content = hist->GetBinContent(i);    // Counts

        if (content == 0) continue;                 // Skip empty bins

        // Calculate FWHM at energy E
        double dE = a + b * sqrt(E) + c * E;
        double sigma_E = dE / 2.355;

        // Redistribute bin content using Gaussian
        for (int k = 0; k < content; ++k){
            
            // Sampling new energy
            double newE = rng.Gaus(E, sigma_E);
            // Find the bin corresponding to this new energy
            int bin = histRes->FindBin(newE);
            // Only add counts within the histogram range
            if (bin >= 1 && bin <= histRes->GetNbinsX()){
                histRes->AddBinContent(bin, 1);
            }
        }
    }

    TCanvas *canvaRes = new TCanvas("canvaRes", "Resolution effect comparission", 800, 600);
    hist->SetLineColor(kRed);
    histRes->SetLineColor(kBlue);
    hist->Draw("HIST");
    hist->SetStats(0);
    histRes->Draw("HIST SAME");

    // Histogram legend
    auto legendRes = new TLegend(0.6,0.7,0.9,0.9);
    legendRes->AddEntry(hist, "Raw");
    legendRes->AddEntry(histRes, "Resolution");
    legendRes->Draw();

    // Update the canvas to display the plot
    canvaRes->SetLogy();
    canvaRes->Update();
    gPad->Update();


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
        dataValues.push_back(value*900);
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
    // hist->SetLineColor(kBlue);  // Set different color for the normalized histogram
    // hist->SetLineWidth(2);
    // hist->Draw("HIST");        // "HIST" option to draw as histogram
    // hist->GetXaxis()->SetTitle("Energy (MeV)");
    // hist->GetYaxis()->SetTitle("Count Rate (s^{-1})");
    // hist->SetStats(0);

    histRes->SetLineColor(kBlue);
    histRes->SetLineWidth(1);
    histRes->Draw("HIST");
    histRes->GetXaxis()->SetTitle("Energy (MeV)");
    histRes->GetYaxis()->SetTitle("Yield");
    histRes->SetStats(0);

    // Draw the new histogram (hist2) with energy x-axis on the same canvas
    // Set histogram style for hist2
    hist2->SetLineColor(kRed);
    hist2->SetLineWidth(1);
    hist2->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    //legend->AddEntry(hist, "Simulated Raw");
    legend->AddEntry(histRes, "Simulated Resolution corrected");
    legend->AddEntry(hist2, "Experimental Bg removed");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    canvas->SaveAs("HPGe_152Eu_8mm_900s-activity_bgrm_res.svg");
    gPad->Update();
}