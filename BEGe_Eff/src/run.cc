#include "run.hh"

MyRunAction::MyRunAction()
{
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    
    // Creates Tuple for Energy Scoring info.
    man->CreateNtuple("Scoring", "Scoring");
    man->CreateNtupleDColumn("Edep");
    man->FinishNtuple(0);

    // Tuples for stepp info.
    man->CreateNtuple("Steps", "Steps");
    man->CreateNtupleDColumn("edep");
    man->FinishNtuple(1);
}

MyRunAction::~MyRunAction()
{}

void MyRunAction::BeginOfRunAction(const G4Run* run)
{
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    
    // Get Run Identification number as integer
    G4int runID = run->GetRunID();
    // Turn it into string
    std::stringstream strRunID;
    strRunID << runID;
    
    // Opens output ".root" file w/ Run identification number 
    man->OpenFile("output"+strRunID.str()+".root");
}

void MyRunAction::EndOfRunAction(const G4Run*)
{    
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();

    // Writes data in the Tuples at the end of the run
    // and closes the output file 
    man->Write();
    man->CloseFile();
}
