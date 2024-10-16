#include "construction.hh"
#include "G4PhysicalConstants.hh"


MyDetectorConstruction::MyDetectorConstruction()
{
    fMessenger = new G4GenericMessenger(this, "/detector/", "DetectorConstruction");
    
    DefineMaterial();
}

MyDetectorConstruction::~MyDetectorConstruction()
{}

void MyDetectorConstruction::DefineMaterial()
{
    //  Materials  //
    G4NistManager *nist = G4NistManager::Instance();

    // Carbon Epoxy: C21H25ClO5  //
    Epoxy = new G4Material("Epoxy", 1.600*g/cm3, 4);
    Epoxy->AddElement(nist->FindOrBuildElement("C"), 21);
    Epoxy->AddElement(nist->FindOrBuildElement("H"), 25);
    Epoxy->AddElement(nist->FindOrBuildElement("Cl"), 1);
    Epoxy->AddElement(nist->FindOrBuildElement("O"), 5);

    //  Mylar: H4C5O2  //
    mylar = new G4Material("Mylar", 1.39*g/cm3, 3);
    mylar->AddElement(nist->FindOrBuildElement("H"), 4);
    mylar->AddElement(nist->FindOrBuildElement("C"), 5);
    mylar->AddElement(nist->FindOrBuildElement("O"), 2);
    
    //  Elements  //
    Al = nist->FindOrBuildElement("Al");
    C = nist->FindOrBuildElement("C");
    Ge = nist->FindOrBuildElement("Ge");
    Sn = nist->FindOrBuildElement("Sn");

    //  Defines world material as Air  //
    worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    //  Defines target Holder material as Al  //
    holderMat = new G4Material("Aluminium", 2.7*g/cm3, 1);
    holderMat->AddElement(Al, 1.);
    
    //  Defines target material as Sn  //
    targetMat = new G4Material("Tin", 7.31*g/cm3, 1);
    targetMat->AddElement(Sn, 1.);
    
    //  Defines detector material as Ge  //
    detMat =  new G4Material("Germanium", 5.323*g/cm3, 1);
    detMat->AddElement(Ge, 1.);
    
}
///OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO///
G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
    //  Defines WORLD volume  //
    G4double xWorld = 110*mm;//World half lenght
    G4double yWorld = 110*mm;//World half height
    G4double zWorld = 110*mm;//World half depth       
    solidWorld = new G4Box("solidWorld", xWorld, yWorld, zWorld); 
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "LogicWorld");
    physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "PhysWorld", 0, false, 0, true);

    //  Defines cylinder for Ge crystal hole  //
    G4double Rin_Hole = 0.*mm;
    G4double Rout_Hole = 4.6*mm; // 9.2 mm diameter
    G4double depth_Hole = 27.7*mm;
    solidHole = new G4Tubs("SolidHole", Rin_Hole, Rout_Hole, depth_Hole, 0., 2*pi);

    //  Defines the Ge crystal unholed  //
    solidGe = new G4Tubs("SolidGeBack", 0.*mm, 27.95*mm, 31.85*mm, 0., 2*pi); // 55.9 mm diameter

    //  Subtracts inner hole from the Ge crystal  //
    G4VSolid *solidDetector = new G4SubtractionSolid("RealTargetFrame", solidGe, solidHole, rotation, G4ThreeVector(0., 0., 8.3*mm));
    logicDetector = new G4LogicalVolume(solidDetector, detMat, "LogicDetector");
    physDetector = new G4PVPlacement(0, G4ThreeVector(0., 0., 30.*mm), logicDetector, "PhysDetector", logicWorld, false, 0., true);
    
    //  Defines internal Al Case  //
    G4double Rin_Case = 32.95*mm;
    G4double Rout_Case = 33.75*mm;
    G4double depth_Case = 52.5*mm;
    solidCase = new G4Tubs("SolidCase", Rin_Case, Rout_Case, depth_Case, 0., 2*pi);
    logicCase = new G4LogicalVolume(solidCase, holderMat, "LogicCase");
    physCase = new G4PVPlacement(0, G4ThreeVector(0., 0., 50.65*mm), logicCase, "PhysCase", logicWorld, false, 0., true);

    //  Defines Carbon Fiber window  //
    G4double Rin_Win = 0.*mm;
    G4double Rout_Win = 38*mm;
    G4double Thick_Win = 0.45*mm;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, Epoxy, "LogicWindow");
    physWindow = new G4PVPlacement(0, G4ThreeVector(0., 0., -4.85*mm), logicWindow, "PhysWindow", logicWorld, false, 0., true);
    
    //  Defines mylar  window  //
    G4double Rin_mylar = 0.*mm;
    G4double Rout_mylar = 33.75*mm;
    G4double thick_mylar = 0.015*mm;
    solidMylar = new G4Tubs("SolidMylar", Rin_mylar, Rout_mylar, thick_mylar, 0., 2*pi);
    logicMylar = new G4LogicalVolume(solidMylar, mylar, "LogicMylar");
    physMylar = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.87*mm), logicMylar, "PhysMylar", logicWorld, false, 0., true);
    
    ScoringVolume = logicDetector;
        
  return physWorld;
}    

//  Defines sensitive detector  //
void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet); 
}
