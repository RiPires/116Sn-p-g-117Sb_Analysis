#include <iostream>
#include <string>
#include <TSystem.h>

void hadd(int maxIndex) {
    for (int i = 0; i <= maxIndex; ++i) {
        // Construct the hadd command
        std::string command = "hadd add" + std::to_string(i) + ".root output" + std::to_string(i) + "_t0.root output" + std::to_string(i) + "_t1.root output" + std::to_string(i) + "_t2.root output" + std::to_string(i) + "_t3.root";

        // Print the command to verify it
        std::cout << "Executing: " << command << std::endl;

        // Execute the hadd command
        gSystem->Exec(command.c_str());
    }
}
