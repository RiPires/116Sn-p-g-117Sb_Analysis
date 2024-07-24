#include <iostream>

void FitPeak(double fitMin, double fitMax) {
    TF1 *gausFit = new TF1('gausFit', 'gaus', fitMin, fitMax);
}