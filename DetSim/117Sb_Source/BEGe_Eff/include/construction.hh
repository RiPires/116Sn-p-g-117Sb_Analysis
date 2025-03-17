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
#include "G4RunManager.hh"

#include "detector.hh"
#include "G4UIcmdWithADoubleAndUnit.hh"
#include "messenger.hh"
#include "generator.hh"


class MyDetectorConstruction : public G4VUserDetectorConstruction
{
public:
    MyDetectorConstruction();
    ~MyDetectorConstruction();
    
    G4LogicalVolume *GetScoringVolume() const { return ScoringVolume;}
    
    virtual G4VPhysicalVolume *Construct();
    virtual void ConstructSDandField();

    void SetSourcePosition(G4double position);
    void SetSnThickness(G4double thickness);
    void RegisterPrimaryGenerator(MyPrimaryGenerator *generator);

    G4double GetSourcePosition() const {return sourcePosition;}
    G4double GetSnTargetThickness() const {return snTargetThickness;}
    
private:

    G4double sourcePosition, snTargetThickness;
    G4Box *solidWorld;
    G4Tubs *solidSnTarget, *solidWindow, *solidDetector, *solidCase;
    G4LogicalVolume *logicSnTarget, *logicWorld, *logicWindow, *logicDetector, *logicCase;
    G4VPhysicalVolume *physSnTarget, *physWorld, *physWindow, *physDetector, *physCase;
    
    DetectorMessenger *messenger;
    G4UIcmdWithADoubleAndUnit *setSourcePositionCmd;
    MyPrimaryGenerator *fPrimaryGenerator;

    G4Material *Epoxy, *worldMat, *caseMat, *detMat, *targetMat;
    G4Element *C, *Al, *Ge, *Sn;
    
    void DefineMaterial();
    
    G4LogicalVolume *ScoringVolume;
    
};

#endif