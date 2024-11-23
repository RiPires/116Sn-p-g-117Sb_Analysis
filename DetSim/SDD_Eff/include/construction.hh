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
    void RegisterPrimaryGenerator(MyPrimaryGenerator* generator);

    G4double GetSourcePosition() const { return sourcePosition; }
    
private:
    
    G4double sourcePosition; 
    G4Box *solidWorld;
    G4Tubs *solidMylar, *solidWindow, *solidW, *solidCr, *solidTi, *solidAl, *solidSi, *solidNi, *solidHole;
    G4LogicalVolume *logicMylar, *logicWorld, *logicWindow, *logicW, *logicCr, *logicTi, *logicAl, *logicSi, *logicCover;
    G4VPhysicalVolume *physMylar, *physWorld, *physWindow, *physW, *physCr, *physTi, *physAl, *physSi, *physCover;
    G4RotationMatrix *rotation = new G4RotationMatrix();
    
    DetectorMessenger* messenger;
    G4UIcmdWithADoubleAndUnit* setSourcePositionCmd;
    MyPrimaryGenerator *fPrimaryGenerator;
    
    G4Material *collMatAl, *collMatTi, *collMatCr, *collMatW, *worldMat, *detMat, *silicon, *beWinMat, *coverMat, *mylar;
    G4Element *H, *C, *O, *Be, *Al, *Si, *Ti, *Cr, *Ni, *W;
    
    void DefineMaterial();
    
    G4LogicalVolume *ScoringVolume;
    
};

#endif



