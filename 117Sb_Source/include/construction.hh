#ifndef CONSTRUCTION_HH
#define CONSTRUCTION_HH

#include "G4SystemOfUnits.hh"
#include "G4VUserDetectorConstruction.hh"
#include "G4UImanager.hh"
#include "G4VPhysicalVolume.hh"
#include "G4LogicalVolume.hh"
#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4PVPlacement.hh"
#include "G4NistManager.hh"
#include "G4GenericMessenger.hh"
#include "G4SubtractionSolid.hh"

#include "detector.hh"


class MyDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    MyDetectorConstruction();
    ~MyDetectorConstruction();
    
    G4LogicalVolume *GetScoringVolume() const { return ScoringVolume;}
    G4LogicalVolume *GetScoringSi() const { return ScoringSi;}
    
    virtual G4VPhysicalVolume *Construct();
    virtual void ConstructSDandField();
    
private:
    
    ///G4double *xWorld, *yWorld, *zWorld; 
    G4Box *solidWorld, *solidFrame;
    G4Tubs *solidWindow, *solidWinBe, *solidDetector, *solidDetSi, *solidCase;
    G4LogicalVolume  *logicWorld, *logicWindow, *logicWinBe, *logicDetector, *logicDetSi, *logicCase;
    G4VPhysicalVolume *physWorld, *physWindow, *physWinBe, *physDetector, *physDetSi, *physCase;
    
    G4GenericMessenger *fMessenger;
    
    G4Material *Epoxy, *caseMat, *worldMat, *detMatGe, *detMatSi, *winBe;
    G4Element *Be, *Al, *Si, *Ge;
    
    void DefineMaterial();
    
    G4LogicalVolume *ScoringVolume;
    G4LogicalVolume *ScoringSi;  
};

#endif



