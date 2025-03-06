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

    // Energy calibration parameters
    double slope = 0.0010564; // MeV/channel
    double intercept = -0.014207; // MeV
    int nrCh = 1024;

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

        // Calculate FWHM and sigma at energy E
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

    // Read the file
    std::string line;
    for (int i = 0; i < 1; i++) {
        std::getline(infile, line);
    }

    // Vector to store data values (from the <<DATA>> section)
    std::vector<double> dataValues;

    // Now read the spectrum data
    double value;
    while (infile >> value) {
        dataValues.push_back(value);
    }

    // Close the file after reading
    infile.close();  

    // Create a histogram for the experimental data
    TH1D* histExp = new TH1D("histExp", expFile, nrCh, intercept, nrCh*slope);

    // Fill the histogram with channels converted to energy
    for (int i = 0; i < nrCh; i++) {
        double energy = (i+0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]);  // ROOT histograms are 1-indexed
    }
    
    // Create a canvas to show both histograms
    string canvasTitle = "Exp vs Sim "+lab;
    const char *cTitle = canvasTitle.c_str();
    TCanvas* canvas = new TCanvas("canvas", cTitle, 1200, 900);

    histRes->SetLineColor(kBlue);
    histRes->SetLineWidth(1);
    histRes->Draw("HIST");
    histRes->GetXaxis()->SetTitle("Energy (MeV)");
    histRes->GetYaxis()->SetTitle("Yield");
    histRes->SetStats(0);

    // Draw the new histogram (histExp) on the same canvas
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

    // Histograms legend
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
    //string s = lab+".root";
    //const char *figName = s.c_str();
    //canvas->SaveAs(figName);
    gPad->Update();

    //cin.get();
}

void Run(){
    PlotCalib("../data-files_BEGe/output_137Cs_10mm.root", "../data-files_BEGe/415113G2_137Cs.TXT");
}