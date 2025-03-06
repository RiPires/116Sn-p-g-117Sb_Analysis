#include "physics.hh"
#include "G4RegionStore.hh"
#include "G4ProductionCuts.hh"
#include "G4Electron.hh"
#include "G4Gamma.hh"
#include "G4SystemOfUnits.hh"

MyPhysicsList::MyPhysicsList()
{
    //  ElectroMagnetic Standard Physiscs Lists
    RegisterPhysics (new G4EmStandardPhysics()); 
    //  Radioactive Decay Physics Lists
    RegisterPhysics (new G4DecayPhysics());
    RegisterPhysics (new G4RadioactiveDecayPhysics());
}

MyPhysicsList::~MyPhysicsList()
{}