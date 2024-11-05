#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <dirent.h>

using namespace std;

void MergeBg(std::string dir){

    DIR* dp = opendir(dir.c_str());

    // Check if directory is valid
    if (dp == nullptr){
        cerr << "Error: Could not open directory" << endl;
        return;
    }

    // Vector to store merged yield
    std::vector<double> mergeYield;

    // Loop over files inside dp
    struct dirent *file;
    while ((file = readdir(dp)) != nullptr){
        std::string filename = file->d_name;

        // Ignore "." and ".." entries
        if (filename != "." && filename != ".."){
            cout << "File: " << filename << endl;

            // Open the data file
            std::ifstream infile(filename);

            // Check if the file was opened
            if (!infile.is_open()) {
                std::cerr << "Error: Could not open the file!" << std::endl;
                return;
            }
            // Read the file and skip the first 15 lines
            std::string line;
            for (int i = 0; i < 14; i++){
                std::getline(infile, line);
            }

            // Vector to store data values
            std::vector<double> dataValues;

            // Now read the spectrum data starting from line 15
            double value;
            while (infile >> value){
                dataValues.push_back(value);
            }
            infile.close();
            
            cout << dataValues.size() << endl;
            for (int i = 0; i < dataValues.size(); i++){
                cout << dataValues[i] << endl;
            }

            // Energy calibration
            double slope = 0.0003225; // MeV/ch

            // Histogram
            int nrBins = dataValues.size();
            TH1D *hist_bg = new TH1D("hist_bg", "HPGe Background Rate", nrBins, 0, nrBins*slope);

            // Time of acquisition
            double t_acqui = 900; // seconds

            // Fill the histigram with background rate values, energy calibrated
            for (int i = 0; i < nrBins; i++){
                double energy = (i+0.5) * slope;
                hist_bg->SetBinContent(hist_bg->FindBin(energy), dataValues[i]/t_acqui);
            }

            // Set histogram style
            hist_bg->SetLineColor(kBlack);
            hist_bg->SetLineWidth(2);
            hist_bg->GetXaxis()->SetTitle("Energy (MeV)");
            hist_bg->GetYaxis()->SetTitle("Rate (s^{-1})");

            // Create canvas
            TCanvas *canvas = new TCanvas("canvas", "HPGe background rate", 800, 600);

            // Draw the histogram
            hist_bg->Draw();
            canvas->SetLogy();
            canvas->Update();
        }
    }
    closedir(dp);
    return;
}