#include "physics.hh"

MyPhysicsList::MyPhysicsList()
{
    //   ElectroMagnetic Standard Physiscs Lists
    RegisterPhysics (new G4EmStandardPhysics()); 
    //   Radioactive Decay Physics Lists
    RegisterPhysics (new G4DecayPhysics());
    RegisterPhysics (new G4RadioactiveDecayPhysics());
}

MyPhysicsList::~MyPhysicsList()
{}