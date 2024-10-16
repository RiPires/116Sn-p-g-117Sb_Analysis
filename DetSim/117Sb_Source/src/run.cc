#include "run.hh"

MyRunAction::MyRunAction()
{
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    
    // Creates Tuple for Energy Scoring in Ge detector
    man->CreateNtuple("ScoringGe", "ScoringGe");
    man->CreateNtupleDColumn("EdepGe");
    man->FinishNtuple(0);

    // Tuples for stepp in Ge detector
    man->CreateNtuple("StepsGe", "StepsGe");
    man->CreateNtupleDColumn("edepGe");
    man->CreateNtupleDColumn("hitPosZ");
    man->FinishNtuple(1);

    // Creates Tuple for Energy Scoring in Si detector
    man->CreateNtuple("ScoringSi", "ScoringSi");
    man->CreateNtupleDColumn("EdepSi");
    man->FinishNtuple(2);

    // Tuples for stepp in Si detector
    man->CreateNtuple("StepsSi", "StepsSi");
    man->CreateNtupleDColumn("edepSi");
    man->CreateNtupleDColumn("hitPosZ");
    man->FinishNtuple(3);
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
