#ifndef MESSENGER_HH
#define MESSENGER_HH

#include "G4UImessenger.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"

class MyDetectorConstruction; // Forward declaration of MyDetectorConstruction

class DetectorMessenger : public G4UImessenger {
public:
    explicit DetectorMessenger(MyDetectorConstruction* det); // Constructor
    ~DetectorMessenger() override; // Destructor

    void SetNewValue(G4UIcommand* command, G4String newValue) override;

private:
    MyDetectorConstruction* detector; // Pointer to the detector construction class
    G4UIcmdWithADoubleAndUnit *setSourcePositionCmd;    // Command for setting the source position
    G4UIcmdWithADoubleAndUnit *setSnThicknessCmd;       // Command for setting the Sn Target thickness
    G4UIcmdWithADoubleAndUnit *setAlThicknessCmd;       // Command for setting the Al layer thickness
};

#endif // MESSENGER_HH
