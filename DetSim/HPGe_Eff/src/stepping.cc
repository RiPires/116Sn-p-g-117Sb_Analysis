#include "stepping.hh"
#include "G4SystemOfUnits.hh"

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

    // Define energy deposit threshold
    G4double edepThreshold = 10. * keV;

    // Get the energy deposit of this step
    G4double edep = step->GetTotalEnergyDeposit(); 

    // Inicializes an instance of the AnalysisManager
    G4AnalysisManager *man = G4AnalysisManager::Instance();

    // Add the energy deposit if it exceeds the threshold
    if (edep > edepThreshold)
    {
        EventAction->AddEdep(edep);
            
        // Fills tuple for energy deposition in the step
        man->FillNtupleDColumn(0, 1, edep);
        man->AddNtupleRow(1); 
    }
}
