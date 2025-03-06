#include "construction.hh"
#include "G4PhysicalConstants.hh"
#include "G4Region.hh"
#include "G4ProductionCuts.hh"


void MyDetectorConstruction::RegisterPrimaryGenerator(MyPrimaryGenerator *generator) {
    fPrimaryGenerator = generator;
}

MyDetectorConstruction::MyDetectorConstruction() : sourcePosition(10 * mm), messenger(nullptr)  // Default value for source position
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
    Be = nist->FindOrBuildElement("Be");
    Al = nist->FindOrBuildElement("Al");
    Si = nist->FindOrBuildElement("Si");
    Ti = nist->FindOrBuildElement("Ti");
    Cr = nist->FindOrBuildElement("Cr");
    Ni = nist->FindOrBuildElement("Ni");
    W = nist->FindOrBuildElement("W");

    // Defines world material as Air  //
    worldMat = nist->FindOrBuildMaterial("G4_AIR");
    
    // Defines detector material as Si  //
    detMat =  new G4Material("Silicon", 2.329*g/cm3, 1);
    detMat->AddElement(Si, 1.);

    // Defines Be window material
    beWinMat = new G4Material("Be", 1.845*g/cm3, 1);
    beWinMat->AddElement(Be, 1.);

    // Defines Multi Layer Collimator materials
    collMatAl = new G4Material("Aluminium", 2.7*g/cm3, 1);
    collMatAl->AddElement(Al, 1.);

    collMatTi = new G4Material("Titanium", 4.502*g/cm3, 1);
    collMatTi->AddElement(Ti, 1.);

    collMatCr = new G4Material("Chromium", 7.192*g/cm3, 1);
    collMatCr->AddElement(Cr, 1.);

    collMatW = new G4Material("Tungsten", 19.254*g/cm3, 1);
    collMatW->AddElement(W, 1.);

    // Defines detector cover material as Ni
    coverMat = new G4Material("Nickel", 8.907*g/cm3, 1);
    coverMat->AddElement(Ni, 1);

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
    G4double xWorld = 20*mm;//World half lenght
    G4double yWorld = 20*mm;//World half height
    G4double zWorld = 20*mm;//World half depth       
    solidWorld = new G4Box("solidWorld", xWorld, yWorld, zWorld); 
    logicWorld = new G4LogicalVolume(solidWorld, worldMat, "LogicWorld");
    physWorld = new G4PVPlacement(0, G4ThreeVector(0., 0., 0.), logicWorld, "PhysWorld", 0, false, 0, true);

    // Defines mylar support of radioactive source
    G4double Rout_Mylar = 25/2 * mm;
    G4double thickMylar = 200 * um;
    G4ThreeVector mylarPosition(0., 0., sourcePosition - 100 * um);
    solidMylar = new G4Tubs("solidMylar", 0., Rout_Mylar, thickMylar/2, 0., 2*pi);
    logicMylar = new G4LogicalVolume(solidMylar, mylar, "LogicMylar");
    physMylar = new G4PVPlacement(0, mylarPosition, logicMylar, "PhysMylar", logicWorld, false, 0., true); 

    //  Defines Si crystal //
    G4double Rin_Si = 0*mm;
    G4double Rout_Si = 2.8209*mm;
    G4double depth_Si = 500*um;
    solidSi = new G4Tubs("SolidSi", Rin_Si, Rout_Si, depth_Si/2, 0., 2*pi);
    logicSi = new G4LogicalVolume(solidSi, detMat, "LogicSi");
    physSi = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.65*mm), logicSi, "PhysSi", logicWorld, false, 0., true);

    //  Defines Be window  //
    G4double Rin_Win = 0.*mm;
    G4double Rout_Win = 3.5*mm;
    G4double Thick_Win = 12.5*um;
    solidWindow = new G4Tubs("SolidWindow", Rin_Win, Rout_Win, Thick_Win/2, 0., 2*pi);
    logicWindow = new G4LogicalVolume(solidWindow, beWinMat, "LogicWindow");
    physWindow = new G4PVPlacement(0, G4ThreeVector(0., 0., -0.00625*mm), logicWindow, "PhysWindow", logicWorld, false, 0., true);
    
    // Defines Multi-Layer Collimator layers
    // W layer
    G4double R_Coll = 2.615*mm;
    G4double thick_W = 100*um;
    solidW = new G4Tubs("SolidTungsten", R_Coll, Rout_Si, thick_W/2, 0., 2*pi);
    logicW = new G4LogicalVolume(solidW, collMatW, "LogicTungsten");
    physW = new G4PVPlacement(0, G4ThreeVector(0., 0., -0.95*mm), logicW, "PhysTungsten", logicWorld, false, 0., true);

    // Cr layer
    G4double thick_Cr = 35*um;
    solidCr = new G4Tubs("SolidChromium", R_Coll, Rout_Si, thick_Cr/2, 0., 2*pi);
    logicCr = new G4LogicalVolume(solidCr, collMatCr, "LogicChromium");
    physCr = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.0175*mm), logicCr, "PhysChromium", logicWorld, false, 0., true);

    // Ti layer
    G4double thick_Ti = 15*um;
    solidTi = new G4Tubs("SolidTitanium", R_Coll, Rout_Si, thick_Ti/2, 0., 2*pi);
    logicTi = new G4LogicalVolume(solidTi, collMatTi, "LogicTitanium");
    physTi = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.0425*mm), logicTi, "PhysTitanium", logicWorld, false, 0., true);

    // Al layer
    G4double thick_Al = 75*um;
    solidAl = new G4Tubs("SolidAluminium", R_Coll, Rout_Si, thick_Al/2, 0., 2*pi);
    logicAl = new G4LogicalVolume(solidAl, collMatAl, "LogicAluminium");
    physAl = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.0875*mm), logicAl, "PhysAluminium", logicWorld, false, 0., true);

    //  Defines Ni cover unholed 
    G4double Dout_Ni = 15.24*mm;
    G4double Thick_Ni = 2*mm;
    solidNi = new G4Tubs("SolidNi", Rout_Win, Dout_Ni/2, Thick_Ni/2, 0., 2*pi);

    // Defines cylinder for cover hole
    G4double thickHole = Thick_Ni;
    solidHole = new G4Tubs("SolidHole", Rout_Win-0.1*mm, Dout_Ni/2-0.127*mm, thickHole/2, 0., 2*pi);

    // Subtract inner hole from the Ni cover
    G4VSolid *solidCover = new G4SubtractionSolid("SolidCover", solidNi, solidHole, rotation, G4ThreeVector(0., 0., -0.127*mm));
    logicCover = new G4LogicalVolume(solidCover, coverMat, "LogicCover");
    physCover = new G4PVPlacement(0, G4ThreeVector(0., 0., -1.*mm), logicCover, "PhysCover", logicWorld, false, 0., true);

    ScoringVolume = logicSi;
        
  return physWorld;
}    

//  Defines sensitive detector  //
void MyDetectorConstruction::ConstructSDandField()
{
    MySensitiveDetector *sensDet = new MySensitiveDetector("SensitiveDetector");
    logicSi->SetSensitiveDetector(sensDet); 
}


// Method to set the source position
void MyDetectorConstruction::SetSourcePosition(G4double position)
{
    sourcePosition = position;  // Update the source position

    // Update the GPS source position (via the General Particle Source)
    G4UImanager::GetUIpointer()->ApplyCommand("/gps/pos/centre 0. 0. " + std::to_string(sourcePosition) + " mm");

    // Update Mylar position based on the source position (75 um behind)
    if (physMylar) {
        G4ThreeVector newMylarPosition(0., 0., sourcePosition - 100 * um);  // 75um behind the source
        physMylar->SetTranslation(newMylarPosition);  // Move the Mylar volume
    }

    // Notify Geant4 that the geometry has been modified
    G4RunManager::GetRunManager()->GeometryHasBeenModified();
}



