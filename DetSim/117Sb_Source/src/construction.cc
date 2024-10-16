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

    // Carbon Epoxy: C21H25ClO5 for Ge detector Window //
    Epoxy = new G4Material("Epoxy", 1.600*g/cm3, 4);
    Epoxy->AddElement(nist->FindOrBuildElement("C"), 21);
    Epoxy->AddElement(nist->FindOrBuildElement("H"), 25);
    Epoxy->AddElement(nist->FindOrBuildElement("Cl"), 1);
    Epoxy->AddElement(nist->FindOrBuildElement("O"), 5);
    
    //   Elements   //
    Be = nist->FindOrBuildElement("Be");
    Al = nist->FindOrBuildElement("Al");
    Si = nist->FindOrBuildElement("Si");
    Ge = nist->FindOrBuildElement("Ge");

    //   Defines world material as Air  //
    worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    //   Defines target Holder material as Al   //
    caseMat = new G4Material("Aluminium", 2.7*g/cm3, 1);
    caseMat->AddElement(Al, 1.);
    
    // Defines detector material as Ge  //
    detMatGe =  new G4Material("Germanium", 5.323*g/cm3, 1);
    detMatGe->AddElement(Ge, 1.);

    // Defines detector material as Si  //
    detMatSi =  new G4Material("Silicon", 2.329*g/cm3, 1);
    detMatSi->AddElement(Si, 1.);

    // Defines Si detector window as Be  //
    winBe =  new G4Material("Berillium", 1.845*g/cm3, 1);
    winBe->AddElement(Be, 1.);
}

///OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO///
G4VPhysicalVolume *MyDetectorConstruction::Construct()
{
    //   Defines WORLD volume   //
    G4double xWorld = 100*mm;//World half lenght
    G4double yWorld = 100*mm;//World half height
    G4double zWorld = 100*mm;//World half depth    
    solidWorld = new G4Box("solidWorld", xWorld, yWorld, zWorld); 
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "LogicWorld");
    physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "PhysWorld", 0, false, 0, true);
    
    //   Defines Case volume for detector active volume   ///
    G4double Rin_Case = 41.*mm;
    G4double Rout_Case = 42.*mm;
    G4double depth_Case = 40.*mm;
    solidCase = new G4Tubs("SolidCase", Rin_Case, Rout_Case, depth_Case, 0., 2*pi);
    logicCase = new G4LogicalVolume(solidCase, caseMat, "LogicCase");
    physCase = new G4PVPlacement(0, G4ThreeVector(0., 0., 45.*mm), logicCase, "PhysCase", logicWorld, false, 0., true);

    //   Defines Ge detector WINDOW volume   //
    G4double Rin_Win = 0.*mm;
    G4double Rout_Win = 41*mm;
    G4double Thick_Win = 0.3*mm;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, Epoxy, "LogicWindow");
    physWindow = new G4PVPlacement(0, G4ThreeVector(0., 0., 10.*mm), logicWindow, "PhysWindow", logicWorld, false, 0., true);
    
    //   Defines Ge DETECTOR active volume  //
    solidDetector = new G4Tubs("SolidDetector", 0.*m, 2.985*cm, 25.*mm, 0., 2*pi); // radius of 2.985 cm lead to ~ 28 cm² of active area
    logicDetector = new G4LogicalVolume(solidDetector, detMatGe, "LogicDetector");
    physDetector = new G4PVPlacement(0, G4ThreeVector(0., 0., 40.*mm), logicDetector, "PhysDetector", logicWorld, false, 0., true);

    //   Defines Si detectors' Be Window volume   //
    G4double Rin_WinBe = 0.*mm;
    G4double Rout_WinBe = 3*mm;
    G4double Thick_WinBe = 8*um;
    solidWinBe = new G4Tubs("SolidWindowSi", Rin_WinBe, Rout_WinBe, Thick_WinBe, 0., 2*pi);
    logicWinBe = new G4LogicalVolume(solidWinBe, winBe, "LogicWindowBe");
    physWinBe = new G4PVPlacement(0, G4ThreeVector(0., 0., -5.*mm), logicWinBe, "PhysWindowBe", logicWorld, false, 0., true);
    
    //   Defines Si DETECTOR active volume  //
    solidDetSi = new G4Tubs("SolidDetector", 0.*m, 2.82*mm, 500.*um, 0., 2*pi);
    logicDetSi = new G4LogicalVolume(solidDetSi, detMatSi, "LogicDetector");
    physDetSi = new G4PVPlacement(0, G4ThreeVector(0., 0., -6.4*mm), logicDetSi, "PhysDetector", logicWorld, false, 0., true);
    
    ScoringVolume = logicDetector;
    ScoringSi = logicDetSi;
        
  return physWorld;
}    

//   Defines sensitive detector//
void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet); 

    SiSensitiveDetector *sensDetSi = new SiSensitiveDetector("SensitiveDetectorSi");
    logicDetSi->SetSensitiveDetector(sensDetSi); 
}
