#ifndef MESSENGER_HH
#define MESSENGER_HH

#include "G4UImessenger.hh"
#include "G4UIcmdWithAString.hh"
#include "generator.hh"

class MyPrimaryGeneratorMessenger : public G4UImessenger
{
private:
    MyPrimaryGenerator* fGenerator;
    G4UIcmdWithAString* fSetGeneratorTypeCmd;

public:
    MyPrimaryGeneratorMessenger(MyPrimaryGenerator *generator):fGenerator(generator)
    {
        fSetGeneratorTypeCmd = new G4UIcmdWithAString("/generator/setGeneratorType", this);
        fSetGeneratorTypeCmd->SetGuidance("Set generator type (gamma or ion)");
        fSetGeneratorTypeCmd->SetParameterName("generatorType", false);
        fSetGeneratorTypeCmd->AvailableForStates(G4State_PreInit, G4State_Idle);
    }

    ~MyPrimaryGeneratorMessenger()
    {
        delete fSetGeneratorTypeCmd;
    }

    virtual void SetNewValue(G4UIcommand* command, G4String newValue)
    {
        if (command == fSetGeneratorTypeCmd)
        {
            fGenerator->SetGeneratorType(newValue);
        }
    }

};
#endif