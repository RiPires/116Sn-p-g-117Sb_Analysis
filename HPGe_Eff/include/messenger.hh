#ifndef MESSENGER_HH
#define MESSENGER_HH

#include "G4UImessenger.hh"
#include "G4UIcmdWithAString.hh"

class MyPrimaryGenerator;

class MyPrimaryGeneratorMessenger : public G4UImessenger
{
private:
    MyPrimaryGenerator* fGenerator;
    G4UIcmdWithAString* fSetGeneratorTypeCmd;

public:
    MyPrimaryGeneratorMessenger(MyPrimaryGenerator *generator);
    ~MyPrimaryGeneratorMessenger();

    virtual void SetNewValue(G4UIcommand* command, G4String newValue);

};
#endif