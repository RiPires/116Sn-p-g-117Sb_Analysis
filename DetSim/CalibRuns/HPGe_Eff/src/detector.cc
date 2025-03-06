#include "detector.hh"

// Sensitive detector constuctor and destructor  //
MySensitiveDetector::MySensitiveDetector(G4String name) : G4VSensitiveDetector(name)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

//  Creates a Hit when a step takes place in a definded sensitive logical detector
//  in a user sensitive detector function called ProcessHits(...)
G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{ 
    G4StepPoint *preStepPoint = aStep->GetPreStepPoint();
    G4ThreeVector hitPos = preStepPoint->GetPosition();

    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->FillNtupleDColumn(1, 0, hitPos[0]); // The x position
    man->FillNtupleDColumn(1, 1, hitPos[1]); // The y position
    man->FillNtupleDColumn(1, 2, hitPos[2]); // The z position
    man->AddNtupleRow(1);
    
    return true; //Because it's a Boolean, ProcessHits function expects a return
                // better to be True
}