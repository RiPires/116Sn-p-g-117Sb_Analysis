#include "generator.hh"
#include "Randomize.hh"
#include "G4RandomDirection.hh"
#include "G4IonTable.hh"

//  Primary particle generator constuctor and destructor  //
MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4GeneralParticleSource();

    // Set default particle to geantino
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition *particle = particleTable->FindParticle("geantino"); 
    G4ThreeVector pos(0.,0.,0.);                    // Position for particle gun
    fParticleGun->SetParticlePosition(pos);         // Particle Position
    fParticleGun->SetParticleDefinition(particle);  // Sets particle as GEANTINO prev. deffined
}

MyPrimaryGenerator::~MyPrimaryGenerator()
{
    delete fParticleGun;
}

//  Generate primary particle  //
void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{   
    // Gamma generator by default
    G4ParticleDefinition *particle = fParticleGun->GetParticleDefinition();

    if(particle == G4Geantino::Geantino())
    {   
        G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
        G4ParticleDefinition *gamma = particleTable->FindParticle("gamma");
        fParticleGun->SetParticleDefinition(gamma);
        G4ThreeVector direction = G4RandomDirection();
        //fParticleGun->SetParticleMomentumDirection(direction); 
    }
    
    // Generate the primary even
    fParticleGun->GeneratePrimaryVertex(anEvent);
}