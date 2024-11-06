#include "stepping.hh"

MySteppingAction::MySteppingAction(MyEventAction *eventAction)
{
    EventAction = eventAction;
}

MySteppingAction::~MySteppingAction()
{}

void MySteppingAction::UserSteppingAction(const G4Step *step)
{
    // Gets the volume where the step is occurring
    G4LogicalVolume *volume = 
    step->GetPreStepPoint()->GetTouchableHandle()->GetVolume()->GetLogicalVolume();
    
    // Gets info. on the geometry construction
    const MyDetectorConstruction *detectorConstruction = 
    static_cast<const MyDetectorConstruction*> (G4RunManager::GetRunManager()->GetUserDetectorConstruction());

    // Gets the scoring volume from the geometric construction
    G4LogicalVolume *ScoringVolume =    detectorConstruction->GetScoringVolume();
    
    // If the 'volume' is not the SensitiveDetector
    if(volume != ScoringVolume) 
        return; // do nothing                                  

    // Get the energy deposit of this step
    G4double edep = step->GetTotalEnergyDeposit(); 
    // Adds it to the total energy deposited in the event
    EventAction->AddEdep(edep);    
}
