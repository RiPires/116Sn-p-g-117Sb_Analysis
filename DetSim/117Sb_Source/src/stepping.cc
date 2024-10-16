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
    G4LogicalVolume *ScoringVolume = detectorConstruction->GetScoringVolume();
    G4LogicalVolume *ScoringSi = detectorConstruction->GetScoringSi();
    
    // Checks volume where interaction occurs //
    if(volume == ScoringVolume) // The Ge detector
    {
    G4double edep = step->GetTotalEnergyDeposit(); // We record the energy deposition,'edep', on the step     //
    EventAction->AddEdepGe(edep);                    // and add it to the total energy deposited in the event, 'Edep' //  

    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->FillNtupleDColumn(1, 0, edep);
    man->AddNtupleRow(1);
    }

    if(volume == ScoringSi) // The Si detector
    {
    G4double edep = step->GetTotalEnergyDeposit(); // We record the energy deposition,'edep', on the step     //
    EventAction->AddEdepSi(edep);                    // and add it to the total energy deposited in the event, 'Edep' //  

    G4AnalysisManager *man = G4AnalysisManager::Instance();
    man->FillNtupleDColumn(3, 0, edep);
    man->AddNtupleRow(3);
    }

    if(!(volume == ScoringVolume || volume == ScoringSi)){return;}
                     
    


}