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

void PlotBothNorm(const char *simFilename, const char *expFilename) {
    
    // Initialize random number generator
    TRandom3 rng(0);

    // Energy conversion factor
    double slope = 0.0003225; // MeV/ch
    double intercept = -0.000149; // MeV
    int nrCh = 4096; 

    // Build costume label for figures
    string lab = simFilename;
    lab.erase(lab.begin(), lab.begin()+26);
    lab.erase(lab.end()-5, lab.end());
    lab.append("_HPGe");
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
    double a = 0.002162;
    double b = -0.002756;
    double c = 0.003346;

    // New histgram for resolution broadened NORMALIZED spectrum
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

    // Find maximum yield of the resolution broadened spectrum
    double maxYield = histRes->GetMaximum();

    // Normalize the bin content  by the maximum yield
    for (int i = 0; i<= nrCh; i++){
        double binContent = histRes->GetBinContent(i);
        histRes->SetBinContent(i, binContent/maxYield);
    }

    // Open the experimental data file
    std::ifstream infile(expFilename);

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the experimental file
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

    // Find experimetal data maximum yield
    double expMaxYield = *std::max_element(dataValues.begin(), dataValues.end());

    // Create a histogram for the data from the file, in channel units
    int numBins = dataValues.size();
    TH1D* histExp = new TH1D("histExp", "Spectrum from File", nrCh, intercept, nrCh*slope);

    // Fill the histogram with the NORMALIZED experimental data, with channels converted to energy
    for (int i = 0; i < numBins; i++) {
        double energy = (i+0.5) * slope + intercept;
        histExp->SetBinContent(histExp->FindBin(energy), dataValues[i]/expMaxYield);  // ROOT histograms are 1-indexed
    }
    
    /*// Create a canvas to plot both histograms
    TCanvas* canvas = new TCanvas("canvas", "Exp vs Sim SDD Calib", 1200, 900);

    histRes->SetLineColor(kBlue);
    histRes->SetLineWidth(1);
    histRes->Draw("HIST");
    histRes->GetXaxis()->SetTitle("Energy (MeV)");
    histRes->GetYaxis()->SetTitle("Normalized Yield");
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
    // Save figure
    string s = lab+"_Normalized.root";
    const char *figName = s.c_str();
    canvas->SaveAs(figName);
    gPad->Update();*/

    //
    // Calculate Sim to Exp peak area ratio
    //

    // ROIs for each photopeak area calculation
    // Simulated:
    // gamma 158 keV
    int binMinGamma = histRes->FindBin(0.15853);
    int binMaxGamma = histRes->FindBin(0.15887);
    // Ka
    int binMinKa = histRes->FindBin(0.0247);
    int binMaxKa = histRes->FindBin(0.0253);
    // Kb
    int binMinKb = histRes->FindBin(0.02833);
    int binMaxKb = histRes->FindBin(0.0293);
    // gamma 511 keV
    int binMin511 = histRes->FindBin(0.5108);
    int binMax511 = histRes->FindBin(0.511); 
    // gamma 861 keV
    int binMin861 = histRes->FindBin(0.86108);
    int binMax861 = histRes->FindBin(0.86142);
    // gamma 1004 keV
    int binMin1004 = histRes->FindBin(1.00448);
    int binMax1004 = histRes->FindBin(1.00484);

    // Experimental:
    // gamma 158 keV
    int binMinGammaExp = histExp->FindBin(0.15853);
    int binMaxGammaExp = histExp->FindBin(0.15887);
    // Ka
    int binMinKaExp = histExp->FindBin(0.0247);
    int binMaxKaExp = histExp->FindBin(0.0253);
    // Kb
    int binMinKbExp = histExp->FindBin(0.02833);
    int binMaxKbExp = histExp->FindBin(0.0293);
    // gamma 511 keV
    int binMin511Exp = histExp->FindBin(0.5108);
    int binMax511Exp = histExp->FindBin(0.511); 
    // gamma 861 keV
    int binMin861Exp = histExp->FindBin(0.86108);
    int binMax861Exp = histExp->FindBin(0.86142);
    // gamma 1004 keV
    int binMin1004Exp = histExp->FindBin(1.00448);
    int binMax1004Exp = histExp->FindBin(1.00484);

    // Calculate the area under each photopeak
    // Simulated:
    double area_GammaSim = histRes->Integral(binMinGamma, binMaxGamma);
    double area_KaSim = histRes->Integral(binMinKa, binMaxKa);
    double area_KbSim = histRes->Integral(binMinKb, binMaxKb);
    double area_511Sim = histRes->Integral(binMin511, binMax511);
    double area_861Sim = histRes->Integral(binMin861, binMax861);
    double area_1004Sim = histRes->Integral(binMin1004, binMax1004);
    // Experimental:
    double area_GammaExp = histExp->Integral(binMinGammaExp, binMaxGamma);
    double area_KaExp = histExp->Integral(binMinKaExp, binMaxKaExp);
    double area_KbExp = histExp->Integral(binMinKbExp, binMaxKbExp);
    double area_511Exp = histExp->Integral(binMin511Exp, binMax511Exp);
    double area_861Exp = histExp->Integral(binMin861Exp, binMax861Exp);
    double area_1004Exp = histExp->Integral(binMin1004Exp, binMax1004Exp);

    // Calculate Sim/Exp peak area ratio
    double ratio_Gamma, ratio_Ka, ratio_Kb, ratio_511, ratio_861, ratio_1004;
    ratio_Gamma = area_GammaSim/area_GammaExp;
    ratio_Ka = area_KaSim/area_KaExp;
    ratio_Kb = area_KbSim/area_KbExp;
    ratio_511 = area_511Sim/area_511Exp;
    ratio_861 = area_861Sim/area_861Exp;
    ratio_1004 = area_1004Sim/area_1004Exp;

    cout << "Sim/Exp peak area ratio for: " << lab << "\n" << endl;
    cout << "Ka: \t\t " << ratio_Ka << endl;
    cout << "Kb: \t\t " << ratio_Kb << endl;
    cout << "158 keV: \t " << ratio_Gamma << endl;
    cout << "511 keV: \t " << ratio_511 << endl;
    cout << "861 keV: \t " << ratio_861 << endl;
    cout << "1004 keV: \t " << ratio_1004 << endl;
    cout << "## ------------------------------------- ##\n" << endl;
}

void Run(){
    PlotBothNorm("../data-files_HPGe/output_Ebeam32_18mm.root", "../data-files_HPGe/Ebeam=3.2MeV_116Sn-C3_Decay_HPGe_BgRemoved_Merged.txt");
    PlotBothNorm("../data-files_HPGe/output_Ebeam39_18mm.root", "../data-files_HPGe/Ebeam=3.9MeV_116Sn-D4_Decay_HPGe_BgRemoved_Merged.txt");
    PlotBothNorm("../data-files_HPGe/output_Ebeam43_18mm.root", "../data-files_HPGe/Ebeam=4.3MeV_116Sn-G1_Decay_HPGe_BgRemoved_Merged.txt");
    PlotBothNorm("../data-files_HPGe/output_Ebeam47_18mm.root", "../data-files_HPGe/Ebeam=4.7MeV_116Sn-D8_Decay_HPGe_BgRemoved_Merged.txt");
    PlotBothNorm("../data-files_HPGe/output_Ebeam50_18mm.root", "../data-files_HPGe/Ebeam=5.0MeV_116Sn-D5_Decay_HPGe_BgRemoved_Merged.txt");

}