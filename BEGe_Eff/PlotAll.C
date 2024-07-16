#include <iostream>
#include <string>
#include <TSystem.h>
#include "Plot.C"


void PlotAll(int index) {

    for (int i = 0; i<= index; ++i) {
        std::string filename = "output" + std::to_string(i) + ".root";
        std::cout << "Plotting file: " << filename << std::endl;
        // Call the Plot function with the filename
        Plot(filename.c_str());
        std::cin.ignore();
    }
}