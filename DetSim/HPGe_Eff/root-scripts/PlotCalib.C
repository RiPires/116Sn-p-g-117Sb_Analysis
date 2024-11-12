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

void PlotCalib(const char *simFile, const char *expFile) {
    
    // Initialize random number generator
    TRandom3 rng(0);

    // Energy conversion factor
    double slope = 0.0003225; // MeV/ch
    double intercept = -0.000149; // MeV
    int nrCh = 4096; 

    // Build costume label for saved figure and hits name
    string lab = simFile;
    lab.erase(lab.begin(), lab.begin()+26);
    lab.erase(lab.end()-5, lab.end());
    lab.append("_HPGe");
    const char *histLab = lab.c_str();
    
    // Open the simulated ROOT file
    TFile *InputTFile = new TFile(simFile, "READ");
    // Check if the file is open successfully
    if (!InputTFile || InputTFile->IsZombie()){
        cout << "Error: Could not open ROOT file." << endl;
        return;}

    // Access the Energy Scoring tree in the file  
    TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring"); 
    // Create a histogram
    TH1D* hist = new TH1D("hist", histLab, nrCh, intercept, nrCh*slope);
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

    // Open the experimental data file
    std::ifstream infile(expFile);

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
    TH1D* histExp = new TH1D("histExp", expFile, numBins, 0, numBins*slope);

    // Fill the histogram with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]);  // ROOT histograms are 1-indexed
    }
    
    // Create a canvas to plot both histograms
    string canvasTitle = "Exp vs Sim "+lab;
    const char *cTitle = canvasTitle.c_str();
    TCanvas* canvas = new TCanvas("canvas", cTitle, 1200, 900);

    histRes->SetLineColor(kBlue);
    histRes->SetLineWidth(1);
    histRes->Draw("HIST");
    histRes->GetXaxis()->SetTitle("Energy (MeV)");
    histRes->GetYaxis()->SetTitle("Yield");
    histRes->SetStats(0);

    // Draw the new histogram (histExp) with energy x-axis on the same canvas
    // Set histogram style for histExp
    histExp->SetLineColor(kRed);
    histExp->SetLineWidth(1);
    histExp->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Histogram for exp/sim ratio
    TH1D *histRatio = (TH1D*)histRes->Clone("histRatio");
    histRatio->SetTitle(histLab);
    histRatio->Divide(histExp);
    histRatio->SetLineColor(kBlack);
    histRatio->SetLineWidth(1);
    histRatio->Draw("HIST SAME");

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    //legend->AddEntry(hist, "Simulated Raw");
    legend->AddEntry(histRes, "Simulated Resolution corrected");
    legend->AddEntry(histExp, "Experimental Bg removed");
    legend->AddEntry(histRatio, "Sim/Exp");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    // Save figure
    string s = lab+".root";
    const char *figName = s.c_str();
    canvas->SaveAs(figName);
    gPad->Update();

    // Configure the ratio histogram's appearance
    histRatio->GetXaxis()->SetTitle("Energy (MeV)");
    histRatio->GetYaxis()->SetTitle("Ratio (Sim / Exp)");
    histRatio->SetLineWidth(1);
    histRatio->SetStats(0);

    // Create a new canvas for the ratio plot
    TCanvas* canvasRatio = new TCanvas("canvasRatio", "Ratio Sim/Exp", 1200, 900);
    histRatio->Draw("HIST");  // Draw the ratio histogram

    // Update the canvas to display the plot
    canvasRatio->SetLogy();
    canvasRatio->Update();
    gPad->Update();

    //cin.get();
}

void Run(){
    PlotCalib("../data-files_HPGe/output_Run01_137Cs_8mm.root", "../data-files_HPGe/Run01_137Cs_8mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run02_137Cs_50mm.root", "../data-files_HPGe/Run02_137Cs_50mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run03_152Eu_50mm.root", "../data-files_HPGe/Run03_152Eu_50mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run04_133Ba_50mm.root", "../data-files_HPGe/Run04_133Ba_50mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run05_60Co_50mm.root", "../data-files_HPGe/Run05_60Co_50mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run06_137Cs_100mm.root", "../data-files_HPGe/Run06_137Cs_100mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run07_152Eu_100mm.root", "../data-files_HPGe/Run07_152Eu_100mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run08_133Ba_100mm.root", "../data-files_HPGe/Run08_133Ba_100mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run09_133Ba_8mm.root", "../data-files_HPGe/Run09_133Ba_8mm_BgRemoved.mca");
    PlotCalib("../data-files_HPGe/output_Run10_152Eu_8mm.root", "../data-files_HPGe/Run10_152Eu_8mm_BgRemoved.mca");
}