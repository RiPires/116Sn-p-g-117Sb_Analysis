#include <iostream>
#include <string>
#include <TSystem.h>
#include "PlotAndFit.C"
#include <vector>
using std::vector; 
using namespace std;

void PlotAll(int index) {

    // Vector to save detector efficiencies for each energy
    vector<double> detEffs;

    for (int i = 0; i<= index; ++i) {

        // Prepare filename string combining "output" and the index of the file
        std::string filename = "output" + std::to_string(i) + ".root";
        std::cout << "Plotting file: " << filename << std::endl;

        // Prepare the ROIs for each file base on the index
        double fitMin, fitMax;
        fitMin = (i*5+5-3)/1000.; // 5 is the minimum energy in keV, -1 to get i keV before, and /1000 to convert to MeV
        fitMax = (i*5+5+2)/1000.;

        // Call the PlotAndFit function with the filename
        double detEff; // variable for detector efficiency in each run
        detEff = PlotAndFit(filename.c_str(), fitMin, fitMax); // it's in %
        detEffs.push_back(detEff);
    }

    // Efficiency spectrum
    TCanvas* effCanvas = new TCanvas("effCanvas", "Absolute Efficiency", 800, 600);
    effCanvas->cd(); // set as current canvas
    auto detEffGraph = new TGraph();
    for (int i = 0; i < index; i++){
        detEffGraph->AddPoint((i*5+5)/1000., detEffs[i]);
    }
    detEffGraph->SetTitle("Absolute Efficiency");
    detEffGraph->GetXaxis()->SetTitle("Energy (MeV)");
    detEffGraph->GetYaxis()->SetTitle("Efficiency (%)");
    detEffGraph->Draw("AL*");
    effCanvas->Draw();
}