import numpy as np
from PIL import Image
import db_con
import draw_labirynt
from Escapee import Escapee
from draw_labirynt import WHITE,BLACK,ALIVE,DEAD,HUNTER,EXIT,drawing



def get_state_from_color(color):
    if color == BLACK:
        return 1
    elif color ==WHITE:
        return 0
    elif color ==ALIVE:
        return 2
    elif color ==HUNTER:
        return 3
    elif color ==DEAD:
        return 4
    elif color ==EXIT:
        return 5

def read_lab_from_file(path):
    obraz=Image.open(path)
    obraz=obraz.convert("RGB")
    cols,rows=obraz.size
    pixels=np.array(obraz)
    map=np.zeros((rows,cols),dtype=int)
    for y in range(rows):
        for x in range(cols):
            color = tuple(pixels[y, x])  # Pobieramy kolor piksela w formacie RGB
            map[y, x] = get_state_from_color(color)
    return map
def lock_obj(board):
    rows,cols=board.shape
    hunters=[]
    exits=[]
    id=0
    for y in range(rows):
        for x in range(cols):
            if(board[y][x]==3):
                hunters.append((id,x,y))
                id+=1
            elif(board[y][x]==5):
                exits.append((x,y))
    print(hunters)
    return hunters,exits
def main():
    conn=db_con.connect_to_db()
    id=1
    print("Wczytywanie uciekinierów z bazy\n")
    escapees=[]
    while db_con.exists_escapee(conn,id):
        escapees.append(db_con.load_q_table(conn,id))
        escapees[id-1].print_info()
        id+=1
    if len(escapees)==0:
        print("No escapee\n")
    map_choice=int(input("Jesli chcesz wczytać domyślną mapę podaj 1 jeśli stworzyc nową - 2: "))
    if map_choice==1:
        map=read_lab_from_file("./default.png")
    elif map_choice==2:
        map=np.array(drawing(800,800))
    hunters,exits=lock_obj(map)
    if not hunters:
        print("no hunters - place hunters")
        if not exits:
            print("no exits - place exits")
        drawing(50,50,map)
        hunters, exits = lock_obj(map)
    if not exits:
        print("no exits - place exits")
        drawing(50, 50, map)
        hunters, exits = lock_obj(map)
    on_screen=0

    escp_placed=[]
    for escp in escapees:
        x,y,wtd=draw_labirynt.place_escapee(map)
        if not wtd:
                break
        escp.set_state(x,y)
        escp_placed.append(escp)
        print(escp.escapee_id," ",escp.pos_x," ",escp.pos_y)
        on_screen+=1


    if on_screen+1==id:
        add_esp=True
        while add_esp:
            print("czy chcesz dodać uciekiniera -T -tak; -N - nie")
            choice=input()
            if choice=="T":
                db_con.insert_escapee(conn,id)
                escp_placed.append(Escapee(id,environment=None))
                x, y = draw_labirynt.place_escapee(map)
                escp_placed[id-1].set_state(x, y)
                id += 1
            else:
                add_esp=False
    print(escp_placed)
    draw_labirynt.simulate(map,hunters,escp_placed,exits,conn)

main()
