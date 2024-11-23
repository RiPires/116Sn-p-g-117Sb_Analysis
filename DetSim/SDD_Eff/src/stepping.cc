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
    if(volume != ScoringVolume){
        return; // do nothing  
    } 
    else{
        // Get step details
        G4Track *track = step->GetTrack();

        // Get parent ID (origin)
        G4int parentID = track->GetParentID();

        // Get particle name
        G4String particleName = track->GetDefinition()->GetParticleName();

        // Get particle kinetic energy
        G4double energy = track->GetKineticEnergy();

        // Get the energy deposit of this step
        G4double edep = step->GetTotalEnergyDeposit(); 

        if (particleName == "e-" && parentID <= 2 && edep > 20. * keV)
        {   track->SetTrackStatus(fStopAndKill);
            EventAction->AddEdep(0.);}

        else{
            // Adds it to the total energy deposited in the event
            EventAction->AddEdep(edep);

            // Push back particleName, parentID and deposited energy to vectors for print out
            EventAction->AddParticleTypeAndEdep(particleName, edep, parentID);}
    }
}
