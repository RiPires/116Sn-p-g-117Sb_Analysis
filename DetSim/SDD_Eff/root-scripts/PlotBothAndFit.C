#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TRandom3.h"
#include "FitPeak.C"

using namespace std;

void PlotBothAndFit(const char *simFilename, const char *expFilename, const vector<double> fitMin, const vector<double> fitMax) {
    
    // Initialize random number generator
    TRandom3 rng(0);

    // Energy conversion factor
    double slope = 0.000031067; // MeV/ch
    double intercept = -0.000005703; // MeV
    int nrCh = 2048; 

    // Build costume label for figures
    string lab = simFilename;
    lab.erase(lab.begin(), lab.begin()+25);
    lab.erase(lab.end()-5, lab.end());
    lab.append(" SDD");
    const char *histLab = lab.c_str();
    
    // Open the ROOT file
    TFile *InputTFile = new TFile(simFilename, "READ");
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
    double a = 0.000111;
    double b = -0.00043;
    double c = 0.006576;

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
    std::ifstream infile(expFilename);

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the file and skip the first 12 lines
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
    TH1D* histExp = new TH1D("histExp", "Spectrum from File", nrCh, intercept, nrCh*slope);

    // Fill the histogram with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]);  // ROOT histograms are 1-indexed
    }
    
    // Create a canvas to plot both histograms
    TCanvas* canvas = new TCanvas("canvas", "Exp vs Sim SDD Calib", 1200, 900);

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

    // Histogram legend
    auto legend = new TLegend(0.6,0.7,0.9,0.9);
    //legend->AddEntry(hist, "Simulated Raw");
    legend->AddEntry(histRes, "Simulated Resolution corrected");
    legend->AddEntry(histExp, "Experimental");
    legend->Draw();

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
    gPad->Update();

    // Fit peaks for both histograms
    // Sim
    vector<double> simIntegrals = FitPeak(histRes, fitMin, fitMax);
    // Exp
    vector<double> expIntegrals = FitPeak(histExp, fitMin, fitMax);

    // Print Sim/Exp peak integral ratio
    for (int i = 0; i <= simIntegrals.size(); ++i){
        // Calculates ratio for peak the ith peak
        double ratio = simIntegrals[i]/expIntegrals[i];
        cout << "Peak nr. " << i+1 << " Sim/Exp integral ratio: " << ratio << endl;
    }
}


void Run11(){
    
    // Peak ROIs for Run 11, 152Eu, 16 mm
    cout << "\nPeak Sim/Exp ratio for Run11, 152Eu, 16 mm" << endl;
    cout << "------------------------------------------" << endl;
    const vector<double> fitMin = {0.00485, 0.00540, 0.00594, 0.00645, 0.00694, 0.00735, 0.03916, 0.03985, 0.04504, 0.04632}; // units in MeV
    const vector<double> fitMax = {0.00519, 0.00588, 0.00642, 0.00683, 0.00734, 0.00759, 0.03980, 0.04059, 0.04596, 0.04699}; // units in MeV

    PlotBothAndFit("../data-files_SDD/output_Run11_152Eu_16mm_Ni-Cover.root", "../data-files_SDD/Run11_152Eu_detSDD_16mm.mca", fitMin, fitMax);
    cout << "\n" << endl;
}

void Run13(){
    
    // Peak ROIs for Run 13, 133Ba, 16 mm
    cout << "\nPeak Sim/Exp ratio for Run13, 133Ba, 16 mm" << endl;
    cout << "------------------------------------------" << endl;
    const vector<double> fitMin = {0.00407, 0.00447, 0.00485, 0.00514, 0.00543, 0.03458, 0.03551}; // units in MeV
    const vector<double> fitMax = {0.00444, 0.00480, 0.00505, 0.00539, 0.00566, 0.03544, 0.03614}; // units in MeV

    PlotBothAndFit("../data-files_SDD/output_Run13_133Ba_16mm_Ni-Cover.root", "../data-files_SDD/Run13_133Ba_detSDD_16mm.mca", fitMin, fitMax);
    cout << "\n" << endl;
}

void Run14(){
    
    // Peak ROIs for Run 14, 152Eu, 2 mm
    cout << "\nPeak Sim/Exp ratio for Run14, 152Eu, 2 mm" << endl;
    cout << "------------------------------------------" << endl;
    const vector<double> fitMin = {0.00485, 0.00540, 0.00594, 0.00645, 0.00694, 0.00735, 0.03916, 0.03985, 0.04504, 0.04632}; // units in MeV
    const vector<double> fitMax = {0.00519, 0.00588, 0.00642, 0.00683, 0.00734, 0.00759, 0.03980, 0.04059, 0.04596, 0.04699}; // units in MeV

    PlotBothAndFit("../data-files_SDD/output_Run14_152Eu_2mm_test2.root", "../data-files_SDD/Run14_152Eu_detSDD_2mm.mca", fitMin, fitMax);
    cout << "\n" << endl;
}

void Run15(){
    
    // Peak ROIs for Run 15, 133Ba, 2 mm
    cout << "\nPeak Sim/Exp ratio for Run15, 133Ba, 2 mm" << endl;
    cout << "------------------------------------------" << endl;
    const vector<double> fitMin = {0.00407, 0.00447, 0.00485, 0.00514, 0.00543, 0.03458, 0.03551}; // units in MeV
    const vector<double> fitMax = {0.00444, 0.00480, 0.00505, 0.00539, 0.00566, 0.03544, 0.03614}; // units in MeV

    PlotBothAndFit("../data-files_SDD/output_Run15_133Ba_2mm.root", "../data-files_SDD/Run15_133Ba_detSDD_2mm.mca", fitMin, fitMax);
    cout << "\n" << endl;
}