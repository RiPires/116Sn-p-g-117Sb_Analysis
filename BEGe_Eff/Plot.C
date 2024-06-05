#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
using namespace std;

void Plot(){

     // Open the ROOT file
     TFile *InputTFile = new TFile("add.root", "READ");
     // Check if the file is open successfully
     if (!InputTFile || InputTFile->IsZombie()){
          cout << "Error: Could not open ROOT file." << endl;
          return;} 
    
     /////////////////////////////////////////////////
     // Access the Energy Scoring tree in the file  //
     /////////////////////////////////////////////////
     TTree *ScoringTTRee = (TTree*)InputTFile->Get("Scoring");

     ////////////////////////////////////////////////////
     // Create a canvas for plotting deposited energy  //
     ////////////////////////////////////////////////////
     TCanvas* canvas = new TCanvas("canvas", "Energy Scoring", 800, 600);
     // Create a histogram
     TH1D* hist1 = new TH1D("hist", "Ge energy scoring", 100, 0, 1.8);
     // Project the variable into the histogram
     ScoringTTRee->Project("hist", "Scoring.Edep");
     // Set the histogram style and labels
     hist1->SetLineColor(kBlue);
     hist1->SetLineWidth(2);
     hist1->GetXaxis()->SetTitle("Energy (MeV)");
     hist1->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     hist1->Draw();

     // Display the canvas
     canvas->SetLogy();
     canvas->Draw();

     ////////////////////////////////////////////////
     // Access the Hist position tree in the file  //
     ////////////////////////////////////////////////
     TTree *StepsTTree = (TTree*)InputTFile->Get("Position");

     //////////////////////////////////////////////////
     // Create a canvas for plotting hit x position  //
     //////////////////////////////////////////////////
     TCanvas* canvas2 = new TCanvas("canvas2", "Hits position x ", 800, 600);
     // Create a histogram
     TH1D* hist2 = new TH1D("hist2", "Ge hits position x ", 100, -40., 40.);
     // Project the variable into the histogram
     StepsTTree->Project("hist2", "Position.xPos");
     // Set the histogram style and labels
     hist2->SetLineColor(kBlue);
     hist2->SetLineWidth(2);
     hist2->GetXaxis()->SetTitle("x (cm)");
     hist2->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     hist2->Draw();

     // Display the canvas
     canvas2->SetLogy();
     canvas2->Draw();

     //////////////////////////////////////////////////
     // Create a canvas for plotting hit y position  //
     //////////////////////////////////////////////////
     TCanvas* canvas3 = new TCanvas("canvas3", "Hits position y ", 800, 600);
     // Create a histogram
     TH1D* hist3 = new TH1D("hist3", "Ge hits position y ", 100, -40., 40.);
     // Project the variable into the histogram
     StepsTTree->Project("hist3", "Position.yPos");
     // Set the histogram style and labels
     hist3->SetLineColor(kBlue);
     hist3->SetLineWidth(2);
     hist3->GetXaxis()->SetTitle("y (cm)");
     hist3->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     hist3->Draw();

     // Display the canvas
     canvas3->SetLogy();
     canvas3->Draw();


     ///////////////////////////////////////////////////////
     // Create a canvas for plotting hit x vs y position  //
     ///////////////////////////////////////////////////////

    // Variables to hold the data
    float xPos = 0, yPos = 0;
    // Set the branches
    StepsTTree->SetBranchAddress("xPos", &xPos);
    StepsTTree->SetBranchAddress("yPos", &yPos);
    
    // Create a canvas for plotting hit x vs y position
    TCanvas* canvas4 = new TCanvas("canvas4", "Hits position x vs y ", 800, 600);
    // Create a histogram
    TH2F* hist4 = new TH2F("hist4", "Ge hits position x vs y ", 100, -5., 5., 100, -5., 5.);
    
    // Fill the histogram
    Long64_t nEntries = StepsTTree->GetEntries();
    for (Long64_t i = 0; i < nEntries; ++i) {
        StepsTTree->GetEntry(i);

        // Debug output to verify data
        cout << "Entry " << i << ": xPos = " << xPos << ", yPos = " << yPos << endl;

        // Fill histogram only if xPos and yPos are not zero
        if (xPos != 0 || yPos != 0) {
            hist4->Fill(xPos, yPos);
        }
    }
    
    // Set the histogram style and labels
    hist4->GetXaxis()->SetTitle("x (cm)");
    hist4->GetYaxis()->SetTitle("y (cm)");
    hist4->Draw("COLZ");
    
    // Display the canvas
    canvas4->Draw();


}
