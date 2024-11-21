#include <iostream>
#include "TF1.h"

using namespace std;

// Funtion to perform gaussian fit and extract fit parameters
vector<double> FitPeak(TH1D *hist, const vector<double> &fitMin, const vector<double> &fitMax) {

    //cout << "Fitting peaks for histogram: " << hist->GetName() << endl;

    // Vectors to store fit parameters
    vector<double> cents;
    vector<double> sigmas;
    vector<double> integrals; 
    // Loop over each ROI
    for (size_t i = 0; i < fitMin.size(); ++i){
        
        double ROId = fitMin[i];
        double ROIu = fitMax[i];

        // Define Gaussian fit function
        string fitName = "gausFit" + to_string(i);
        TF1 *gaussFit = new TF1(fitName.c_str(), "gaus", ROId, ROIu);

        // Perform the fit
        hist->Fit(gaussFit, "RQ"); // R = Range, Q = Quiet mode

        // Extract fit parameters
        double centroid = gaussFit->GetParameter(1);        // Mean (centroid)
        double sigma = gaussFit->GetParameter(2);           // Standard deviation
        double amplitude = gaussFit->GetParameter(0);       // Amplitude
        double integral = amplitude * sigma * sqrt(2*M_PI); // Integral

        // Push back to output vectors
        cents.push_back(centroid);
        sigmas.push_back(sigma);
        integrals.push_back(integral);

        // Print results
        //cout << "Peak " << i+1 << " results:" << endl;
        //cout << "Centroid: " << centroid << " MeV" << endl;
        //cout << "Sigma: " << sigma << " MeV" << endl;
        //cout << "Integral: " << integral << " counts" << endl;
        //cout << "-----------------\n" << endl;
    }
    return integrals;
}