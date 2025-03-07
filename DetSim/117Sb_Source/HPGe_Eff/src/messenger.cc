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
}

DetectorMessenger::~DetectorMessenger() {
    delete setSourcePositionCmd; // Cleanup allocated memory
    delete setSourcePositionCmd;
}

void DetectorMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if (command == setSourcePositionCmd) {
        G4double newPos = setSourcePositionCmd->GetNewDoubleValue(newValue);
        detector->SetSourcePosition(newPos);  // Update both the Mylar and the source position
    }

    if (command == setSnThicknessCmd) {
        G4double newThick = setSnThicknessCmd->GetNewDoubleValue(newValue);
        detector->SetSnThickness(newThick);  // Update the Sn target thickness
    }
}






