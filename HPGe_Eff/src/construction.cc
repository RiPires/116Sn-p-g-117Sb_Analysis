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
    G4double xWorld = 100*mm;//World half lenght
    G4double yWorld = 100*mm;//World half height
    G4double zWorld = 100*mm;//World half depth       
    solidWorld = new G4Box("solidWorld", xWorld, yWorld, zWorld); 
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "LogicWorld");
    physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "PhysWorld", 0, false, 0, true);

    //  Defines cylinder for back side Ge crystal hole  //
    G4double Rin_Hole = 0.*mm;
    G4double Rout_Hole = 4.*mm; // 8 mm diameter
    G4double depth_Hole = 38.*mm;
    solidHole = new G4Tubs("SolidHole", Rin_Hole, Rout_Hole, depth_Hole, 0., 2*pi);

    //  Defines the back side, holed, of Ge DETECTOR  //
    solidGe = new G4Tubs("SolidGeBack", 0.*mm, 25*mm, 50.*mm, 0., 2*pi); // 5 cm diameter

    //  Subtracts inner hole from the Ge crystal  //
    G4VSolid *solidDetector = new G4SubtractionSolid("RealTargetFrame", solidGe, solidHole, rotation, G4ThreeVector(0., 0., 12.*mm));
    logicDetector = new G4LogicalVolume(solidDetector, detMat, "LogicDetector");
    physDetector = new G4PVPlacement(0, G4ThreeVector(0., 0., 35.*mm), logicDetector, "PhysDetector", logicWorld, false, 0., true);
    
    //  Defines Case volume for detector active volume  ///
    G4double Rin_Case = 41.*mm;
    G4double Rout_Case = 42.*mm;
    G4double depth_Case = 40.*mm;
    solidCase = new G4Tubs("SolidCase", Rin_Case, Rout_Case, depth_Case, 0., 2*pi);
    logicCase = new G4LogicalVolume(solidCase, holderMat, "LogicCase");
    physCase = new G4PVPlacement(0, G4ThreeVector(0., 0., 20.*mm), logicCase, "PhysCase", logicWorld, false, 0., true);

    //  Defines detector WINDOW volume  //
    G4double Rin_Win = 0.*mm;
    G4double Rout_Win = 41*mm;
    G4double Thick_Win = 0.3*mm;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, Epoxy, "LogicWindow");
    physWindow = new G4PVPlacement(0, G4ThreeVector(0., 0., -20.*mm), logicWindow, "PhysWindow", logicWorld, false, 0., true);
    
    ScoringVolume = logicDetector;
        
  return physWorld;
}    

//  Defines sensitive detector  //
void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet); 
}
