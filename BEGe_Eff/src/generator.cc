#include "generator.hh"
#include "Randomize.hh"


//   Primary particle generator constuctor and destructor   //
MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4ParticleGun(1);
    
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4String particleName="geantino"; // Sets prim .particle as GEANTINO
    G4ParticleDefinition *particle = particleTable->FindParticle("geantino"); 

    G4ThreeVector pos(0.,0.,-20.);                  //  Position for particle gun
    fParticleGun->SetParticlePosition(pos);         // Particle Position
    fParticleGun->SetParticleMomentum(0.*MeV);      // Particle Momentum magnitude
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
        fParticleGun->SetParticleMomentum(25.*keV);
        
        // Set isotropoic distribution //
        G4double twopi = 6.28318530718;
        G4double cosTheta = -1.0 + 2.0*G4UniformRand();
        G4double phi = twopi * G4UniformRand();
        G4double sinTheta = sqrt(1 - cosTheta*cosTheta);

        //  Momentum direction vector for prim. particle
        fParticleGun->SetParticleMomentumDirection(G4ThreeVector(sinTheta*cos(phi), sinTheta*sin(phi), cosTheta)); // Particle Momentum Direction
        fParticleGun->SetParticleDefinition(gamma);
    }

    fParticleGun->GeneratePrimaryVertex(anEvent);
}