#include "messenger.hh"
#include "construction.hh"

DetectorMessenger::DetectorMessenger(MyDetectorConstruction* det)
    : detector(det) {
    // Create the command for setting the source position
    setSourcePositionCmd = new G4UIcmdWithADoubleAndUnit("/detector/setSourcePosition", this);
    setSourcePositionCmd->SetGuidance("Set the position of the source.");
    setSourcePositionCmd->SetParameterName("position", false);
    setSourcePositionCmd->SetUnitCategory("Length");
    setSourcePositionCmd->AvailableForStates(G4State_PreInit, G4State_Idle);

    // Create the command for setting the Sn target thickness
    setSnThicknessCmd = new G4UIcmdWithADoubleAndUnit("/detector/setSnThickness", this);
    setSnThicknessCmd->SetGuidance("Set the Sn target thickness.");
    setSnThicknessCmd->SetParameterName("SnTargetThickness", false);
    setSnThicknessCmd->SetUnitCategory("Length");
    setSnThicknessCmd->AvailableForStates(G4State_PreInit, G4State_Idle);

    // Create the command for setting the Sn target thickness
    setAlThicknessCmd = new G4UIcmdWithADoubleAndUnit("/detector/setAlThickness", this);
    setAlThicknessCmd->SetGuidance("Set the Al layer thickness.");
    setAlThicknessCmd->SetParameterName("SnTargetThickness", false);
    setAlThicknessCmd->SetUnitCategory("Length");
    setAlThicknessCmd->AvailableForStates(G4State_PreInit, G4State_Idle);
}

DetectorMessenger::~DetectorMessenger() {
    delete setSourcePositionCmd; // Cleanup allocated memory
    delete setSnThicknessCmd;
    delete setAlThicknessCmd;
}

void DetectorMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if (command == setSourcePositionCmd) {
        G4double newPos = setSourcePositionCmd->GetNewDoubleValue(newValue);
        detector->SetSourcePosition(newPos);  // Update the source position   
    }

    if (command == setSnThicknessCmd) {
        G4double newThick = setSnThicknessCmd->GetNewDoubleValue(newValue);
        detector->SetSnThickness(newThick);  // Update the Sn target thickness
    }

    if (command == setAlThicknessCmd) {
        G4double newThick = setAlThicknessCmd->GetNewDoubleValue(newValue);
        detector->SetAlThickness(newThick);  // Update the Al layer thickness
    }
    G4RunManager::GetRunManager()->GeometryHasBeenModified(); 
}