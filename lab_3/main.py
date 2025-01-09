import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
con_drawing = True
war = 1
def on_key(event):
    global con_drawing
    if event.key==' ':
        con_drawing=False
    elif event.key=='escape':
        plt.close(event.canvas.figure)

def apply_rule(rule,state):
    global war
    bin_rule=np.array([int(x) for x in f"{rule:08b}"])
    new_state=np.zeros_like(state)
    size=len(state)
    if war == 1:#periodyczny
        for i in range(0,size):
            if i==0:
                nb=np.array([state[size-1],state[0],state[1]])
            elif i==size-1:
                nb=np.array([state[size-2],state[size-1],state[0]])
            else:
                nb=state[i-1:i+2]
            in_r=7-int("".join(str(x) for x in nb),2)
            new_state[i]=bin_rule[in_r]
    elif war==2:#absorbcyjny
        for i in range(0,size):
            if i==0:
                nb=np.array([0,state[0],state[1]])
            elif i==size-1:
                nb=np.array([state[size-2],state[size-1],0])
            else:
                nb=state[i-1:i+2]
            in_r=7-int("".join(str(x) for x in nb),2)
            new_state[i]=bin_rule[in_r]
    return new_state

def run_automaton(rule,len,iter=100,filename='automat.csv',state=None,disp=True):
    global con_drawing
    con_drawing=disp
    if con_drawing:
        plt.ion()
        fig,ax=plt.subplots()
        fig.canvas.mpl_connect('key_press_event',on_key)
    if state==None:
        state=np.random.randint(2,size=len)
    ret = np.zeros(shape=(iter + 1, len))
    ret[0] = state
    for i in range(iter):
        state=apply_rule(rule,state)
        ret[i+1]=state
        if con_drawing:
            ax.clear()
            ax.imshow(ret,cmap='binary',interpolation='nearest')
            plt.show()
            plt.pause(1e-10)
    con_drawing=disp
    if con_drawing:
        ax.clear()
        ax.imshow(ret, cmap='binary', interpolation='nearest')
        plt.show()
        while(plt.fignum_exists(fig.number)):
            plt.pause(1e-10)
    np.savetxt(filename,ret,delimiter=';',fmt='%i')

    bmp=filename.replace('.csv','.bmp')

    inverted_ret = np.where(ret == 1, 0, 255)
    im = Image.fromarray(inverted_ret.astype(np.uint8))
    im.save(bmp)
    return ret

def main():
    global con_drawing, war
    while(True):
        w=int(input("Wybierz:\n1.Program wygeneruje przebieg dla wybranego rozmiaru automatu i ilości iteracji dla reguł [41,55,88,190] i warunku periodycznego\n2.Program wygeneruje przebieg dla wybranego rozmiaru automatu i ilości iteracji dla reguł [41,55,88,190] i warunku absorbcyjnego\n3.Własne reguły\n"))
        if w not in [1,2,3]:
            print("Zły wybór DOWIDZENIA\n")
            break
        else:
            len = int(input("podaj rozmiar automatu:\n"))
            while len == 0:
                len = int(input("podaj poprawny rozmiar !=0:\n"))
            iter = int(input("podaj ilość iteracji:\n"))
            while iter == 0:
                iter = int(input("podaj poprawny rozmiar !=0:\n"))
            if w == 1:
                run_automaton(41,len,iter,'41_1.csv',disp=False)
                run_automaton(55, len, iter, '55_1.csv',disp=False)
                run_automaton(88, len, iter, '88_1.csv',disp=False)
                run_automaton(190, len, iter, '190_1.csv',disp=False)
            elif w==2:
                run_automaton(41, len, iter, '41_2.csv',disp=False)
                run_automaton(55, len, iter, '55_2.csv',disp=False)
                run_automaton(88, len, iter, '88_2.csv',disp=False)
                run_automaton(190, len, iter, '190_2.csv',disp=False)
            else:
                war = int(input("Wybierz warunek brzegowy:\n1.periodyczny\n2.absorbcyjny\n"))
                while war != 1 and war != 2:
                    war = int(input("podaj poprawny warunek =1 lub =2:\n"))
                rule = int(input("Wybierz regułę Wolframa - liczba 0-255:\n"))
                while rule not in range(0, 255):
                    rule = int(input("podaj regułę:\n"))
                fn = str(input("Podaj nazwę pliku zapisowego - w przypadku braku zapisze się jako automat.csv:"))
                if fn == ('\n'):
                    run_automaton(rule, len, iter)
                else:
                    run_automaton(rule, len, iter, fn)
            print("Czy chcesz jeszcze raz?\n")
            w = str(input())
            if w == 'n' or w == 'N':
                break

main()