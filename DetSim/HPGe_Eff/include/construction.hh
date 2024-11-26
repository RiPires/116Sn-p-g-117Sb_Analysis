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
#include "G4RotationMatrix.hh"
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
    void RegisterPrimaryGenerator(MyPrimaryGenerator *generator);

    G4double GetSourcePosition() const { return sourcePosition; }
    
private:
    
    G4double sourcePosition;
    G4Box *solidWorld;
    G4Tubs *solidHole, *solidGe, *solidWindow, *solidMylar, *solidMylarSource, *solidCase;
    G4LogicalVolume *logicWorld, *logicWindow, *logicMylar, *logicMylarSource, *logicDetector, *logicCase;
    G4VPhysicalVolume *physWorld, *physWindow, *physMylar, *physMylarSource, *physDetector, *physCase;
    G4RotationMatrix *rotation = new G4RotationMatrix();
    
    DetectorMessenger *messenger;
    G4UIcmdWithADoubleAndUnit *setSourcePositionCmd;
    MyPrimaryGenerator *fPrimaryGenerator;
    
    G4Material *mylar, *holderMat, *worldMat, *detMat, *cw;
    G4Element *H, *C, *O, *Al, *Ge, *Si;
    
    void DefineMaterial();
    
    G4LogicalVolume *ScoringVolume;
};

#endif



