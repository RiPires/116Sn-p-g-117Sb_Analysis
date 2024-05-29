#include "generator.hh"

//   Primary particle generator constuctor and destructor   //
MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4ParticleGun(1);
    
    G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
    G4String particleName="geantino"; // Sets prim .particle as GEANTINO
    G4ParticleDefinition *particle = particleTable->FindParticle("geantino"); 
    
    G4ThreeVector pos(0.,0.,-19.5*mm+100*nm); //  Position for particle gun
    G4ThreeVector mom(0.,0.,1.);     //  Momentum direction vector for prim. particle
    
    fParticleGun->SetParticlePosition(pos);          // Particle Position
    fParticleGun->SetParticleMomentumDirection(mom); // Particle Momentum Direction
    fParticleGun->SetParticleMomentum(0.*keV);       // Particle Momentum magnitude
    fParticleGun->SetParticleDefinition(particle);   // Sets particle as GEANTINO prev. deffined
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
        // 152Eu source //
        G4int Z = 63;
        G4int A = 152;
        
        G4double charge = 0.;
        G4double energy = 0.;
        
        G4ParticleDefinition *ion = G4IonTable::GetIonTable()->GetIon(Z, A, energy);
        
        fParticleGun->SetParticleDefinition(ion);
        fParticleGun->SetParticleCharge(charge);
    }

    fParticleGun->GeneratePrimaryVertex(anEvent);
}