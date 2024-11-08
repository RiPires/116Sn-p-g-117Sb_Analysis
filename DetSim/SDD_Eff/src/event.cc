#include "event.hh"
#include "G4SystemOfUnits.hh"

MyEventAction::MyEventAction(MyRunAction*)
{   Edep = 0.;}

MyEventAction::~MyEventAction()
{}

void MyEventAction::BeginOfEventAction(const G4Event*) 
{   Edep = 0.;}

void MyEventAction::EndOfEventAction(const G4Event*)
{
    ///G4cout << "Energy deposition: " << Edep << " MeV" << G4endl;
    
    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();
    
    // Sets event energy threshold
    G4double EdepThreshold = 400. * eV;

    // Check if energy in the event is above threshold
    if (Edep > EdepThreshold)
    {
        // Fills tuple for energy deposition in the event
        // and starts new row
        man->FillNtupleDColumn(0, 0, Edep);
        man->AddNtupleRow(0); 
    }
}


