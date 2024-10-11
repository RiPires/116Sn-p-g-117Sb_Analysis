#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "TH1D.h"
#include "TCanvas.h"

using namespace std;
void PlotSpectrumAndOverlay() {
    // Open the data file
    std::ifstream infile("Run03_152Eu_detGe_50mm.mca");  // Replace "datafile.txt" with your actual file name

    if (!infile.is_open()) {
        std::cerr << "Error: Could not open the file!" << std::endl;
        return;
    }

    // Read the file and skip the first 15 lines
    std::string line;
    for (int i = 0; i < 15; i++) {
        std::getline(infile, line);
    }

    // Vector to store data values (from the <<DATA>> section)
    std::vector<double> dataValues;

    // Now read the spectrum data starting from line 15
    double value;
    while (infile >> value) {
        dataValues.push_back(value);
    }

    // Find the maximum value in dataValues
    double maxYield = *max_element(dataValues.begin(), dataValues.end());
    cout << "Maximum yield = " << maxYield << endl;

    infile.close();  // Close the file after reading

    // Create a histogram for the data from the file
    int numBins = dataValues.size();
    TH1D* hist2 = new TH1D("hist2", "Spectrum from File", numBins, 0, numBins);

    // Fill the histogram with the NORMALIZED data values
    for (int i = 0; i < numBins; i++) {
        hist2->SetBinContent(i + 1, dataValues[i]/maxYield);  // ROOT histograms are 1-indexed
    }

    // Set histogram style for hist2
    hist2->SetLineColor(kRed);
    hist2->SetLineWidth(2);
    hist2->GetXaxis()->SetTitle("Channel");
    hist2->GetYaxis()->SetTitle("Counts");

    // Create a canvas to plot both histograms
    TCanvas* canvas = new TCanvas("canvas", "Overlay of Histograms", 800, 600);

    // Draw the new histogram (hist2) on the same canvas
    hist2->Draw("HIST SAME");  // "SAME" option to overlay histograms

    // Update the canvas to display the plot
    canvas->SetLogy();
    canvas->Update();
}

