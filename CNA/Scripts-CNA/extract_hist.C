#include <TFile.h>
#include <TCanvas.h>
#include <TList.h>
#include <TH1.h>
#include <TGraph.h>
#include <TMultiGraph.h>
#include <iostream>

void extrair_tudo() {
    TFile *f_in = TFile::Open("data/AbsoluteEfficiency_HPGe_100mm_1e6.root");
    TCanvas *c = (TCanvas*)f_in->Get("effCanvas");

    if (!c) {
        std::cout << "Canvas nao encontrada." << std::endl;
        return;
    }

    TObject *obj_encontrado = nullptr;

    // Percorre todos os objetos gráficos dentro da Canvas
    TIter next(c->GetListOfPrimitives());
    TObject *obj;
    while ((obj = next())) {
        // Verifica se e um Histograma, TGraph ou TMultiGraph
        if (obj->InheritsFrom(TH1::Class()) || 
            obj->InheritsFrom(TGraph::Class()) || 
            obj->InheritsFrom(TMultiGraph::Class())) {
            
            // Ignora os eixos temporarios criados ao desenhar
            TString name = obj->GetName();
            if (name != "hframe") {
                obj_encontrado = obj;
                break;
            }
        }
    }

    if (obj_encontrado) {
        std::cout << "Objeto encontrado! Tipo: " << obj_encontrado->ClassName() 
                  << " | Nome: " << obj_encontrado->GetName() << std::endl;

        // Salva o objeto num ficheiro limpo
        TFile *f_out = TFile::Open("HPGe_100mm.root", "RECREATE");
        obj_encontrado->Write("curva_eficiencia");
        f_out->Close();

        std::cout << "Salvo com sucesso como 'curva_eficiencia' em HPGe_100mm.root!" << std::endl;
    } else {
        std::cout << "Nenhum objeto de curva/histograma reconhecido dentro da Canvas." << std::endl;
    }
}