#include "Randomize.hh"
#include "G4RandomDirection.hh"
#include "G4IonTable.hh"
#include "G4RunManager.hh"

#include "generator.hh"
#include "construction.hh"

//  Primary particle generator constuctor //
MyPrimaryGenerator::MyPrimaryGenerator() {
    MyDetectorConstruction* detector =
        const_cast<MyDetectorConstruction*>(static_cast<const MyDetectorConstruction*>(G4RunManager::GetRunManager()->GetUserDetectorConstruction()));

    fParticleGun = new G4GeneralParticleSource();

    // Get initial source position from the detector
    fSourcePosition = detector->GetSourcePosition();
    fParticleGun->SetParticlePosition(G4ThreeVector(-0.56*mm, 1.03*mm, fSourcePosition));  // Set initial particle position
    G4cout << "Primary generator initialized at position: " << fSourcePosition / mm << " mm" << G4endl;

    // Set default particle type to geantino
    G4ParticleTable* particleTable = G4ParticleTable::GetParticleTable();
    G4ParticleDefinition* particle = particleTable->FindParticle("geantino");
    fParticleGun->SetParticleDefinition(particle);
}

// Destructor
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

void MyPrimaryGenerator::SetGunPosition(G4double position) {
    fParticleGun->SetParticlePosition(G4ThreeVector(0., 0., position));
}

void MyPrimaryGenerator::UpdateSourcePosition(G4double position) {
    fSourcePosition = position;  // Update the internal source position
    fParticleGun->SetParticlePosition(G4ThreeVector(0., 0., position));  // Set particle gun position
    G4cout << "Primary generator source position updated to: " << position / mm << " mm" << G4endl;
}