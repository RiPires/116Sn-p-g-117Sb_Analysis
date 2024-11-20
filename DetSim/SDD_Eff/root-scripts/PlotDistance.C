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

void PlotDistance(const char *simFile1, const char *simFile2, const char *simFile3, const char *expFile) {
    
    // Initialize random number generator
    TRandom3 rng(0);

    // Energy conversion factor
    double slope = 0.000031067; // MeV/ch
    double intercept = -0.000005703; // MeV
    int nrCh = 2048;

    // Build costume label for saved figure and hits name
    string lab = simFile1;
    lab.erase(lab.begin(), lab.begin()+25);
    lab.erase(lab.end()-5, lab.end());
    lab.append("_SDD");
    const char *histLab = lab.c_str();
    
    // Open the 1st simulated ROOT file
    TFile *InputTFile1 = new TFile(simFile1, "READ");
    // Check if the file is open successfully
    if (!InputTFile1 || InputTFile1->IsZombie()){
        cout << "Error: Could not open ROOT file." << endl;
        return;}
    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee1 = (TTree*)InputTFile1->Get("Scoring"); 
    // Create a histogram
    TH1D* hist1 = new TH1D("hist1", histLab, nrCh, intercept, nrCh*slope);
    // Project the variable into the histogram
    ScoringTTRee1->Project("hist1", "Scoring.Edep");

        // Open the 2nd simulated ROOT file
    TFile *InputTFile2 = new TFile(simFile2, "READ");
    // Check if the file is open successfully
    if (!InputTFile2 || InputTFile2->IsZombie()){
        cout << "Error: Could not open ROOT file." << endl;
        return;}
    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee2 = (TTree*)InputTFile2->Get("Scoring"); 
    // Create a histogram
    TH1D* hist2 = new TH1D("hist2", histLab, nrCh, intercept, nrCh*slope);
    // Project the variable into the histogram
    ScoringTTRee2->Project("hist2", "Scoring.Edep");

        // Open the 3rd simulated ROOT file
    TFile *InputTFile3 = new TFile(simFile3, "READ");
    // Check if the file is open successfully
    if (!InputTFile3 || InputTFile3->IsZombie()){
        cout << "Error: Could not open ROOT file." << endl;
        return;}
    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee3 = (TTree*)InputTFile3->Get("Scoring"); 
    // Create a histogram
    TH1D* hist3 = new TH1D("hist3", histLab, nrCh, intercept, nrCh*slope);
    // Project the variable into the histogram
    ScoringTTRee3->Project("hist3", "Scoring.Edep");

    // Detector resolution parameters (energy in MeV)
    double a = 0.000211;
    double b = -0.00083;
    double c = 0.006576;

    // New histgram 1 for resolution broadened spectrum
    TH1D *histRes1 = (TH1D*)hist1->Clone("histRes1");
    histRes1->Reset();

    // Loop over each bin in the original simulated histogram
    for (int i = 1; i <= hist1->GetNbinsX(); ++i){
        
        double E1 = hist1->GetBinCenter(i);           // Energy
        double content1 = hist1->GetBinContent(i);    // Counts

        if (content1 == 0) continue;                 // Skip empty bins

        // Calculate FWHM at energy E
        double dE1 = a + b * sqrt(E1) + c * E1;
        double sigma_E1 = dE1 / 2.355;

        // Redistribute bin content using Gaussian
        for (int k = 0; k < content1; ++k){
            
            // Sampling new energy
            double newE1 = rng.Gaus(E1, sigma_E1);
            // Find the bin corresponding to this new energy
            int bin = histRes1->FindBin(newE1);
            // Only add counts within the histogram range
            if (bin >= 1 && bin <= histRes1->GetNbinsX()){
                histRes1->AddBinContent(bin, 1);
            }
        }
    }

    // New histgram 2 for resolution broadened spectrum
    TH1D *histRes2 = (TH1D*)hist2->Clone("histRes2");
    histRes2->Reset();

    // Loop over each bin in the original simulated histogram
    for (int i = 1; i <= hist2->GetNbinsX(); ++i){
        
        double E2 = hist2->GetBinCenter(i);           // Energy
        double content2 = hist2->GetBinContent(i);    // Counts

        if (content2 == 0) continue;                 // Skip empty bins

        // Calculate FWHM at energy E
        double dE2 = a + b * sqrt(E2) + c * E2;
        double sigma_E2 = dE2 / 2.355;

        // Redistribute bin content using Gaussian
        for (int k = 0; k < content2; ++k){
            
            // Sampling new energy
            double newE2 = rng.Gaus(E2, sigma_E2);
            // Find the bin corresponding to this new energy
            int bin = histRes2->FindBin(newE2);
            // Only add counts within the histogram range
            if (bin >= 1 && bin <= histRes2->GetNbinsX()){
                histRes2->AddBinContent(bin, 1);
            }
        }
    }

    // New histgram 3 for resolution broadened spectrum
    TH1D *histRes3 = (TH1D*)hist3->Clone("histRes3");
    histRes3->Reset();

    // Loop over each bin in the original simulated histogram
    for (int i = 1; i <= hist3->GetNbinsX(); ++i){
        
        double E3 = hist3->GetBinCenter(i);           // Energy
        double content3 = hist3->GetBinContent(i);    // Counts

        if (content3 == 0) continue;                 // Skip empty bins

        // Calculate FWHM at energy E
        double dE3 = a + b * sqrt(E3) + c * E3;
        double sigma_E3 = dE3 / 2.355;

        // Redistribute bin content using Gaussian
        for (int k = 0; k < content3; ++k){
            
            // Sampling new energy
            double newE3 = rng.Gaus(E3, sigma_E3);
            // Find the bin corresponding to this new energy
            int bin = histRes3->FindBin(newE3);
            // Only add counts within the histogram range
            if (bin >= 1 && bin <= histRes3->GetNbinsX()){
                histRes3->AddBinContent(bin, 1);
            }
        }
    }

    // Open the experimental data file
    std::ifstream infile(expFile);

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the file and skip the first 15 lines
    std::string line;
    for (int i = 0; i < 12; i++) {
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
    TH1D* histExp = new TH1D("histExp", expFile, nrCh, intercept, nrCh*slope);

    // Fill the histogram with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]);  // ROOT histograms are 1-indexed
    }
    
    // Create a canvas to plot both histograms
    string canvasTitle = "Exp vs Sim "+lab;
    const char *cTitle = canvasTitle.c_str();
    TCanvas* canvas = new TCanvas("canvas", cTitle, 1200, 900);

    histRes1->SetLineColor(kBlue);
    histRes1->SetLineWidth(1);
    histRes1->Draw("HIST");
    histRes1->GetXaxis()->SetTitle("Energy (MeV)");
    histRes1->GetYaxis()->SetTitle("Yield");
    histRes1->SetStats(0);

    // Draw the new histogram (histExp) with energy x-axis on the same canvas
    // Set histogram style for histExp
    histRes2->SetLineColor(kOrange);
    histRes2->SetLineWidth(1);
    histRes2->Draw("HIST SAME");  // "SAME" option to overlay histograms

        // Draw the new histogram (histExp) with energy x-axis on the same canvas
    // Set histogram style for histExp
    histRes3->SetLineColor(kGreen);
    histRes3->SetLineWidth(1);
    histRes3->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Draw the new histogram (histExp) with energy x-axis on the same canvas
    // Set histogram style for histExp
    histExp->SetLineColor(kRed);
    histExp->SetLineWidth(1);
    histExp->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Histogram for exp/sim ratio
    //TH1D *histRatio = (TH1D*)histRes->Clone("histRatio");
    //histRatio->SetTitle(histLab);
    //histRatio->Divide(histExp);
    //histRatio->SetLineColor(kBlack);
    //histRatio->SetLineWidth(1);
    //histRatio->Draw("HIST SAME");

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    //legend->AddEntry(hist, "Simulated Raw");
    legend->AddEntry(histRes1, "No cut 2 mm");
    legend->AddEntry(histRes2, "50 keV event 2 mm");
    legend->AddEntry(histRes3, "50 keV StopAndKill mm");
    legend->AddEntry(histExp, "Experimental: 2 mm");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    // Save figure
    //string s = lab+".root";
    //const char *figName = s.c_str();
    //canvas->SaveAs(figName);
    gPad->Update();

    //cin.get();
}

void Run(){
    PlotDistance("../data-files_SDD/output_Run14_152Eu_2mm_Ni-Cover.root",
                 "../data-files_SDD/output_Run14_152Eu_2mm_Ecut50keVHigh.root",
                 "../data-files_SDD/output_Run14_152Eu_2mm_GPS.root",
                 "../data-files_SDD/Run14_152Eu_detSDD_2mm.mca");
}