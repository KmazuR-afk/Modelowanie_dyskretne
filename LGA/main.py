from svgwrite import Drawing

from Automaton import Automaton
import Drawing as draw
from LBM import LBM
from LBM_fluid import LBM_fluid
def main():
    #simul=Automaton(100,1)
    #draw.simul(simul)
    #simul=LBM(1,100)
    simul=LBM_fluid(1,100)
    draw.simul_LBM(simul)

main()