#include "event.hh"

MyEventAction::MyEventAction(MyRunAction*)
{   EdepGe = 0.; EdepSi = 0.;}

MyEventAction::~MyEventAction()
{}

void MyEventAction::BeginOfEventAction(const G4Event*) 
{   EdepGe = 0.; EdepSi = 0.;}

void MyEventAction::EndOfEventAction(const G4Event*)
{
    ///G4cout << "Energy deposition: " << Edep << " MeV" << G4endl;
    
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    
    // Fills tuple for energy deposition in the event
    // and starts new row
    man->FillNtupleDColumn(0, 0, EdepGe);
    man->AddNtupleRow(0); 

    man->FillNtupleDColumn(2, 0, EdepSi);
    man->AddNtupleRow(2); 
}


