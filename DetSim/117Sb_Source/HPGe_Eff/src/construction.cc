#include "construction.hh"
#include "G4PhysicalConstants.hh"

void MyDetectorConstruction::RegisterPrimaryGenerator(MyPrimaryGenerator *generator){
    fPrimaryGenerator = generator;
}

MyDetectorConstruction::MyDetectorConstruction() : sourcePosition(-50 * mm), messenger(nullptr)
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
    
    //  Elements  //
    H = nist->FindOrBuildElement("H");
    C = nist->FindOrBuildElement("C");
    O = nist->FindOrBuildElement("O");
    Al = nist->FindOrBuildElement("Al");
    Ge = nist->FindOrBuildElement("Ge");

    //  Defines world material as Air  //
    worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    //  Defines target Holder material as Al  //
    holderMat = new G4Material("Aluminium", 2.7*g/cm3, 1);
    holderMat->AddElement(Al, 1.);
    
    //  Defines detector material as Ge  //
    detMat =  new G4Material("Germanium", 5.323*g/cm3, 1);
    detMat->AddElement(Ge, 1.);

    // Defines carbon fiber window material
    cw = new G4Material("CarbonFiber", 1.75*g/cm3, 1);
    cw->AddElement(C, 1.);

    // Defines mylar for source support
    mylar = new G4Material("Mylar", 1.4*g/cm3, 3);
    mylar->AddElement(H, 0.041959);
    mylar->AddElement(C, 0.625017);
    mylar->AddElement(O, 0.333025);
    
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

    // Defines mylar support of radioactive source
    G4double Rout_MylarSource = 25/2 * mm;
    G4double thickMylarSource = 200 * um;
    G4ThreeVector mylarPosition(0., 0., sourcePosition + 100 * um);
    solidMylarSource = new G4Tubs("solidMylarSource", 0., Rout_MylarSource, thickMylarSource/2, 0., 2*pi);
    logicMylarSource = new G4LogicalVolume(solidMylarSource, mylar, "LogicMylarSource");
    physMylarSource = new G4PVPlacement(0, mylarPosition, logicMylarSource, "PhysMylarSource", logicWorld, false, 0., true); 

    //  Defines cylinder for Ge crystal hole  //
    G4double Rin_Hole = 0.*mm;
    G4double Rout_Hole = 4.6*mm; // 9.2 mm diameter
    G4double depth_Hole = 27.7*mm;
    solidHole = new G4Tubs("SolidHole", Rin_Hole, Rout_Hole, depth_Hole, 0., 2*pi);

    //  Defines the Ge crystal unholed  //
    solidGe = new G4Tubs("SolidGeBack", 0.*mm, 27.95*mm, 31.85*mm, 0., 2*pi); // 55.9 mm diameter

    //  Subtracts inner hole from the Ge crystal  //
    G4VSolid *solidDetector = new G4SubtractionSolid("SolidDetector", solidGe, solidHole, rotation, G4ThreeVector(0., 0., 8.3*mm));
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
    G4double Thick_Win = 0.375*mm;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, cw, "LogicWindow");
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

// Method to set the source position
void MyDetectorConstruction::SetSourcePosition(G4double position)
{
    sourcePosition = position;  // Update the source position

    // Update the GPS source position (via the General Particle Source)
    G4UImanager::GetUIpointer()->ApplyCommand("/gps/pos/centre 0. 0. " + std::to_string(sourcePosition) + " mm");

    // Update Mylar position based on the source position (75 um behind)
    if (physMylarSource) {
        G4ThreeVector newMylarPosition(0., 0., sourcePosition + 100 * um);  // 75um behind the source
        physMylarSource->SetTranslation(newMylarPosition);  // Move the Mylar volume
    }

    // Notify Geant4 that the geometry has been modified
    G4RunManager::GetRunManager()->GeometryHasBeenModified();
}