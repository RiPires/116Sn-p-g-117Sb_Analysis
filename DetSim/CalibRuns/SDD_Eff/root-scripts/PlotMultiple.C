#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>
#include "TFile.h"
#include "TTree.h"
#include "TH1D.h"
#include "TCanvas.h"
#include "TRandom3.h"
#include "TLegend.h"

using namespace std;

// Energy conversion constants
const double SLOPE = 0.000031067; // MeV/ch
const double INTERCEPT = -0.000005703; // MeV
const int NR_CH = 2048;

// Resolution parameters (energy in MeV)
const double A = 0.000111;
const double B = -0.00043;
const double C = 0.006576;

// Helper function: Open a ROOT file and retrieve the "Scoring" tree
TTree* GetScoringTree(const char* fileName) {
    TFile* inputFile = new TFile(fileName, "READ");
    if (!inputFile || inputFile->IsZombie()) {
        cout << "Error: Could not open ROOT file " << fileName << endl;
        return nullptr;
    }
    TTree* scoringTree = (TTree*)inputFile->Get("Scoring");
    if (!scoringTree) {
        cout << "Error: 'Scoring' tree not found in file " << fileName << endl;
        return nullptr;
    }
    return scoringTree;
}

// Helper function: Extract label from file name
string ExtractLabel(const char* fileName) {
    string label = fileName;
    size_t start = label.find_last_of('/');
    if (start != string::npos) label = label.substr(start + 8);
    size_t end = label.find(".root");
    if (end != string::npos) label = label.substr(0, end);
    return label + "_SDD";
}

// Helper function: Create a histogram from a tree
TH1D* CreateHistogram(TTree* tree, const char* histName, int nrCh, double intercept, double slope) {
    TH1D* hist = new TH1D(histName, histName, nrCh, intercept, nrCh * slope);
    tree->Project(histName, "Scoring.Edep");
    return hist;
}

// Helper function: Broaden histogram using resolution parameters
TH1D* BroadenHistogram(TH1D* inputHist, TRandom3& rng) {
    TH1D* broadenedHist = (TH1D*)inputHist->Clone();
    broadenedHist->Reset();

    for (int i = 1; i <= inputHist->GetNbinsX(); ++i) {
        double E = inputHist->GetBinCenter(i);          // Energy
        double content = inputHist->GetBinContent(i);  // Counts
        if (content == 0) continue;                    // Skip empty bins

        // Calculate FWHM and sigma
        double dE = A + B * sqrt(E) + C * E;
        double sigma_E = dE / 2.355;

        // Redistribute bin content using Gaussian
        for (int k = 0; k < content; ++k) {
            double newE = rng.Gaus(E, sigma_E);
            int bin = broadenedHist->FindBin(newE);
            if (bin >= 1 && bin <= broadenedHist->GetNbinsX()) {
                broadenedHist->AddBinContent(bin, 1);
            }
        }
    }
    return broadenedHist;
}

// Helper function: Load experimental data into a histogram
TH1D* LoadExperimentalData(const char* expFile, int nrCh, double intercept, double slope) {
    ifstream infile(expFile);
    if (!infile.is_open()) {
        cerr << "Error: Could not open the experimental file " << expFile << endl;
        return nullptr;
    }

    // Skip the first 12 lines
    string line;
    for (int i = 0; i < 12; ++i) getline(infile, line);

    // Read data values
    vector<double> dataValues;
    double value;
    while (infile >> value) dataValues.push_back(value);
    infile.close();

    // Create histogram
    TH1D* histExp = new TH1D("histExp", expFile, nrCh, intercept, nrCh * slope);
    for (size_t i = 0; i < dataValues.size(); ++i) {
        double energy = (i + 0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]);
    }
    return histExp;
}

