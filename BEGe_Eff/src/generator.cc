#include "generator.hh"
#include "Randomize.hh"
#include "G4RandomDirection.hh"


//   Primary particle generator constuctor and destructor   //
MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4GeneralParticleSource();
    
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4String particleName="geantino"; // Sets prim .particle as GEANTINO
    G4ParticleDefinition *particle = particleTable->FindParticle("geantino"); 

    //G4ThreeVector pos(0.,0.,-20.);                  //  Position for particle gun
    //fParticleGun->SetParticlePosition(pos);         // Particle Position
    //fParticleGun->SetParticleMomentum(0.*MeV);      // Particle Momentum magnitude
    fParticleGun->SetParticleDefinition(particle);  // Sets particle as GEANTINO prev. deffined
}

MyPrimaryGenerator::~MyPrimaryGenerator()
{
    delete fParticleGun;
}

///   Generate primary particle as a radioactive punctual source   ///
void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{    
    G4ParticleDefinition *particle = fParticleGun->GetParticleDefinition();
    
    if(particle == G4Geantino::Geantino())
    {   
        G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
        G4ParticleDefinition *gamma = particleTable->FindParticle("gamma");
        fParticleGun->SetParticleDefinition(gamma);
        //fParticleGun->SetParticleMomentum(158.*keV);

        G4ThreeVector direction = G4RandomDirection();
        //fParticleGun->SetParticleMomentumDirection(direction); 
    }

    fParticleGun->GeneratePrimaryVertex(anEvent);
}