#include "messenger.hh"
#include "generator.hh"

MyPrimaryGeneratorMessenger::MyPrimaryGeneratorMessenger(MyPrimaryGenerator* generator)
: fGenerator(generator)
{
    fSetGeneratorTypeCmd = new G4UIcmdWithAString("/generator/setGeneratorType", this);
    fSetGeneratorTypeCmd->SetGuidance("Set generator type (gamma or ion)");
    fSetGeneratorTypeCmd->SetParameterName("generatorType", false);
    fSetGeneratorTypeCmd->AvailableForStates(G4State_PreInit, G4State_Idle);
}

MyPrimaryGeneratorMessenger::~MyPrimaryGeneratorMessenger()
{
    delete fSetGeneratorTypeCmd;
}

void MyPrimaryGeneratorMessenger::SetNewValue(G4UIcommand* command, G4String newValue)
{
    if (command == fSetGeneratorTypeCmd)
    {
        fGenerator->SetGeneratorType(newValue);
    }
}
