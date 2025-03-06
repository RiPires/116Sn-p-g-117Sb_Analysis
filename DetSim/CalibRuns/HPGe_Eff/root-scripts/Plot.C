#include "TFile.h"
#include "TTree.h"
#include <iostream>
#include "TH2.h"
#include <cmath>
#include "TF1.h"
using namespace std;

void Plot(const char* filename){

     // Open the ROOT file
     TFile *InputTFile = new TFile(filename, "READ");
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
     TH1D* hist1 = new TH1D("hist", "Ge energy scoring", 4096, 0, 1.320);
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
     gPad->Update();

     ////////////////////////////////////////////////////
     // Create a canvas for plotting energy deposits  //
     ////////////////////////////////////////////////////
     TCanvas* canvasEdep = new TCanvas("canvasEdep", "Energy Deposits", 800, 600);
     // Create a histogram
     TH1D* histEdep = new TH1D("histEdep", "Ge energy deposits", 4096, 0, 1.320);
     // Project the variable into the histogram
     ScoringTTRee->Project("histEdep", "Scoring.edep");
     // Set the histogram style and labels
     histEdep->SetLineColor(kBlue);
     histEdep->SetLineWidth(2);
     histEdep->GetXaxis()->SetTitle("Energy (MeV)");
     histEdep->GetYaxis()->SetTitle("Counts");
     // Draw the histogram on the canvas
     histEdep->Draw();
     // Display the canvas
     canvasEdep->SetLogy();
     canvasEdep->Draw();
     gPad->Update();

    ////////////////////////////////////////////////
    // Access the Hits position tree in the file  //
    ////////////////////////////////////////////////
    TTree *StepsTTree = (TTree*)InputTFile->Get("Position");

    //////////////////////////////////////////////////
    // Create a canvas for plotting hit z position  //
    //////////////////////////////////////////////////
    TCanvas* canvasZ = new TCanvas("canvasZ", "Hits position z ", 800, 600);
    // Create a histogram
    TH1D* histZ = new TH1D("histZ", "Ge hits position z ", 100, 0., 100.);
    // Project the variable into the histogram
    StepsTTree->Project("histZ", "Position.zPos");
    // Set the histogram style and labels
    histZ->SetLineColor(kBlue);
    histZ->SetLineWidth(2);
    histZ->GetXaxis()->SetTitle("z (cm)");
    histZ->GetYaxis()->SetTitle("Counts");
    // Draw the histogram on the canvas
    histZ->Draw();
    // Display the canvas
    canvasZ->SetLogy();
    canvasZ->Draw();
    gPad->Update();

    ///////////////////////////////////////////////////////
    // Create a canvas for plotting hit x vs y position  //
    ///////////////////////////////////////////////////////
    // Variables to hold the data
    double xPos = 0., yPos = 0.;
    // Set the branches
    StepsTTree->SetBranchAddress("xPos", &xPos);
    StepsTTree->SetBranchAddress("yPos", &yPos);
    // Create a canvas for plotting hit x vs y position
    TCanvas* canvas4 = new TCanvas("canvas4", "Hits position x vs y ", 800, 600);
    // Create a histogram
    TH2F* hist4 = new TH2F("hist4", "Ge hits position x vs y ", 100, -30., 30., 100, -30., 30.);
    // Fill the histogram
    Long64_t nEntries = StepsTTree->GetEntries();
    for (Long64_t i = 0; i < nEntries; ++i) {
        StepsTTree->GetEntry(i);
        // Fill histogram only if xPos and yPos are not zero
        if (xPos != 0 || yPos != 0) {
            // Debug output to verify data
            //cout << "Entry " << i << ": " << "xPos = " << xPos << " | yPos = " << yPos << endl;
            hist4->Fill(xPos, yPos);
        }
    }   
    // Set the histogram style and labels
    hist4->GetXaxis()->SetTitle("x (cm)");
    hist4->GetYaxis()->SetTitle("y (cm)");
    hist4->Draw("COLZ");
    // Display the canvas
    canvas4->Draw();
    gPad->Update();
}   