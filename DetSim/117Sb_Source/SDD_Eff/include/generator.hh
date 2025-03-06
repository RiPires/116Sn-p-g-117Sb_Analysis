#ifndef GENERATOR_HH
#define GENERATOR_HH

#include "G4VUserPrimaryGeneratorAction.hh"
#include "G4ParticleGun.hh"
#include "G4GeneralParticleSource.hh"
#include "G4SystemOfUnits.hh"
#include "G4ParticleTable.hh"
#include "G4Geantino.hh"
#include "G4IonTable.hh"

class MyPrimaryGenerator : public G4VUserPrimaryGeneratorAction
{
//  Primary particle generator constuctor and destructor  //
public:
    MyPrimaryGenerator();
    ~MyPrimaryGenerator();
    
    virtual void GeneratePrimaries(G4Event*);

    void SetGunPosition(G4double position);
    void UpdateSourcePosition(G4double position);

    G4double GetSourcePosition() const { return fSourcePosition; }

private:
    G4GeneralParticleSource *fParticleGun;
    G4double fSourcePosition;
};
#endif