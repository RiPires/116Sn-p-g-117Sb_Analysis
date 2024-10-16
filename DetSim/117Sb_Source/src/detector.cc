#include "detector.hh"

// Sensitive detector constuctor and destructor   //
MySensitiveDetector::MySensitiveDetector(G4String name):G4VSensitiveDetector(name)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

//   Creates a Hit when a step takes place in a definded sensitive logical detector
// in a user sensitive detector function called ProcessHits(...)
G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{ 
    G4StepPoint *postStepPoint = aStep->GetPostStepPoint();
    G4ThreeVector hitPos = postStepPoint->GetPosition();

    G4AnalysisManager *man = G4AnalysisManager::Instance();

    man->FillNtupleDColumn(1, 1, hitPos[2]);
    man->AddNtupleRow(1);

    return true; //Because it's a Boolean, ProcessHits function expects a return
                // better to be True
}


// Silicon sensitive detector constuctor and destructor   //
SiSensitiveDetector::SiSensitiveDetector(G4String name):G4VSensitiveDetector(name)
{}

SiSensitiveDetector::~SiSensitiveDetector()
{}

//   Creates a Hit when a step takes place in a definded sensitive logical detector
// in a user sensitive detector function called ProcessHits(...)
G4bool SiSensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{ 
    G4StepPoint *postStepPoint = aStep->GetPostStepPoint();
    G4ThreeVector hitPos = postStepPoint->GetPosition();

    G4AnalysisManager *man = G4AnalysisManager::Instance();

    man->FillNtupleDColumn(3, 1, hitPos[2]);
    man->AddNtupleRow(3);

    return true; //Because it's a Boolean, ProcessHits function expects a return
                // better to be True
}