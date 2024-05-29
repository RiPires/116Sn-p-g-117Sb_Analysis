#include "detector.hh"

// Sensitive detector constuctor and destructor   //
MySensitiveDetector::MySensitiveDetector(G4String name) : G4VSensitiveDetector(name)
{}

MySensitiveDetector::~MySensitiveDetector()
{}

//   Creates a Hit when a step takes place in a definded sensitive logical detector
// in a user sensitive detector function called ProcessHits(...)
G4bool MySensitiveDetector::ProcessHits(G4Step *aStep, G4TouchableHistory *ROhist)
{ 

    return true; //Because it's a Boolean, ProcessHits function expects a return
                // better to be True
}


/*
00084   protected: // with description
00085       virtual G4bool ProcessHits(G4Step*aStep,G4TouchableHistory*ROhist) = 0;
00086       //  The user MUST implement this method for generating hit(s) using the 
00087       // information of G4Step object. Note that the volume and the position
00088       // information is kept in PreStepPoint of G4Step.
00089       //  Be aware that this method is a protected method and it sill be invoked 
00090       // by Hit() method of Base class after Readout geometry associated to the
00091       // sensitive detector is handled.
00092       //  "ROhist" will be given only is a Readout geometry is defined to this
00093       // sensitive detector. The G4TouchableHistory object of the tracking geometry
00094       // is stored in the PreStepPoint object of G4Step.*/