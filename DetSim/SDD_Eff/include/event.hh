#ifndef EVENT_HH
#define EVENT_HH

#include "G4UserEventAction.hh"
#include "G4Event.hh"
#include "g4root.hh"
#include "run.hh"

#include <vector>
#include <string>

class MyEventAction : public G4UserEventAction
{
    public:
        MyEventAction(MyRunAction*);
        ~MyEventAction();
    
        virtual void BeginOfEventAction(const G4Event*);
        virtual void EndOfEventAction(const G4Event*);

        void AddEdep(G4double edep) {Edep += edep;}
    
    private:
        G4double Edep;
    
};
#endif