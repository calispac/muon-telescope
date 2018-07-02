from root_numpy import root2array
import ROOT

def read(file):

    f = ROOT.TFile(file, 'read')

    print(f.ls())
    print(f.Print())
    print(f)

    t = f.Get('FEB_1')

    print(t.Print())

if __name__ == '__main__':
    read('data/25May_3_ON_MCR0_T2K_beamline_trigger_beam60us_neutrinos_ON_histo.root')