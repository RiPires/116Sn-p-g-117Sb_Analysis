#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "G4GeneralParticleSource.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"
#include "G4Geantino.hh"
#include "G4IonTable.hh"

#include "messenger.hh"

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
//  Primary particle generator constuctor and destructor  //
public:
    MyPrimaryGenerator();
    ~MyPrimaryGenerator();
    
    virtual void GeneratePrimaries(G4Event*);

    // Macro command to set the generator type
    void SetGeneratorType(const G4String& genType);

private:
    G4GeneralParticleSource *fParticleGun;
    G4String fGeneratorType; // to track the generator type
    MyPrimaryGeneratorMessenger *fMessenger;
};
#endif