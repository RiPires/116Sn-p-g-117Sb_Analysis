#include "generator.hh"
#include "Randomize.hh"
#include "G4RandomDirection.hh"
#include "G4IonTable.hh"
#include "messenger.hh"

//  Primary particle generator constuctor and destructor  //
MyPrimaryGenerator::MyPrimaryGenerator()
{
    fParticleGun = new G4GeneralParticleSource();
    fGeneratorType = 'gamma'; // set default generator type as gamma
    fMessenger = new MyPrimaryGeneratorMessenger(this); // initialize messenger
    
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
    delete fMessenger;
}

// Set generator type based on user input from macro
void MyPrimaryGenerator::SetGeneratorType(const G4String& genType)
{
    fGeneratorType = genType;
}

//  Generate primary particle  //
void MyPrimaryGenerator::GeneratePrimaries(G4Event *anEvent)
{   
    if (fGeneratorType == 'gamma')
    {
        // Gamma generator
        G4ParticleDefinition *particle = fParticleGun->GetParticleDefinition();
    
        if(particle == G4Geantino::Geantino())
        {   
            G4ParticleTable *particleTable = G4ParticleTable::GetParticleTable();
            G4ParticleDefinition *gamma = particleTable->FindParticle("gamma");
            fParticleGun->SetParticleDefinition(gamma);
            G4ThreeVector direction = G4RandomDirection();
            //fParticleGun->SetParticleMomentumDirection(direction); 
        }
    } 
    else if (fGeneratorType == 'ion')
    {
        // Ion generator (152Eu source)
        G4ParticleDefinition *particle = fParticleGun->GetParticleDefinition();
        
        if (particle == G4Geantino::Geantino())
        {
            G4int Z = 63;  // Atomic number of Eu
            G4int A = 152; // Mass number of 152Eu
            G4double energy = 0.;
            G4double charge = 0.;
            
            G4ParticleDefinition *ion = G4IonTable::GetIonTable()->GetIon(Z, A, energy);
            fParticleGun->SetParticleDefinition(ion);
            fParticleGun->SetParticleCharge(charge);
        }
    }

    // Generate the primary even
    fParticleGun->GeneratePrimaryVertex(anEvent);
}