// Main function: Plot distance
void PlotMultiple(vector<const char*> simFiles, const char* expFile) {
    TRandom3 rng(0); // Random number generator

    // Prepare histograms
    vector<TH1D*> broadenedHists;
    vector<string> labels;
    for (size_t i = 0; i < simFiles.size(); ++i) {
        TTree* scoringTree = GetScoringTree(simFiles[i]);
        if (!scoringTree) return;

        string histLabel = ExtractLabel(simFiles[i]);
        labels.push_back(histLabel);

        TH1D* hist = CreateHistogram(scoringTree, histLabel.c_str(), NR_CH, INTERCEPT, SLOPE);
        TH1D* broadenedHist = BroadenHistogram(hist, rng);
        broadenedHists.push_back(broadenedHist);
    }

    // Load experimental data
    TH1D* histExp = LoadExperimentalData(expFile, NR_CH, INTERCEPT, SLOPE);
    if (!histExp) return;

    // Create a canvas
    TCanvas* canvas = new TCanvas("canvas", "Simulated vs Experimental Data", 1200, 900);
    canvas->SetLogy();

    // Plot histograms
    vector<int> colors = {kBlue, kOrange, kGreen, kRed, kMagenta}; // Assign colors
    for (size_t i = 0; i < broadenedHists.size(); ++i) {
        broadenedHists[i]->SetLineColor(colors[i % colors.size()]);
        broadenedHists[i]->SetLineWidth(1);
        if (i == 0) {
            broadenedHists[i]->Draw("HIST");
            broadenedHists[i]->GetXaxis()->SetTitle("Energy (MeV)");
            broadenedHists[i]->GetYaxis()->SetTitle("Yield");
            broadenedHists[i]->SetStats(0);
        } else {
            broadenedHists[i]->Draw("HIST SAME");
        }
    }

    // Plot experimental data
    histExp->SetLineColor(kBlack);
    histExp->SetLineWidth(1);
    histExp->Draw("HIST SAME");

    // Add legend
    TLegend* legend = new TLegend(0.6, 0.7, 0.9, 0.9);
    for (size_t i = 0; i < broadenedHists.size(); ++i) {
        legend->AddEntry(broadenedHists[i], labels[i].c_str());
    }
    legend->AddEntry(histExp, "Experimental = 2 mm");
    legend->Draw();

    // Update canvas
    canvas->Update();
    // Save figure
    //string s = labels[0]+".root";
    //const char *figName = s.c_str();
    //canvas->SaveAs(figName);
    gPad->Update();
}

// Wrapper functions to run the script for each calibration Run
void Run11() {
    vector<const char*> simFiles = {
        "../data-files_SDD/output_Run11_152Eu_16mm_Ni-Cover.root",
        "../data-files_SDD/output_Run11_152Eu_17mm.root",
        "../data-files_SDD/output_Run11_152Eu_18mm.root"
    };
    const char* expFile = "../data-files_SDD/Run11_152Eu_detSDD_16mm.mca";
    PlotMultiple(simFiles, expFile);
}

void Run14() {
    vector<const char*> simFiles = {
        "../data-files_SDD/output_Run14_152Eu_2mm_Ni-Cover.root",
        "../data-files_SDD/output_Run14_152Eu_3mm.root",
        "../data-files_SDD/output_Run14_152Eu_4mm.root"
    };
    const char* expFile = "../data-files_SDD/Run14_152Eu_detSDD_2mm.mca";
    PlotMultiple(simFiles, expFile);
}

void Run15() {
    vector<const char*> simFiles = {
        "../data-files_SDD/output_Run15_133Ba_2mm_Ni-Cover.root",
        "../data-files_SDD/output_Run15_133Ba_5mm.root",
        "../data-files_SDD/output_Run15_133Ba_6mm.root",
        "../data-files_SDD/output_Run15_133Ba_10mm.root"
    };
    const char* expFile = "../data-files_SDD/Run15_133Ba_detSDD_2mm.mca";
    PlotMultiple(simFiles, expFile);
}