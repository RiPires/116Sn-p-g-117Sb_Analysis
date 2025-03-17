#include "construction.hh"
#include "G4PhysicalConstants.hh"

void MyDetectorConstruction::RegisterPrimaryGenerator(MyPrimaryGenerator *generator){
    fPrimaryGenerator = generator;
}

MyDetectorConstruction::MyDetectorConstruction() : sourcePosition(-20*mm), 
                                                   snTargetThickness(1*um),
                                                   messenger(nullptr)
{
    // Define materials and other necessary initializations
    DefineMaterial();

    // Initialize the messenger object
    messenger = new DetectorMessenger(this);
}

MyDetectorConstruction::~MyDetectorConstruction()
{
    delete messenger;
    delete setSourcePositionCmd;
}

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
    C = nist->FindOrBuildElement("C");
    Al = nist->FindOrBuildElement("Al");
    Ge = nist->FindOrBuildElement("Ge");
    Sn = nist->FindOrBuildElement("Sn");

    //  Defines world material as Air  //
    worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    //  Defines detector Case material as Al  //
    caseMat = new G4Material("Aluminium", 2.7*g/cm3, 1);
    caseMat->AddElement(Al, 1.);
    
    //  Defines detector material as Ge  //
    detMat =  new G4Material("Germanium", 5.323*g/cm3, 1);
    detMat->AddElement(Ge, 1.);

    targetMat = new G4Material("Tin", 7.31*g/cm3, 1);
    targetMat->AddElement(Sn, 1);
    
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
    
    // Defines Sn target
    G4double Rout_SnTarget = 5 * mm;
    G4double thickSnTarget = snTargetThickness;
    G4ThreeVector targetPosition(0., 0., sourcePosition); // the source is in the middle of the target
    solidSnTarget = new G4Tubs("solidSnTarget", 0., Rout_SnTarget, thickSnTarget/2, 0., 2*pi);
    logicSnTarget = new G4LogicalVolume(solidSnTarget, targetMat, "LogicSnTarget");
    physSnTarget = new G4PVPlacement(0, targetPosition, logicSnTarget, "PhysSnTarget", logicWorld, false, 0., true); 
    
    //  Defines Case volume for detector active volume  ///
    G4double Rin_Case = 41.*mm;
    G4double Rout_Case = 42.*mm;
    G4double depth_Case = 40.*mm;
    solidCase = new G4Tubs("SolidCase", Rin_Case, Rout_Case, depth_Case, 0., 2*pi);
    logicCase = new G4LogicalVolume(solidCase, caseMat, "LogicCase");
    physCase = new G4PVPlacement(0, G4ThreeVector(0., 0., 40.*mm), logicCase, "PhysCase", logicWorld, false, 0., true);

    //  Defines detector WINDOW volume  //
    G4double Rin_Win = 0.*mm;
    G4double Rout_Win = 41*mm;
    G4double Thick_Win = 0.3*mm;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, Epoxy, "LogicWindow");
    physWindow = new G4PVPlacement(0, G4ThreeVector(0., 0., 2.*mm), logicWindow, "PhysWindow", logicWorld, false, 0., true);
    
    //  Defines Ge DETECTOR active volume  //
    solidDetector = new G4Tubs("SolidDetector", 0.*m, 2.985*cm, 25.*mm, 0., 2*pi); // radius of 2.985 cm lead to ~ 28 cm² of active area
    logicDetector = new G4LogicalVolume(solidDetector, detMat, "LogicDetector");
    physDetector = new G4PVPlacement(0, G4ThreeVector(0., 0., 33.*mm), logicDetector, "PhysDetector", logicWorld, false, 0., true);
    
    ScoringVolume = logicDetector;
        
  return physWorld;
}    

//  Defines sensitive detector  //
void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicDetector->SetSensitiveDetector(sensDet); 
}

// Method to set the source position
void MyDetectorConstruction::SetSourcePosition(G4double position)
{
    sourcePosition = position;  // Update the source position

    // Update the GPS source position (via the General Particle Source)
    G4UImanager::GetUIpointer()->ApplyCommand("/gps/pos/centre 0. 0. " + std::to_string(sourcePosition) + " mm");

    // Update Mylar position based on the source position (75 um behind)
    if (physSnTarget) {
        G4ThreeVector newTargetPosition(0., 0., sourcePosition);  // in the middle of the target
        physSnTarget->SetTranslation(newTargetPosition);  // Move the Mylar volume
    }

    // Notify Geant4 that the geometry has been modified
    G4RunManager::GetRunManager()->GeometryHasBeenModified();
}

// Method to set the Sn target thickness
void MyDetectorConstruction::SetSnThickness(G4double thickness)
{
    snTargetThickness = thickness;

    if (physSnTarget) {
        solidSnTarget->SetZHalfLength(snTargetThickness/2.0);
        G4cout << "Sn target thickness updated to: " << snTargetThickness / um << " um" << G4endl;        
    }

    G4RunManager::GetRunManager()->GeometryHasBeenModified();
}